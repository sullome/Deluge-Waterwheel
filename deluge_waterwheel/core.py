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

import deluge.configmanager
from deluge.core.rpcserver import export
from deluge.plugins.pluginbase import CorePluginBase

log = logging.getLogger(__name__)

DEFAULT_PREFS = {
    'test': 'NiNiNi'
}


class Core(CorePluginBase):
    def enable(self):
        self.config = deluge.configmanager.ConfigManager(
            'waterwheel.conf', DEFAULT_PREFS)

    def disable(self):
        pass

    def update(self):
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
