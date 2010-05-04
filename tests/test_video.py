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
import pybrightcove
import mock
## NOTE: This are ids private to my account, if you want to run these tests
##       for yourself and have them pass, replace these with your own values.
TEST_VIDEO_ID = 11449913001
TEST_VIDEO_IDS = [TEST_VIDEO_ID, 24780403001, 24780402001]
TEST_VIDEO_REF_ID = 'SN-47314834-100808-ATLGA-SV-404693da06d38.mp4'
TEST_VIDEO_REF_IDS = ['unittest-1', 'unittest-2', TEST_VIDEO_REF_ID]
VIDEO_DATA = {
    'creationDate': 1272312315.0,
    'economics': pybrightcove.enums.EconomicsEnum.FREE,
    'id': TEST_VIDEO_ID,
    'lastModifiedDate': 1272312315.0,
    'length': 55,
    'linkText': "the link text",
    'linkURL': "the link url",
    'longDescription': "A really long description.",
    'name': "My Video",
    'playsTotal': 100,
    'playsTrailingWeek': 40,
    'publishedDate': 1272312315.0,
    'startDate': 1272312315.0,
    'endDate': 1272312315.0,
    'referenceId': TEST_VIDEO_REF_ID,
    'shortDescription': "this is a short description",
    'tags': ['tag1', 'tag2', 'tag3'],
    'thumbnailURL': 'another_something_url',
    'videoStillURL': 'something_url'
}
IMAGE_DATA = {
    'id': 'image id',
    'referenceId': 'reference id',
    'type': 'image type',
    'displayName': 'display_name',
    'remoteUrl': 'image url'
}

class RenditionTest(unittest.TestCase):

    def test_invalid_size_type(self):
        try:
            r = pybrightcove.video.Rendition()
            r.remote_url = 'http://my.sample.com/flash.flv'
            r.size = 'invalid'
            r.video_duration = 600000
            r.video_codec = pybrightcove.enums.VideoCodecEnum.H264
            self.fail("Should have raised a PyBrightcoveError")
        except pybrightcove.exceptions.PyBrightcoveError, e:
            self.assertEquals(str(e), "Rendition.size must be the number of bytes as an integer or long.")

    def test_invalid_duration_type(self):
        try:
            r = pybrightcove.video.Rendition()
            r.remote_url = 'http://my.sample.com/flash.flv'
            r.size = 10000000
            r.video_duration = "invalid"
            r.video_codec = pybrightcove.enums.VideoCodecEnum.H264
            self.fail("Should have raised a PyBrightcoveError")
        except pybrightcove.exceptions.PyBrightcoveError, e:
            self.assertEquals(str(e), "Rendition.video_duration must be the duration in milliseconds as an integer or long.")

    def test_invalid_codec_type(self):
        try:
            r = pybrightcove.video.Rendition()
            r.remote_url = 'http://my.sample.com/flash.flv'
            r.size = 10000000
            r.video_duration = 600000
            r.video_codec = "INVALID"
            self.fail("Should have raised a PyBrightcoveError")
        except pybrightcove.exceptions.PyBrightcoveError, e:
            self.assertEquals(str(e), "Rendition.video_codec must be SORENSON, ON2, or H264.")

    def test_serialization(self):
        r = pybrightcove.video.Rendition()
        r.remote_url = 'http://my.sample.com/flash.flv'
        r.size = 10000000
        r.video_duration = 600000
        r.video_codec = pybrightcove.enums.VideoCodecEnum.H264
        data = r.to_dict()
        self.assertTrue('remoteUrl' in data.keys())
        self.assertTrue('size' in data.keys())
        self.assertTrue('videoDuration' in data.keys())
        self.assertTrue('videoCodec' in data.keys())
        self.assertEquals(data['remoteUrl'], 'http://my.sample.com/flash.flv')
        self.assertEquals(data['size'], 10000000)
        self.assertEquals(data['videoDuration'], 600000)
        self.assertEquals(data['videoCodec'], pybrightcove.enums.VideoCodecEnum.H264)
        self.assertEquals(len(data.keys()), 4)


