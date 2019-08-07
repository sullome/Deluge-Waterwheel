# Copyright (C) 2019 Constantine Farrahov <sullome.techie@gmail.com>
#
# This file is part of Waterwheel and is licensed under GNU GPL 3.0, or later,
# with the additional special exception to link portions of this program with
# the OpenSSL library. See LICENSE for more details.

import pytest
import pytest_twisted
import warnings

import deluge.component as component
from deluge.ui.client import client


@pytest.fixture
async def deluge_client_started(tmpdir):
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
    client.start_standalone()
    client.core.enable_plugin('Waterwheel')

    await component.start()
    yield

    # Tear Down
    client.stop_standalone()

    await component.shutdown()
    component._ComponentRegistry.components.clear()
    component._ComponentRegistry.dependents.clear()


@pytest_twisted.ensureDeferred
async def test_good(deluge_client_started):
    # res = await something()
    # assert res == good
    pass

# class WaterwheelTestCase(unittest.TestCase):
#     """
#     TODO: this is from deluge.tests BaseTestCase - check if needed at all
#
#     This is the base class that should be used for all test classes
#     that create classes that inherit from deluge.component.Component. It
#     ensures that the component registry has been cleaned up when tests
#     have finished.
#
#     """
#
#     # TODO: this is from deluge.tests BaseTestCase - check if needed at all
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
#     # TODO: this is from deluge.tests BaseTestCase - check if needed at all
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
