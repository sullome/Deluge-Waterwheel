# Copyright (C) 2019 Constantine Farrahov <sullome.techie@gmail.com>
#
# This file is part of Waterwheel and is licensed under GNU GPL 3.0, or later,
# with the additional special exception to link portions of this program with
# the OpenSSL library. See LICENSE for more details.

import pytest
import pytest_twisted
import warnings

from deluge import component
from deluge import configmanager
from deluge.ui.client import Client
from deluge.i18n import setup_translation

# install python3-pytest_twisted
# pip3 install deluge
# install rb_libtorrent-python3


@pytest.fixture
def started_deluge_client(tmpdir):
    # Set Up
    standalone_client = Client()

    if len(component._ComponentRegistry.components) != 0:
        warnings.warn(
            "The component._ComponentRegistry.components"
            " is not empty on test setup.\n"
            "This is probably caused by another test"
            " that did not clean up after finishing!:"
            f" {component._ComponentRegistry.components}"
        )

    configmanager.set_config_dir(tmpdir)
    standalone_client.start_standalone()

    pytest_twisted.blockon(component.start())
    yield standalone_client

    # Tear Down
    pytest_twisted.blockon(standalone_client.disconnect())
    pytest_twisted.blockon(component.shutdown())

    # There can be KeyErrors after pytest run about RPCServer
    # This errors are happening because of the next clear()
    #
    # It is so because plugins objects (that are based on CorePluginBase)
    # are still stored inside RPCServer's factory.methods
    # When RPCServer object is destroyed, it's dicts are cleared as well
    # That's when CorePluginBase.__del__ is called
    # And it tries to obtain RPCServer object from a list of components,
    # but this object already excluded from the list, so it fails to
    # deregister itself from RPCServer's dicts.
    #
    # Moreover, calling RPCServer's deregister_object is of no use, because:
    # def deregister_object(self, obj):
    #     """
    #     Deregisters an objects exported rpc methods.
    #
    #     :param obj: the object that was previously registered
    #
    #     """
    # >       for key, value in self.factory.methods.items():
    #             if value.__self__ == obj:
    #                 del self.factory.methods[key]
    # E       RuntimeError: dictionary changed size during iteration

    component._ComponentRegistry.components.clear()
    component._ComponentRegistry.dependents.clear()


@pytest.fixture
def enabled_plugins(started_deluge_client):
    started_deluge_client.core.set_config({"pre_allocate_storage": True})
    pytest_twisted.blockon(started_deluge_client.core.enable_plugin("Label"))
    pytest_twisted.blockon(started_deluge_client.core.enable_plugin("Waterwheel"))
    setup_translation()

    yield

    label_plugin = component.get("CorePlugin.Label")
    for label in label_plugin.get_labels():
        label_plugin.remove(label)


@pytest.fixture
def added_torrent(enabled_plugins):
    torrent_file = "data/test.torrent"
    torrent_manager = component.get("TorrentManager")
    torrent_info = torrent_manager.get_torrent_info_from_file("data/test.torrent")
    torrent_manager.add(torrent_info=torrent_info, filename=torrent_file)

    yield


@pytest_twisted.ensureDeferred
async def test_plugin_is_known(started_deluge_client, caplog):
    await started_deluge_client.core.enable_plugin("Waterwheel")
    assert "Cannot enable non-existant plugin" not in caplog.text


@pytest_twisted.ensureDeferred
async def test_not_enabled_without_label(started_deluge_client):
    enabled = await started_deluge_client.core.enable_plugin("Waterwheel")
    assert not enabled


@pytest_twisted.ensureDeferred
async def test_label_can_be_enabled(started_deluge_client):
    enabled = await started_deluge_client.core.enable_plugin("Label")
    assert enabled


@pytest_twisted.ensureDeferred
async def test_not_enabled_without_preallocation(started_deluge_client):
    await started_deluge_client.core.enable_plugin("Label")
    started_deluge_client.core.set_config({"pre_allocate_storage": False})
    enabled = await started_deluge_client.core.enable_plugin("Waterwheel")
    assert not enabled


@pytest_twisted.ensureDeferred
async def test_enabled_with_label_and_preallocation(started_deluge_client):
    started_deluge_client.core.set_config({"pre_allocate_storage": True})
    await started_deluge_client.core.enable_plugin("Label")
    enabled = await started_deluge_client.core.enable_plugin("Waterwheel")
    assert enabled


@pytest_twisted.ensureDeferred
async def test_label_added_correctly(enabled_plugins):
    ww = component.get("CorePlugin.Waterwheel")
    label_plugin = component.get("CorePlugin.Label")
    assert label_plugin.get_labels() == []

    known_labels = {"sequential", "one-by-one", "auto-priority"}
    for label in known_labels:
        label_plugin.add(label)

    new_label = known_labels.pop()
    ww.track_label(new_label)

    needed_labels = {new_label}
    assert needed_labels == ww._tracked_labels


@pytest_twisted.ensureDeferred
async def test_label_removed_correctly(enabled_plugins):
    ww = component.get("CorePlugin.Waterwheel")
    label_plugin = component.get("CorePlugin.Label")
    assert label_plugin.get_labels() == []

    known_labels = {"sequential", "one-by-one", "auto-priority"}
    for label in known_labels:
        label_plugin.add(label)
        ww.track_label(label)

    needed_labels = known_labels
    wrong_label = needed_labels.pop()
    ww.untrack_label(wrong_label)
    assert needed_labels == ww._tracked_labels


@pytest_twisted.ensureDeferred
async def test_unknown_label_not_added(enabled_plugins):
    ww = component.get("CorePlugin.Waterwheel")
    label_plugin = component.get("CorePlugin.Label")
    assert label_plugin.get_labels() == []

    known_labels = {"sequential", "one-by-one", "auto-priority"}
    test_label = known_labels.pop()

    for label in known_labels:
        label_plugin.add(label)
        ww.track_label(label)

    with pytest.raises(KeyError):
        ww.track_label(test_label)
