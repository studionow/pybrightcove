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
Test the Playlist object
"""

import unittest
import uuid
import mock
import pybrightcove

TEST_VIDEO_ID = 11449913001
TEST_VIDEO_IDS = [TEST_VIDEO_ID, 24780403001, 24780402001]
TEST_PLAYLIST_ID = 24781161001
TEST_PLAYLIST_IDS = [TEST_PLAYLIST_ID, 10518202001]
TEST_PLAYLIST_REF_ID = 'unittest-playlist'
TEST_PLAYLIST_REF_IDS = [TEST_PLAYLIST_REF_ID, 'test']


class PlaylistTest(unittest.TestCase):

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
        playlist = pybrightcove.playlist.Playlist(name='My Playlist', type=pybrightcove.enums.PlaylistTypeEnum.EXPLICIT)
        playlist.video_ids = TEST_VIDEO_IDS
        self.assertEquals(playlist.id, None)
        self.assertEquals(playlist.name, 'My Playlist')
        self.assertEquals(playlist.type, pybrightcove.enums.PlaylistTypeEnum.EXPLICIT)
        self.assertEquals(playlist.video_ids, TEST_VIDEO_IDS)
        self.assertEquals(playlist.short_description, None)

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_instantiate_with_playlist_id(self, ConnectionMock):
        m = ConnectionMock()
        m.get_item.return_value = {'id': TEST_PLAYLIST_ID, 'name': '', 'shortDescription': '', 'referenceId': TEST_PLAYLIST_REF_ID, 'thumbnailURL': '', 'videoIds': [], 'playlistType': ''}
        playlist = pybrightcove.playlist.Playlist(id=TEST_PLAYLIST_ID)
        self.assertEquals(playlist.reference_id, TEST_PLAYLIST_REF_ID)

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_instantiate_with_reference_id(self, ConnectionMock):
        m = ConnectionMock()
        m.get_item.return_value = {'id': TEST_PLAYLIST_ID, 'name': '', 'shortDescription': '', 'referenceId': TEST_PLAYLIST_REF_ID, 'thumbnailURL': '', 'videoIds': [], 'playlistType': ''}
        playlist = pybrightcove.playlist.Playlist(reference_id=TEST_PLAYLIST_REF_ID)
        self.assertEquals(playlist.id, TEST_PLAYLIST_ID)

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_instantiate_with_invalid_parameters(self, ConnectionMock):
        try:
            playlist = pybrightcove.playlist.Playlist(name="No type specified")
            self.fail('Should have raised an error.')
        except pybrightcove.PyBrightcoveError, e:
            self.assertEquals(str(e), 'Invalid parameters for Video.')

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_save_new(self, ConnectionMock):
        m = self._get_list_mock(ConnectionMock)
        m.post.return_value = 10
        playlist = pybrightcove.playlist.Playlist(name="Unit Test Videos",
            type=pybrightcove.enums.PlaylistTypeEnum.EXPLICIT)
        for video in pybrightcove.Video.find_by_tags(and_tags=['unittest', ]):
            playlist.videos.append(video)
        playlist.save()
        self.assertEquals(playlist.id, 10)
        self.assertEquals(playlist.name, 'Unit Test Videos')
        self.assertEquals(m.method_calls[0][0], 'get_list')
        self.assertEquals(m.method_calls[0][1][0], 'find_videos_by_tags')
        self.assertEquals(m.method_calls[1][0], 'post')
        self.assertEquals(m.method_calls[1][1][0], 'create_playlist')

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_save_update(self, ConnectionMock):
        m = ConnectionMock()
        data = {}
        data['id'] = TEST_PLAYLIST_ID
        data['referenceId'] = TEST_PLAYLIST_REF_ID
        data['name'] = "test-%s" % self.test_uuid
        data['shortDescription'] = "My description"
        data['thumbnailURL'] = "http://google.com"
        data['videoIds'] = TEST_VIDEO_IDS
        data['playlistType'] = pybrightcove.enums.PlaylistTypeEnum.EXPLICIT
        m.get_item.return_value = data
        m.post.return_value = data
        playlist = pybrightcove.playlist.Playlist(id=TEST_PLAYLIST_ID)
        playlist.name = 'test-%s' % self.test_uuid
        playlist.save()
        self.assertEquals(playlist.id, TEST_PLAYLIST_ID)
        self.assertEquals(playlist.name, 'test-%s' % self.test_uuid)
        self.assertEquals(m.method_calls[0][0], 'get_item')
        self.assertEquals(m.method_calls[0][1][0], 'find_playlist_by_id')
        self.assertEquals(m.method_calls[1][0], 'post')
        self.assertEquals(m.method_calls[1][1][0], 'update_playlist')
        

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_delete(self, ConnectionMock):
        m = self._get_list_mock(ConnectionMock)
        m.post.return_value = 10

        playlist = pybrightcove.playlist.Playlist(name="DELETE - Unit Test Videos",
            type=pybrightcove.enums.PlaylistTypeEnum.EXPLICIT)
        for video in pybrightcove.video.Video.find_by_tags(and_tags=['unittest', ]):
            playlist.videos.append(video)
        self.assertEquals(playlist.id, None)
        playlist.save()
        self.assertEquals(playlist.id, 10)
        playlist.delete()
        self.assertEquals(playlist.id, None)
        self.assertEquals(m.method_calls[0][0], 'get_list')
        self.assertEquals(m.method_calls[0][1][0], 'find_videos_by_tags')
        self.assertEquals(m.method_calls[1][0], 'post')
        self.assertEquals(m.method_calls[1][1][0], 'create_playlist')
        self.assertEquals(m.method_calls[2][0], 'post')
        self.assertEquals(m.method_calls[2][1][0], 'delete_playlist')

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_find_by_ids(self, ConnectionMock):
        m = self._get_list_mock(ConnectionMock)
        playlists = pybrightcove.playlist.Playlist.find_by_ids(TEST_PLAYLIST_IDS)
        for playlist in playlists:
            print playlist
        print m.method_calls
        self.assertEquals(m.method_calls[0][0], 'get_list')
        self.assertEquals(m.method_calls[0][1][0], 'find_playlists_by_ids')
        self.assertEquals(m.method_calls[0][2]['playlist_ids'], ','.join([str(x) for x in TEST_PLAYLIST_IDS]))
        

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_find_by_reference_ids(self, ConnectionMock):
        m = self._get_list_mock(ConnectionMock)
        playlists = pybrightcove.playlist.Playlist.find_by_reference_ids(TEST_PLAYLIST_REF_IDS)
        for playlist in playlists:
            print playlist
        print m.method_calls
        self.assertEquals(m.method_calls[0][0], 'get_list')
        self.assertEquals(m.method_calls[0][1][0], 'find_playlists_by_reference_ids')
        self.assertEquals(m.method_calls[0][2]['reference_ids'], ','.join([str(x) for x in TEST_PLAYLIST_REF_IDS]))

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_find_for_player_id(self, ConnectionMock):
        m = self._get_list_mock(ConnectionMock)
        playlists = pybrightcove.playlist.Playlist.find_for_player_id(23424255)
        for playlist in playlists:
            print playlist
        print m.method_calls
        self.assertEquals(m.method_calls[0][0], 'get_list')
        self.assertEquals(m.method_calls[0][1][0], 'find_playlists_for_player_id')
        self.assertEquals(m.method_calls[0][2]['player_id'], 23424255)

    @mock.patch('pybrightcove.connection.APIConnection')
    def test_find_all(self, ConnectionMock):
        m = self._get_list_mock(ConnectionMock)
        playlists = pybrightcove.playlist.Playlist.find_all()
        for playlist in playlists:
            print playlist
        self.assertEquals(m.method_calls[0][0], 'get_list')
        self.assertEquals(m.method_calls[0][1][0], 'find_all_playlists')
        
        