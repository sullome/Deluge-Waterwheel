# Copyright (C) 2019 Constantine Farrahov <sullome.techie@gmail.com>
#
# Basic plugin template created by the Deluge Team.
#
# This file is part of Waterwheel and is licensed under GNU GPL 3.0, or later,
# with the additional special exception to link portions of this program with
# the OpenSSL library. See LICENSE for more details.
import sys
if sys.version_info < (3,):
    raise ImportError(
    """You are running Waterwheel on Python 2

Waterwheel are not compatible with Python 2, and you still 
ended up with this version installed.
That's unfortunate; sorry about that. It should not have happened.

Make sure you have pip >= 9.0 to avoid this kind 
of issue, as well as setuptools >= 24.2:

 $ pip install pip setuptools --upgrade

Your have to upgrade to Python 3.

It would be great if you can figure out how this version ended up being
installed, and try to check how to prevent that for future users.
""")

from deluge.plugins.init import PluginInitBase


class CorePlugin(PluginInitBase):
    def __init__(self, plugin_name):
        from .core import Core as PluginClass
        self._plugin_cls = PluginClass
        super(CorePlugin, self).__init__(plugin_name)


class Gtk3UIPlugin(PluginInitBase):
    def __init__(self, plugin_name):
        from .gtk3ui import Gtk3UI as PluginClass
        self._plugin_cls = PluginClass
        super(Gtk3UIPlugin, self).__init__(plugin_name)


class WebUIPlugin(PluginInitBase):
    def __init__(self, plugin_name):
        from .webui import WebUI as PluginClass
        self._plugin_cls = PluginClass
        super(WebUIPlugin, self).__init__(plugin_name)
