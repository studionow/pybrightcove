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
import uuid
from datetime import datetime, timedelta
from pybrightcove import PyBrightcoveError
from pybrightcove import Video, Image
from pybrightcove import UploadStatusEnum, ImageTypeEnum, FilterChoicesEnum

## NOTE: This are ids private to my account, if you want to run these tests
##       for yourself and have them pass, replace these with your own values.
TEST_VIDEO_ID = 11449913001
TEST_VIDEO_IDS = [TEST_VIDEO_ID, 24780403001, 24780402001]
TEST_VIDEO_REF_ID = 'SN-47314834-100808-ATLGA-SV-404693da06d38.mp4'
TEST_VIDEO_REF_IDS = ['unittest-1', 'unittest-2', TEST_VIDEO_REF_ID]

## TODO: Figure out a good way to mock the Connection object


class VideoTest(unittest.TestCase):

    def setUp(self):
        self.test_uuid = str(uuid.uuid4())

    def test_instantiate_new(self):
        video = Video(filename='/mnt/local/movie.mov', name='My Movie',
            short_description='This is my movie.')
        self.assertEquals(video.id, None)
        self.assertEquals(video.name, 'My Movie')
        self.assertEquals(video.short_description, 'This is my movie.')
        self.assertEquals(video.long_description, None)
        self.assertEquals(len(video.tags), 0)

    def test_instantiate_with_video_id(self):
        video = Video(id=TEST_VIDEO_ID)
        self.assertEquals(video.reference_id, TEST_VIDEO_REF_ID)

    def test_instantiate_with_reference_id(self):
        video = Video(reference_id=TEST_VIDEO_REF_ID)
        self.assertEquals(video.id, TEST_VIDEO_ID)

    def test_instantiate_with_invalid_parameters(self):
        try:
            video = Video(name='This is wrong.')
            self.fail('Should not have worked, but rather raised an error.')
            video = Video()
            self.fail('Should not have worked, but rather raised an error.')
        except PyBrightcoveError, e:
            self.assertEquals(e.message, 'Invalid parameters for Video.')
        except Exception, e:
            self.fail('Should have thrown a PyBrightcoveError exception.')

    def test_save_new(self):
        video = Video(filename='bears.mov', name='The Bears',
            short_description='Opening roll for an exciting soccer match.')
        video.tags.append('unittest')
        video.save()
        self.assertEquals(video.id not in (0, '', None), True)

    def test_save_update(self):
        video = Video(id=TEST_VIDEO_ID)
        video.tags.append('tag-%s' % self.test_uuid)
        video.tags.append('unittest')
        lmd = video.last_modified_date
        video.save()
        self.assertEquals(video.reference_id, TEST_VIDEO_REF_ID)
        self.assertNotEquals(video.last_modified_date, lmd)

    def test_get_upload_status(self):
        video = Video(filename='bears.mov', name='STATUS TEST The Bears',
            short_description='Opening roll for an exciting soccer match.')
        video.tags.append('unittest')
        video.save()
        status = video.get_upload_status()
        self.assertEquals(status, UploadStatusEnum.PROCESSING)

    def test_delete(self):
        video = Video(filename='bears.mov', name='DELETE TEST The Bears',
            short_description='Opening roll for an exciting soccer match.')
        video.tags.append('unittest')
        video.save()
        video.delete()
        self.assertEquals(video.id, None)

    def test_share(self):
        self.fail()

    def test_set_image(self):
        video = Video(id=TEST_VIDEO_ID)
        self.assertEquals(video.image, None)
        image = Image(reference_id="img-%s" % self.test_uuid,
                      display_name="My Test Image",
                      type=ImageTypeEnum.VIDEO_STILL)
        video.set_image(image, filename='bears.png')
        self.assertEquals(video.image != None, True)
        self.assertEquals(video.image.id > 0, True)

    def test_find_by_tags(self):
        videos = Video.find_by_tags(and_tags=['unittest', ])
        for video in videos:
            self.assertEquals(type(video), Video)
            self.assertEquals('unittest' in video.tags, True)

    def test_find_by_text(self):
        videos = Video.find_by_text('bear')
        for video in videos:
            self.assertEquals(type(video), Video)

    def test_find_by_campaign(self):
        videos = Video.find_by_campaign(988756758)
        for video in videos:
            self.assertEquals(type(video), Video)

    def test_find_by_user(self):
        videos = Video.find_by_user(12312431)
        for video in videos:
            self.assertEquals(type(video), Video)

    def test_find_by_reference_ids(self):
        videos = Video.find_by_reference_ids(TEST_VIDEO_REF_IDS)
        for video in videos:
            self.assertEquals(video.reference_id in TEST_VIDEO_REF_IDS, True)

    def test_find_by_ids(self):
        videos = Video.find_by_ids(TEST_VIDEO_IDS)
        for video in videos:
            self.assertEquals(video.id in TEST_VIDEO_IDS, True)

    def test_find_all(self):
        videos = Video.find_all()
        for video in videos:
            self.assertEquals(type(video), Video)
        self.assertEquals(video.id not in (0, None), True)
        if not video:
            self.fail("Did not find any videos.")

    def test_find_related(self):
        video = Video(id=TEST_VIDEO_IDS[1])
        for related_video in video.find_related():
            self.assertEquals(type(related_video), Video)
        self.assertEquals(related_video.id > 0, True)

    def test_find_modified_unfiltered(self):
        yesterday = datetime.now() - timedelta(days=1)
        videos = Video.find_modified(since=yesterday)
        for video in videos:
            self.assertEquals(type(video), Video)
        self.assertEquals(video.id > 0, True)

    def test_find_modified_filtered(self):
        yesterday = datetime.now() - timedelta(days=1)
        filters = [FilterChoicesEnum.PLAYABLE, FilterChoicesEnum.DELETED]
        videos = Video.find_modified(since=yesterday, filter_list=filters)
        for video in videos:
            self.assertEquals(type(video), Video)
        self.assertEquals(video.id > 0, True)

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
            err += "ItemStateEnum.INACTIVE"
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