class VideoTest(unittest.TestCase):

    def setUp(self):
        self.test_uuid = str(uuid.uuid4())

    def _get_list_mock(self, ConnectionMock):
        m = ConnectionMock()
        c = mock.Mock()
        c.items = [mock.Mock(), mock.Mock()]
        c.total_count = 2
        c.page_size = 0
        m.get_list.return_value = c
        return m

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_instantiate_new(self, ConnectionMock):
        m = ConnectionMock()
        video = pybrightcove.video.Video(filename='/mnt/local/movie.mov', name='My Movie',
            short_description='This is my movie.')
        self.assertEquals(video.id, None)
        self.assertEquals(video.name, 'My Movie')
        self.assertEquals(video.short_description, 'This is my movie.')
        self.assertEquals(video.long_description, None)
        self.assertEquals(len(video.tags), 0)

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_instantiate_with_video_id(self, ConnectionMock):
        m = ConnectionMock()
        m.get_item.return_value = VIDEO_DATA
        video = pybrightcove.video.Video(id=TEST_VIDEO_ID)
        self.assertEquals(video.reference_id, TEST_VIDEO_REF_ID)
        self.assertEquals(m.method_calls[0][0], 'get_item')
        self.assertEquals(m.method_calls[0][1][0], 'find_video_by_id')
        self.assertEquals(m.method_calls[0][2]['video_id'], TEST_VIDEO_ID)

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_instantiate_with_reference_id(self, ConnectionMock):
        m = ConnectionMock()
        m.get_item.return_value = VIDEO_DATA
        video = pybrightcove.video.Video(reference_id=TEST_VIDEO_REF_ID)
        self.assertEquals(video.id, TEST_VIDEO_ID)
        self.assertEquals(m.method_calls[0][0], 'get_item')
        self.assertEquals(m.method_calls[0][1][0], 'find_video_by_reference_id')
        self.assertEquals(m.method_calls[0][2]['reference_id'], TEST_VIDEO_REF_ID)

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_instantiate_with_invalid_parameters(self, ConnectionMock):
        try:
            video = pybrightcove.video.Video(name='This is wrong.')
            self.fail('Should not have worked, but rather raised an error.')
            video = pybrightcove.video.Video()
            self.fail('Should not have worked, but rather raised an error.')
        except pybrightcove.exceptions.PyBrightcoveError, e:
            self.assertEquals(str(e), 'Invalid parameters for Video.')
        except Exception, e:
            self.fail('Should have thrown a pybrightcove.exceptions.PyBrightcoveError exception.')

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_save_new(self, ConnectionMock):
        m = ConnectionMock()
        m.post.return_value = 10
        video = pybrightcove.video.Video(filename='bears.mov', name='The Bears',
            short_description='Opening roll for an exciting soccer match.')
        video.tags.append('unittest')
        self.assertEquals(video.id, None)
        video.save()
        self.assertEquals(video.id, 10)
        self.assertEquals(m.method_calls[0][0], 'post')
        self.assertEquals(m.method_calls[0][1][0], 'create_video')

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_save_new_with_renditions(self, ConnectionMock):
        m = ConnectionMock()
        m.post.return_value = 10

        renditions = []
        r = pybrightcove.video.Rendition()
        r.remote_url = 'http://my.server.com/640_h264.flv'
        r.size = 232522522
        r.video_duration = 60000
        r.video_codec = pybrightcove.enums.VideoCodecEnum.H264
        renditions.append(r)

        r = pybrightcove.video.Rendition()
        r.remote_url = 'http://my.server.com/560_h264.flv'
        r.size = 23252252
        r.video_duration = 60000
        r.video_codec = pybrightcove.enums.VideoCodecEnum.H264
        renditions.append(r)
        
        r = pybrightcove.video.Rendition()
        r.remote_url = 'http://my.server.com/480_h264.flv'
        r.size = 2325225
        r.video_duration = 60000
        r.video_codec = pybrightcove.enums.VideoCodecEnum.H264
        renditions.append(r)

        video = pybrightcove.video.Video(name='The Bears', renditions=renditions,
            short_description='Opening roll for an exciting soccer match.')
        video.tags.append('unittest')
        
        self.assertEquals(video.id, None)
        video.save()
        m.post.return_value = {'id': 123456, 'referenceId': 777777, 'type': 'VIDEO_STILL', 'remoteUrl': 'http://my.sample.com/image-2', 'displayName': None}
        i = pybrightcove.video.Image()
        i.type = pybrightcove.enums.ImageTypeEnum.THUMBNAIL
        i.remote_url = 'http://my.sample.com/image-1.jpg'
        video.set_image(i)
        i = pybrightcove.video.Image()
        i.type = pybrightcove.enums.ImageTypeEnum.VIDEO_STILL
        i.remote_url = 'http://my.sample.com/image-2.jpg'
        video.set_image(i)
        
        self.assertEquals(video.id, 10)
        self.assertEquals(m.method_calls[0][0], 'post')
        self.assertEquals(m.method_calls[0][1][0], 'create_video')
        self.assertEquals(len(m.method_calls[0][2]['video']['renditions']), 3)
        self.assertEquals(m.method_calls[0][2]['video']['renditions'][1]['remoteUrl'], 'http://my.server.com/560_h264.flv')
        self.assertEquals(m.method_calls[1][0], 'post')
        self.assertEquals(m.method_calls[1][1][0], 'add_image')
        self.assertEquals(m.method_calls[1][2]['image']['remoteUrl'], 'http://my.sample.com/image-1.jpg')
        self.assertEquals(m.method_calls[2][0], 'post')
        self.assertEquals(m.method_calls[2][1][0], 'add_image')
        self.assertEquals(m.method_calls[2][2]['image']['remoteUrl'], 'http://my.sample.com/image-2.jpg')

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_save_new_with_metadata(self, ConnectionMock):
        m = ConnectionMock()
        m.post.return_value = TEST_VIDEO_ID
        video = pybrightcove.video.Video(filename='bears.mov', name='The Bears',
            short_description='Opening roll for an exciting soccer match.')
        video.tags.append('unittest')
        self.assertEquals(video.id, None)
        video.add_custom_metadata('genre', 'Sci-Fi', 'string')
        video.add_custom_metadata('rating', 'PG-13', 'string')
        video.save()
        self.assertEquals(video.id, TEST_VIDEO_ID)
        self.assertEquals(m.method_calls[0][0], 'post')
        self.assertEquals(m.method_calls[0][1][0], 'create_video')
        self.assertTrue('unittest' in m.method_calls[0][2]['video']['tags'])
        self.assertTrue('customFields' in m.method_calls[0][2]['video'])
        self.assertTrue('genre' in m.method_calls[0][2]['video']['customFields'])
        self.assertTrue('rating' in m.method_calls[0][2]['video']['customFields'])
        self.assertEquals(m.method_calls[0][2]['video']['customFields']['genre'], 'Sci-Fi')
        self.assertEquals(m.method_calls[0][2]['video']['customFields']['rating'], 'PG-13')

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_save_update(self, ConnectionMock):
        m = ConnectionMock()
        m.post.return_value = VIDEO_DATA
        m.get_item.return_value = VIDEO_DATA
        video = pybrightcove.video.Video(id=TEST_VIDEO_ID)
        video.tags.append('tag-%s' % self.test_uuid)
        video.tags.append('unittest')
        lmd = video.last_modified_date
        self.assertEquals(video.id, TEST_VIDEO_ID)
        video.save()
        self.assertEquals(video.id, TEST_VIDEO_ID)
        self.assertEquals(video.reference_id, TEST_VIDEO_REF_ID)
        self.assertEquals(m.method_calls[0][0], 'get_item')
        self.assertEquals(m.method_calls[1][0], 'post')
        self.assertEquals(m.method_calls[1][1][0], 'update_video')
        self.assertTrue('unittest' in m.method_calls[1][2]['video']['tags'])
        self.assertTrue('tag-%s' % self.test_uuid in m.method_calls[1][2]['video']['tags'])

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_save_update_with_metadata(self, ConnectionMock):
        m = ConnectionMock()
        m.post.return_value = VIDEO_DATA
        m.get_item.return_value = VIDEO_DATA
        video = pybrightcove.video.Video(id=TEST_VIDEO_ID)
        video.tags.append('tag-%s' % self.test_uuid)
        video.tags.append('unittest')
        video.add_custom_metadata('genre', 'Sci-Fi', 'string')
        video.add_custom_metadata('rating', 'PG-13', 'string')
        lmd = video.last_modified_date
        self.assertEquals(video.id, TEST_VIDEO_ID)
        video.save()
        self.assertEquals(video.id, TEST_VIDEO_ID)
        self.assertEquals(video.reference_id, TEST_VIDEO_REF_ID)
        self.assertEquals(m.method_calls[0][0], 'get_item')
        self.assertEquals(m.method_calls[1][0], 'post')
        self.assertEquals(m.method_calls[1][1][0], 'update_video')
        self.assertTrue('unittest' in m.method_calls[1][2]['video']['tags'])
        self.assertTrue('tag-%s' % self.test_uuid in m.method_calls[1][2]['video']['tags'])
        self.assertTrue('customFields' in m.method_calls[1][2]['video'])
        self.assertTrue('genre' in m.method_calls[1][2]['video']['customFields'])
        self.assertTrue('rating' in m.method_calls[1][2]['video']['customFields'])
        self.assertEquals(m.method_calls[1][2]['video']['customFields']['genre'], 'Sci-Fi')
        self.assertEquals(m.method_calls[1][2]['video']['customFields']['rating'], 'PG-13')


    @mock.patch('pybrightcove.connection.APIConnection')
    def test_get_upload_status(self, ConnectionMock):
        m = ConnectionMock()
        m.post.return_value = pybrightcove.enums.UploadStatusEnum.PROCESSING
        m.get_item.return_value = VIDEO_DATA
        video = pybrightcove.video.Video(id=TEST_VIDEO_ID)
        status = video.get_upload_status()
        self.assertEquals(status, pybrightcove.enums.UploadStatusEnum.PROCESSING)
        self.assertEquals(m.method_calls[0][0], 'get_item')
        self.assertEquals(m.method_calls[1][0], 'post')
        self.assertEquals(m.method_calls[1][1][0], 'get_upload_status')
        self.assertEquals(m.method_calls[1][2]['video_id'], TEST_VIDEO_ID)
        
    @mock.patch('pybrightcove.connection.APIConnection')
    def test_delete(self, ConnectionMock):
        m = ConnectionMock()
        m.get_item.return_value = VIDEO_DATA
        video = pybrightcove.video.Video(id=TEST_VIDEO_ID)
        video.delete()
        self.assertEquals(m.method_calls[0][0], 'get_item')
        self.assertEquals(m.method_calls[1][0], 'post')
        self.assertEquals(m.method_calls[1][1][0], 'delete_video')
        self.assertEquals(m.method_calls[1][2]['video_id'], TEST_VIDEO_ID)

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_set_image(self, ConnectionMock):
        image = pybrightcove.video.Image(reference_id="img-%s" % self.test_uuid,
                      display_name="My Test Image",
                      type=pybrightcove.enums.ImageTypeEnum.VIDEO_STILL)
        m = ConnectionMock()
        m.post.return_value = IMAGE_DATA
        m.get_item.return_value = VIDEO_DATA
        video = pybrightcove.video.Video(id=TEST_VIDEO_ID)
        video.set_image(image, filename="IMG_0050.JPG")
        self.assertEquals(m.method_calls[0][0], 'get_item')
        self.assertEquals(m.method_calls[1][0], 'post')
        self.assertEquals(m.method_calls[1][1][0], 'add_image')
        self.assertEquals(m.method_calls[1][2]['video_id'], TEST_VIDEO_ID)
        self.assertEquals(video.image.to_dict(), IMAGE_DATA)

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_find_by_tags(self, ConnectionMock):
        m = self._get_list_mock(ConnectionMock)
        videos = pybrightcove.video.Video.find_by_tags(and_tags=['unittest', 'two'])
        for video in videos:
            print video #self.assertEquals(type(video), Video)
        print m.method_calls
        self.assertEquals(m.method_calls[0][0], 'get_list')
        self.assertEquals(m.method_calls[0][1][0], 'find_videos_by_tags')
        self.assertEquals(m.method_calls[0][2]['and_tags'], ','.join(['unittest', 'two']))

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_find_by_text(self, ConnectionMock):
        m = self._get_list_mock(ConnectionMock)
        videos = pybrightcove.video.Video.find_by_text('bear')
        for video in videos:
            print video #self.assertEquals(type(video), Video)
        print m.method_calls
        self.assertEquals(m.method_calls[0][0], 'get_list')
        self.assertEquals(m.method_calls[0][1][0], 'find_videos_by_text')
        self.assertEquals(m.method_calls[0][2]['text'], 'bear')

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_find_by_campaign(self, ConnectionMock):
        m = self._get_list_mock(ConnectionMock)
        videos = pybrightcove.video.Video.find_by_campaign(988756758)
        for video in videos:
            print video #self.assertEquals(type(video), Video)
        print m.method_calls
        self.assertEquals(m.method_calls[0][0], 'get_list')
        self.assertEquals(m.method_calls[0][1][0], 'find_videos_by_campaign_id')
        self.assertEquals(m.method_calls[0][2]['campaign_id'], 988756758)

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_find_by_user(self, ConnectionMock):
        m = self._get_list_mock(ConnectionMock)
        videos = pybrightcove.video.Video.find_by_user(12312431)
        for video in videos:
            print video #self.assertEquals(type(video), Video)
        print m.method_calls
        self.assertEquals(m.method_calls[0][0], 'get_list')
        self.assertEquals(m.method_calls[0][1][0], 'find_videos_by_user_id')
        self.assertEquals(m.method_calls[0][2]['user_id'], 12312431)

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_find_by_reference_ids(self, ConnectionMock):
        m = self._get_list_mock(ConnectionMock)
        videos = pybrightcove.video.Video.find_by_reference_ids(TEST_VIDEO_REF_IDS)
        for video in videos:
            print video #self.assertEquals(type(video), Video)
        print m.method_calls
        self.assertEquals(m.method_calls[0][0], 'get_list')
        self.assertEquals(m.method_calls[0][1][0], 'find_videos_by_reference_ids')
        self.assertEquals(m.method_calls[0][2]['reference_ids'], ','.join([str(x) for x in TEST_VIDEO_REF_IDS]))

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_find_by_ids(self, ConnectionMock):
        m = self._get_list_mock(ConnectionMock)
        videos = pybrightcove.video.Video.find_by_ids(TEST_VIDEO_IDS)
        for video in videos:
            print video #self.assertEquals(type(video), Video)
        print m.method_calls
        self.assertEquals(m.method_calls[0][0], 'get_list')
        self.assertEquals(m.method_calls[0][1][0], 'find_videos_by_ids')
        self.assertEquals(m.method_calls[0][2]['video_ids'], ','.join([str(x) for x in TEST_VIDEO_IDS]))

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_find_all(self, ConnectionMock):
        m = self._get_list_mock(ConnectionMock)
        videos = pybrightcove.video.Video.find_all()
        for video in videos:
            print video #self.assertEquals(type(video), Video)
        print m.method_calls
        self.assertEquals(m.method_calls[0][0], 'get_list')
        self.assertEquals(m.method_calls[0][1][0], 'find_all_videos')

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_find_related(self, ConnectionMock):
        m = self._get_list_mock(ConnectionMock)
        m.get_item.return_value = VIDEO_DATA
        video = pybrightcove.video.Video(id=TEST_VIDEO_ID)
        for related_video in video.find_related():
            print related_video #self.assertEquals(type(related_video), Video)
        print m.method_calls
        self.assertEquals(m.method_calls[1][0], 'get_list')
        self.assertEquals(m.method_calls[1][1][0], 'find_related_videos')
        self.assertEquals(m.method_calls[1][2]['video_id'], TEST_VIDEO_ID)

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_find_modified_unfiltered(self, ConnectionMock):
        m = self._get_list_mock(ConnectionMock)
        yesterday = datetime.now() - timedelta(days=1)
        videos = pybrightcove.video.Video.find_modified(since=yesterday)
        for video in videos:
            print video #self.assertEquals(type(video), Video)
        print m.method_calls
        self.assertEquals(m.method_calls[0][0], 'get_list')
        self.assertEquals(m.method_calls[0][1][0], 'find_modified_videos')
        self.assertEquals(m.method_calls[0][2]['from_date'] > 0, True)

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_find_modified_filtered(self, ConnectionMock):
        m = self._get_list_mock(ConnectionMock)
        yesterday = datetime.now() - timedelta(days=1)
        filters = [pybrightcove.enums.FilterChoicesEnum.PLAYABLE,
            pybrightcove.enums.FilterChoicesEnum.DELETED]
        videos = pybrightcove.video.Video.find_modified(since=yesterday, filter_list=filters)
        for video in videos:
            print video #self.assertEquals(type(video), Video)
        self.assertEquals(m.method_calls[0][0], 'get_list')
        self.assertEquals(m.method_calls[0][1][0], 'find_modified_videos')
        self.assertEquals(m.method_calls[0][2]['from_date'] > 0, True)
        self.assertEquals(m.method_calls[0][2]['filter'], filters)

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_invalid_name(self, ConnectionMock):
        try:
            video = pybrightcove.video.Video(name="Name is too long"*10,
                          short_description="ok desc",
                          filename="somefile.mov")
        except pybrightcove.exceptions.PyBrightcoveError, e:
            self.assertEqual(str(e),
                "Video.name must be 60 characters or less.")
        else:
            self.fail("Expected pybrightcove.exceptions.PyBrightcoveError.")

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_invalid_short_description(self, ConnectionMock):
        try:
            video = pybrightcove.video.Video(name="Name is too long",
                          short_description="ok desc"*100,
                          filename="somefile.mov")
        except pybrightcove.exceptions.PyBrightcoveError, e:
            self.assertEqual(str(e),
                "Video.short_description must be 250 characters or less.")
        else:
            self.fail("Expected pybrightcove.exceptions.PyBrightcoveError.")

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_invalid_long_description(self, ConnectionMock):
        try:
            video = pybrightcove.video.Video(name="Name is too long",
                          short_description="ok desc",
                          filename="somefile.mov")
            video.long_description = "Very long"*5000
        except pybrightcove.exceptions.PyBrightcoveError, e:
            self.assertEqual(str(e),
                "Video.long_description must be 5000 characters or less.")
        else:
            self.fail("Expected pybrightcove.exceptions.PyBrightcoveError.")

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_invalid_reference_id(self, ConnectionMock):
        try:
            video = pybrightcove.video.Video(name="Name is too long",
                          short_description="ok desc",
                          filename="somefile.mov")
            video.reference_id = "long ref id"*100
        except pybrightcove.exceptions.PyBrightcoveError, e:
            self.assertEqual(str(e),
                "Video.reference_id must be 150 characters or less.")
        else:
            self.fail("Expected pybrightcove.exceptions.PyBrightcoveError.")

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_invalid_economics(self, ConnectionMock):
        try:
            video = pybrightcove.video.Video(name="Name is too long",
                          short_description="ok desc",
                          filename="somefile.mov")
            video.economics = "The Keynesian view is Wrong"
        except pybrightcove.exceptions.PyBrightcoveError, e:
            err = "Video.economics must be either EconomicsEnum.FREE or"
            err += " EconomicsEnum.AD_SUPPORTED"
            self.assertEqual(str(e), err)
        else:
            self.fail("Expected pybrightcove.exceptions.PyBrightcoveError.")

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_invalid_item_state(self, ConnectionMock):
        try:
            video = pybrightcove.video.Video(name="Name is too long",
                          short_description="ok desc",
                          filename="somefile.mov")
            video.item_state = "Invalid"
        except pybrightcove.exceptions.PyBrightcoveError, e:
            err = "Video.item_state must be either ItemStateEnum.ACTIVE or "
            err += "ItemStateEnum.INACTIVE"
            self.assertEqual(str(e), err)
        else:
            self.fail("Expected pybrightcove.exceptions.PyBrightcoveError.")

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_invalid_video_full_length(self, ConnectionMock):
        try:
            video = pybrightcove.video.Video(name="Name is too long",
                          short_description="ok desc",
                          filename="somefile.mov")
            video.video_full_length = 10
        except pybrightcove.exceptions.PyBrightcoveError, e:
            self.assertEqual(str(e),
                "Video.video_full_length must be of type Rendition")
        else:
            self.fail("Expected pybrightcove.exceptions.PyBrightcoveError.")
