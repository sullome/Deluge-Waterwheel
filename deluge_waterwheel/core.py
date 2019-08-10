# Copyright (C) 2019 Constantine Farrahov <sullome.techie@gmail.com>
#
# Basic plugin template created by the Deluge Team.
#
# This file is part of Waterwheel and is licensed under GNU GPL 3.0, or later,
# with the additional special exception to link portions of this program with
# the OpenSSL library. See LICENSE for more details.
import logging
from collections import namedtuple
from functools import wraps

from twisted.internet.defer import ensureDeferred

import deluge.configmanager
from deluge import component
from deluge.core.rpcserver import export
from deluge.plugins.pluginbase import CorePluginBase

log = logging.getLogger(__name__)

DEFAULT_PREFS = {
    "order": "alphabetical",  # TODO: put to use
    "labels": [],
    "amount_top": 1,
    "amount_second": 2,
}

# Values are given in deluge/core/torrent.py
Priority = namedtuple("Priority", ["skip", "low", "normal", "high"])
PRIORITY = Priority(0, 1, 4, 7)


def wrap_for_twisted(func):
    """This decorator is needed for async functions
    to work with LoopingCall, maybeDeferred and other Twisted functions
    that Deluge uses in component.Component.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        coroutine = func(*args, **kwargs)
        return ensureDeferred(coroutine)

    return wrapper


def update_torrent_priorities(torrent_id, top=1, second=1):
    """Adjust files priorities for a specified torrent

    From deluge/core/torrent.py

    files (list of dict):
        The files this torrent contains
        The format for the file dict::
            {
                "index": int,
                "path": str,
                "size": int,
                "offset": int
            }

    file_priorities (list of int):
        The priority for files in torrent, range is [0..7] however
        only [0, 1, 4, 7] are normally used and correspond to [Skip, Low, Normal, High]

    file_progress (list of floats):
        The file progress (0.0 -> 1.0), empty list if n/a.
    """

    torrent = component.get("TorrentManager").torrents[torrent_id]
    files = torrent.get_files()
    priorities = torrent.get_file_priorities()
    progress = torrent.get_file_progress()

    if len(files) != len(priorities) != len(progress):
        # FIXME: Exception here
        pass

    priorities_to_assign = [PRIORITY.high] * top + [PRIORITY.normal] * second

    for priority in priorities_to_assign:
        for file in files:
            index = file.index

            # There is no point in changing priority for the file that is:
            #     • fully downloaded
            #     • set to be skipped
            #     • set to a higher priority
            if progress[index] < 1.0 and PRIORITY.skip < priorities[index] < priority:
                priorities[index] = priority

                # Each priority should be assigned only once
                continue

    torrent.set_file_priorities(priorities)


class PluginError(Exception):
    """Base class for plugin exceptions"""

    pass


class PluginDependencyError(PluginError):
    """Exception raised when plugin dependencies are not satisfied"""

    pass


class Core(CorePluginBase):
    def enable(self):
        log.info("*** Start Waterwheel plugin ***")

        self.core = component.get("Core")
        self.config = deluge.configmanager.ConfigManager(
            "waterwheel.conf", DEFAULT_PREFS
        )

        if "Label" not in component.get("CorePluginManager").get_enabled_plugins():
            raise PluginDependencyError(
                'Plugin "Label" is not enabled!'
                "\nThis plugin is required for Waterwheel to work."
                " Please enable Label in the preferences."
            )

        if self.core.get_config_value("pre_allocate_storage") is not True:
            # TODO: It is unclear whether this is actually needed or not
            raise PluginDependencyError(
                'Pre-allocation is not enabled!'
                '\nThis property is required for priorities to work.'
                ' Please enable pre-allocation in the preferences.'
            )

    def disable(self):
        pass

    @wrap_for_twisted
    async def update(self):
        # TODO
        # In order to configure update frequency,
        # 'CorePluginBase > PluginBase' should be modified;
        # PluginBase is based on Component,
        # so it should be easy to base this class directly on Component.
        # BTW, Component runs update() with twisted LoopingCall().
        #
        # I believe it is not needed, and 1 second is a good interval for now.

        configured_labels = self.config["labels"]

        # In UI there should be SessionProxy,
        #   but because all this happens inside the core,
        #   Core is used directly.
        # Important part here is get_torrents_status,
        #   which returns a {torrent_id: {key: value}} of torrents
        #   that were filtered by configured_labels;
        # FIXME: "name" is just a placeholder key, it is probably not needed at all
        labeled_torrents = await self.core.get_torrents_status(
            {"label": configured_labels}, "name"
        )

        # FIXME: This should probably work…
        for torrent_id in labeled_torrents:
            update_torrent_priorities(
                torrent_id,
                top=self.config["amount_top"],
                second=self.config["amount_second"],
            )

    @export
    def set_labels(self, labels):
        """Specifies labels that should be tracked"""

        # TODO
        pass

    @export
    def set_config(self, config):
        """Sets the config dictionary"""
        for key in config:
            self.config[key] = config[key]
        self.config.save()

    @export
    def get_config(self):
        """Returns the config dictionary"""
        return self.config.config
