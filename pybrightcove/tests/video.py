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
Test the Video object.
"""

import unittest
from pybrightcove import PyBrightcoveError
from pybrightcove import Video

## NOTE: This are ids private to my account, if you want to run these tests
##       for yourself and have them pass, replace these with your own values.
TEST_VIDEO_ID = 11449913001
TEST_VIDEO_REF_ID = 'SN-47314834-100808-ATLGA-SV-404693da06d38.mp4'


class VideoTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_instantiate_new(self):
        self.fail()

    def test_instantiate_with_video_id(self):
        video = Video(id=TEST_VIDEO_ID)
        self.assertEquals(video.reference_id, TEST_VIDEO_REF_ID)

    def test_instantiate_with_reference_id(self):
        video = Video(reference_id=TEST_VIDEO_REF_ID)
        self.assertEquals(video.id, TEST_VIDEO_ID)

    def test_instantiate_with_invalid_parameters(self):
        self.fail()

    def test_save_new(self):
        self.fail()

    def test_save_update(self):
        self.fail()

    def test_save_update_add_additional_tags(self):
        self.fail()

    def test_get_upload_status(self):
        self.fail()

    def test_delete(self):
        self.fail()

    def test_share(self):
        self.fail()

    def test_add_image(self):
        self.fail()

    def test_update_image(self):
        self.fail()

    def test_find_by_tags(self):
        self.fail()

    def test_find_by_text(self):
        self.fail()

    def test_find_by_campaign(self):
        self.fail()

    def test_find_by_user(self):
        self.fail()

    def test_find_by_reference_ids(self):
        self.fail()

    def test_find_by_ids(self):
        self.fail()

    def test_find_all(self):
        videos = Video.find_all()
        for video in videos:
            self.assertEquals(type(video), Video)
        self.assertEquals(video.id not in (0, None), True)
        if not video:
            self.fail("Did not find any videos.")

    def test_find_related(self):
        self.fail()

    def test_invalid_name(self):
        try:
            video = Video(name="Name is too long"*10,
                          short_description="ok desc",
                          filename="somefile.mov")
        except PyBrightcoveError, e:
            self.assertEqual(e.message,
                "Video.name must be 60 characters or less.")
        else:
            self.fail("Expected PyBrightcoveError.")

    def test_invalid_short_description(self):
        try:
            video = Video(name="Name is too long",
                          short_description="ok desc"*100,
                          filename="somefile.mov")
        except PyBrightcoveError, e:
            self.assertEqual(e.message,
                "Video.short_description must be 250 characters or less.")
        else:
            self.fail("Expected PyBrightcoveError.")

    def test_invalid_long_description(self):
        try:
            video = Video(name="Name is too long",
                          short_description="ok desc",
                          filename="somefile.mov")
            video.long_description = "Very long"*5000
        except PyBrightcoveError, e:
            self.assertEqual(e.message,
                "Video.long_description must be 5000 characters or less.")
        else:
            self.fail("Expected PyBrightcoveError.")

    def test_invalid_reference_id(self):
        try:
            video = Video(name="Name is too long",
                          short_description="ok desc",
                          filename="somefile.mov")
            video.reference_id = "long ref id"*100
        except PyBrightcoveError, e:
            self.assertEqual(e.message,
                "Video.reference_id must be 150 characters or less.")
        else:
            self.fail("Expected PyBrightcoveError.")

    def test_invalid_economics(self):
        try:
            video = Video(name="Name is too long",
                          short_description="ok desc",
                          filename="somefile.mov")
            video.economics = "The Keynesian view is Wrong"
        except PyBrightcoveError, e:
            err = "Video.economics must be either EconomicsEnum.FREE or"
            err += " EconomicsEnum.AD_SUPPORTED"
            self.assertEqual(e.message, err)
        else:
            self.fail("Expected PyBrightcoveError.")

    def test_invalid_item_state(self):
        try:
            video = Video(name="Name is too long",
                          short_description="ok desc",
                          filename="somefile.mov")
            video.item_state = "Invalid"
        except PyBrightcoveError, e:
            err = "Video.item_state must be either ItemStateEnum.ACTIVE or "
            err += "or ItemStateEnum.INACTIVE"
            self.assertEqual(e.message, err)
        else:
            self.fail("Expected PyBrightcoveError.")

    def test_invalid_video_full_length(self):
        try:
            video = Video(name="Name is too long",
                          short_description="ok desc",
                          filename="somefile.mov")
            video.video_full_length = 10
        except PyBrightcoveError, e:
            self.assertEqual(e.message,
                "Video.video_full_length must be of type Rendition")
        else:
            self.fail("Expected PyBrightcoveError.")
