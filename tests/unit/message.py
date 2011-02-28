#!/usr/bin/env python
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
__date__ = "$2011-01-23 14:02:16$"

import base64

import unittest
from mockito import *

from ggbotapi.lib_2_1.message import MessageBuilder

from base import BaseTestCase


class MessageBuilderTestCase(BaseTestCase):
    """
    Test cases for MessageBuilder class
    """
    correctLogin = '1'
    correctPass = 'ok_pass'

    incorrectLogin = 'error'
    incorrectPass = 'error_pass'

    def setUp(self):
        BaseTestCase.setUp(self)
        self.mb = MessageBuilder()

    def compare_to(self, expected):
        self.assertEqual(
            base64.b64encode(self.mb.build()),
            expected)

    def testEmptyOnInitialization(self):
        assert self.mb.txt == ''
        assert self.mb.html == ''
        assert self.mb.formatting == ''
        assert self.mb.img is None
        assert self.mb.response is None

    def testPlainMessage(self):
        self.mb.add_text('plain text')
        self.compare_to('UwAAAAsAAAAAAAAAAAAAADxzcGFuIHN0eWxlPSJjb2xvcjojM' + \
            'DAwMDAwOyBmb250LWZhbWlseTonTVMgU2hlbGwgRGxnIDInOyBmb250LXNpem' + \
            'U6OXB0OyAiPjwvc3Bhbj4AcGxhaW4gdGV4dAA=')

    def testHtmlMessage(self):
        self.mb.add_html('<b>html content</b>')
        self.compare_to('ZgAAAAEAAAAAAAAAAAAAADxzcGFuIHN0eWxlPSJjb2xvcjojM' + \
            'DAwMDAwOyBmb250LWZhbWlseTonTVMgU2hlbGwgRGxnIDInOyBmb250LXNpem' + \
            'U6OXB0OyAiPjxiPmh0bWwgY29udGVudDwvYj48L3NwYW4+AAA=')

if __name__ == "__main__":
    unittest.main() # run all tests
