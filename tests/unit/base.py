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
import psycopg2
from pigeon.api.db import Connection, Cursor
from mockito import *


class BaseMockTestCase(unittest.TestCase):
    """
    Base class for test cases that uses Mocks
    """

    def setUp(self):
        self._db = mock(Connection)
        self._cursor = mock(Cursor)
        when(self._db).cursor().thenReturn(self._cursor)

    def checkDbCall(self, thenReturn, method, procedure, params):
        try:
            # stub
            when(self._cursor).fetchone().thenReturn(thenReturn)
            # test
            method(self)
            # verify
            inorder.verify(self._cursor).callproc(procedure,params)
            inorder.verify(self._cursor).fetchone()
        except VerificationError, e:
            self.fail(e.message)


class BaseTestCase(unittest.TestCase):
    """
    Base class for test cases
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

