#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2011 Michał Bachowski
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
__date__ = "$2011-03-23 14:02:16$"

import base64

import unittest

from ggbotapi.lib_2_1.authentication import *
from ggbotapi.lib_2_1.message import MessageBuilder
from ggbotapi.lib_2_1.botmaster import *

from base import BaseTestCase


class BotmasterTestCase(BaseTestCase):
    """
    Test cases for Botmaster module
    """

    def setUp(self):
        BaseTestCase.setUp(self)

    def test_send(self):
        message = MessageBuilder()
        message.add_text('tests')
        self.botmaster.send(message,[8714989],False)

    def test_set_status(self):
        message = MessageBuilder()
        message.add_text('tests')
        self.botmaster.set_status(Status(2),'testing...')


if __name__ == "__main__":
    unittest.main() # run all tests
