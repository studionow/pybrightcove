# Copyright (c) 2009 StudioNow, Inc <patrick@studionow.com>
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

"""
Test the Media API Connection and Methods:
- Connection.find_video_by_id
- Connection.update_video
"""

import unittest
import uuid
import datetime
from pybrightcove.video import Video
from pybrightcove.connection import Connection

## Note: This is a video in my account for these tests to work for you, change
##       to a video id your account has rights to manipulate.
TEST_VIDEO_ID = 11449913001L
CREATION_DATE = datetime.datetime(2009, 2, 11, 13, 38, 21, 372000)


class ConnectionTest(unittest.TestCase):

    def setUp(self):
        self.test_video_id = TEST_VIDEO_ID
        self.test_creation = CREATION_DATE
        self.unique_name = str(uuid.uuid4())
        self.connection = Connection()

    def test_find_video_by_id(self):
        video = self.connection.find_video_by_id(self.test_video_id)
        self.assertEqual(video.creationDate, self.test_creation)

    def test_update_video(self):
        video = Video({'id': self.test_video_id})
        video.name = self.unique_name
        video.tags = ['tag-%s' % self.unique_name, ]
        new_video = self.connection.update_video(video)
        self.assertEqual(new_video.name, self.unique_name)
        self.assertEqual(new_video.tags, ['tag-%s' % self.unique_name, ])
