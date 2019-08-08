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

# install python3-pytest_twisted
# pip3 install deluge
# install rb_libtorrent-python3


@pytest.fixture
def started_deluge_client(tmpdir):
    # Set Up
    standalone_client = Client()

    if len(component._ComponentRegistry.components) != 0:
        warnings.warn(
            'The component._ComponentRegistry.components'
            ' is not empty on test setup.\n'
            'This is probably caused by another test'
            ' that did not clean up after finishing!:'
            f' {component._ComponentRegistry.components}'
        )

    configmanager.set_config_dir(tmpdir)
    standalone_client.start_standalone()

    pytest_twisted.blockon(component.start())
    yield standalone_client

    # Tear Down
    standalone_client.stop_standalone()

    pytest_twisted.blockon(component.shutdown())
    # There can be KeyErrors after pytest run about RPCServer
    # This errors are happening because of this shutdown.

    component._ComponentRegistry.components.clear()
    component._ComponentRegistry.dependents.clear()


@pytest_twisted.ensureDeferred
async def test_plugin_is_known(started_deluge_client, caplog):
    await started_deluge_client.core.enable_plugin('Waterwheel')
    assert "Cannot enable non-existant plugin" not in caplog.text


@pytest_twisted.ensureDeferred
async def test_not_enabled_without_label(started_deluge_client):
    enabled = await started_deluge_client.core.enable_plugin('Waterwheel')
    assert not enabled


@pytest_twisted.ensureDeferred
async def test_not_enabled_without_preallocation(started_deluge_client):
    started_deluge_client.core.set_config({'pre_allocate_storage': False})
    enabled = await started_deluge_client.core.enable_plugin('Waterwheel')
    assert not enabled


@pytest_twisted.ensureDeferred
async def test_label_can_be_enabled(started_deluge_client):
    enabled = await started_deluge_client.core.enable_plugin('Label')
    assert enabled


@pytest_twisted.ensureDeferred
async def test_enabled_with_label_and_preallocation(started_deluge_client):
    await started_deluge_client.core.enable_plugin('Label')
    started_deluge_client.core.set_config({'pre_allocate_storage': True})
    enabled = await started_deluge_client.core.enable_plugin('Waterwheel')
    assert enabled
