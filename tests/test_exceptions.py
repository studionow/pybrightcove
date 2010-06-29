# Copyright (c) 2010 StudioNow, Inc <patrick@studionow.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import pickle
import unittest

import pybrightcove


class BrightcoveErrorPickleTest(unittest.TestCase):

    def test_call_timeout_error_pickle(self):
        e = pybrightcove.exceptions.CallTimeoutError()
        se = pickle.dumps(e)
        ne = pickle.loads(se)
        self.assertEquals(str(ne), str(e))


class PyBrightcoveErrorPickleTest(unittest.TestCase):

    def test_pybrightcove_error_pickle(self):
        e = pybrightcove.exceptions.PyBrightcoveError("Test Error")
        se = pickle.dumps(e)
        ne = pickle.loads(se)
        self.assertEquals(str(ne), str(e))

    def test_improperly_configured_error_pickle(self):
        e = pybrightcove.exceptions.ImproperlyConfiguredError("Test Error")
        se = pickle.dumps(e)
        ne = pickle.loads(se)
        self.assertEquals(str(ne), str(e))

    def test_no_data_found_error_pickle(self):
        e = pybrightcove.exceptions.NoDataFoundError("Test Error")
        se = pickle.dumps(e)
        ne = pickle.loads(se)
        self.assertEquals(str(ne), str(e))

    def test_no_data_found_error_no_message_pickle(self):
        e = pybrightcove.exceptions.NoDataFoundError()
        se = pickle.dumps(e)
        ne = pickle.loads(se)
        self.assertEquals(str(ne), str(e))

