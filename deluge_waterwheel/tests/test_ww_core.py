# Copyright (C) 2019 Constantine Farrahov <sullome.techie@gmail.com>
#
# This file is part of Waterwheel and is licensed under GNU GPL 3.0, or later,
# with the additional special exception to link portions of this program with
# the OpenSSL library. See LICENSE for more details.

import pytest
from twisted.internet import defer
from twisted.trial import unittest

import deluge.component as component
from deluge.common import fsize, fspeed
from deluge.tests import common as tests_common
from deluge.tests.basetest import BaseTestCase
from deluge.ui.client import client
