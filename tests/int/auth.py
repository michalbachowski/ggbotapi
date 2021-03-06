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
__date__ = "$2011-01-23 14:02:16$"
import unittest

from base import BaseTestCase


class AuthenticationTestCase(BaseTestCase):
    """
    Test cases for Authentication class
    """

    incorrectBotId = 123
    incorrectLogin = 'error'
    incorrectPass = 'error_pass'

    def setUp(self):
        BaseTestCase.setUp(self)

    def testCorrectAuthentication(self):
        """Tests response to correct authentication"""
        self.assertTrue(self.auth.is_valid())


if __name__ == "__main__":
    unittest.main() # run all tests
