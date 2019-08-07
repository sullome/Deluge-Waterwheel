# Copyright (C) 2019 Constantine Farrahov <sullome.techie@gmail.com>
#
# This file is part of Waterwheel and is licensed under GNU GPL 3.0, or later,
# with the additional special exception to link portions of this program with
# the OpenSSL library. See LICENSE for more details.

import pytest
import pytest_twisted
import warnings

import deluge.component as component
from deluge.ui.client import client as standalone_client


@pytest.fixture
async def started_deluge_client(tmpdir):
    # Set Up
    if len(component._ComponentRegistry.components) != 0:
        warnings.warn(
            'The component._ComponentRegistry.components'
            ' is not empty on test setup.\n'
            'This is probably caused by another test'
            ' that did not clean up after finishing!:'
            f' {component._ComponentRegistry.components}'
        )

    deluge.configmanager.set_config_dir(tmpdir)
    standalone_client.start_standalone()

    await component.start()
    yield standalone_client

    # Tear Down
    standalone_client.stop_standalone()

    await component.shutdown()
    component._ComponentRegistry.components.clear()
    component._ComponentRegistry.dependents.clear()


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
async def test_enabled_with_label_and_preallocation(started_deluge_client):
    await started_deluge_client.core.enable_plugin('Label')
    started_deluge_client.core.set_config({'pre_allocate_storage': True})
    enabled = await started_deluge_client.core.enable_plugin('Waterwheel')
    assert enabled

# @pytest_twisted.ensureDeferred
# async def test_good(deluge_client_started):
#     # res = await something()
#     # assert res == good
#     pass

# TODO: remove this reference material
# class WaterwheelTestCase(unittest.TestCase):
#     """
#     this is from deluge.tests BaseTestCase
#
#     This is the base class that should be used for all test classes
#     that create classes that inherit from deluge.component.Component. It
#     ensures that the component registry has been cleaned up when tests
#     have finished.
#
#     """
#
#     def setUp(self):  # NOQA: N803
#
#         if len(component._ComponentRegistry.components) != 0:
#             warnings.warn(
#                 'The component._ComponentRegistry.components is not empty on test setup.\n'
#                 'This is probably caused by another test that did not clean up after finishing!: %s'
#                 % component._ComponentRegistry.components
#             )
#         d = maybeDeferred(self.set_up)
#
#         def on_setup_error(error):
#             warnings.warn('Error caught in test setup!\n%s' % error.getTraceback())
#             self.fail()
#
#         return d.addErrback(on_setup_error)
#
#     def tearDown(self):  # NOQA: N803
#         d = maybeDeferred(self.tear_down)
#
#         def on_teardown_failed(error):
#             warnings.warn('Error caught in test teardown!\n%s' % error.getTraceback())
#             self.fail()
#
#         def on_teardown_complete(result):
#             component._ComponentRegistry.components.clear()
#             component._ComponentRegistry.dependents.clear()
#
#         return d.addCallbacks(on_teardown_complete, on_teardown_failed)
#
#     def set_up(self, tmpdir):
#         # defer.setDebugging(True)
#         deluge.configmanager.set_config_dir(tmpdir)
#         client.start_standalone()
#         client.core.enable_plugin('Waterwheel')
#         return component.start()
#
#     def tear_down(self):
#         client.stop_standalone()
#         return component.shutdown()
#
#     @pytest_twisted.inlineCallbacks
#     def test_sometest(self):
#         pass
