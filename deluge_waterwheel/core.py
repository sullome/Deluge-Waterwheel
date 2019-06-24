# -*- coding: utf-8 -*-
# Copyright (C) 2019 Constantine Farrahov <sullome.techie@gmail.com>
#
# Basic plugin template created by the Deluge Team.
#
# This file is part of Waterwheel and is licensed under GNU GPL 3.0, or later,
# with the additional special exception to link portions of this program with
# the OpenSSL library. See LICENSE for more details.
from __future__ import unicode_literals

import logging

import six

# noinspection PyPackageRequirements
import deluge.configmanager
# noinspection PyPackageRequirements
from deluge import component
# noinspection PyPackageRequirements
from deluge.core.rpcserver import export
# noinspection PyPackageRequirements
from deluge.plugins.pluginbase import CorePluginBase

log = logging.getLogger(__name__)

DEFAULT_PREFS = {
    "order": "alphabetical",
    "labels": [],
    "amount_top": 1,
    "amount_second": 2,
}


def get_torrent_ids_by_label(labeled_torrents, required_label):
    """Extracts a list of torrent IDs from dictionary {torrent_id:label_id} by label."""

    result = []

    for torrent_id, label_id in labeled_torrents.items():
        if label_id == required_label:
            result.append(torrent_id)

    return result


def update_torrent_priorities(torrent_id, top=1, second=1):
    """Adjust files priorities for a specified torrent"""

    torrent = component.get("TorrentManager").torrents[torrent_id]
    # TODO


class Core(CorePluginBase):
    def enable(self):
        log.info("*** Start Waterwheel plugin ***")
        self.config = deluge.configmanager.ConfigManager(
            "waterwheel.conf", DEFAULT_PREFS
        )

        # TODO
        # Plugin "Labels" is required

        # TODO
        # It is possible that priorities does not work without pre-allocation.
        # If it is true, than check if pre-allocation is enabled should be made.

    def disable(self):
        pass

    def update(self):
        # TODO
        # In order to configure update frequency,
        # 'CorePluginBase > PluginBase' should be modified;
        # PluginBase is based on Component,
        # so it should be easy to base this class directly on Component.
        # BTW, Component runs update() with twisted LoopingCall().
        #
        # I believe it is not needed, and 1 second is a good interval for now.

        for label_id in self.config["labels"]:
            torrent_ids = get_torrent_ids_by_label(TODO, label_id)

            known_torrents = []  # TODO
            new_torrents = []  # TODO

            # FIXME
            known_torrents = torrent_ids

            for torrent_id in new_torrents:
                update_torrent_priorities(
                    torrent_id,
                    top=self.config["amount_top"],
                    second=self.config["amount_second"],
                )
                known_torrents.append(torrent_id)

            for torrent_id in known_torrents:
                # TODO
                # Check that set interval is already passed
                # It is safe to assume that each time this function is called,
                # 1 second is passed.

                # TODO
                # Update priorities if it is time to do so
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
