#! /usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2009 Michał Bachowski
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
__author__ = "mib"
__date__ = "$2011-01-23 14:57:14$"

import unittest
from mockito import *

from ggbotapi.lib_2_1.authentication import Authentication
from ggbotapi.lib_2_1.botmaster import Client, CommunicationAdapter


class BaseTestCase(unittest.TestCase):
    """
    Base class for test cases that uses Mocks
    """

    def setUp(self):
        self.botmaster = mock(Client)
        self.adapter = mock(CommunicationAdapter)
        self.auth = mock(Authentication)
        when(self.botmaster).auth().thenReturn(self.auth)
        when(self.botmaster).adapter().thenReturn(self.adapter)

