# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import pytest
from twisted.internet import defer
from twisted.trial import unittest

import deluge.component as component
from deluge.common import fsize, fspeed
from deluge.tests import common as tests_common
from deluge.tests.basetest import BaseTestCase
from deluge.ui.client import client
