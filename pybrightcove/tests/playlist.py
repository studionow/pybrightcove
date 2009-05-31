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
from pybrightcove import Playlist, PlaylistTypeEnum, Video, PyBrightcoveError
from pybrightcove.tests.video import TEST_VIDEO_IDS

TEST_PLAYLIST_ID = 24781161001
TEST_PLAYLIST_IDS = [TEST_PLAYLIST_ID, 10518202001]
TEST_PLAYLIST_REF_ID = 'unittest-playlist'
TEST_PLAYLIST_REF_IDS = [TEST_PLAYLIST_REF_ID, 'test']


class PlaylistTest(unittest.TestCase):

    def setUp(self):
        self.test_uuid = str(uuid.uuid4())

    def test_instantiate_new(self):
        playlist = Playlist(name='My Playlist', video_ids=TEST_VIDEO_IDS,
            type=PlaylistTypeEnum.EXPLICIT)
        self.assertEquals(playlist.id, None)
        self.assertEquals(playlist.name, 'My Playlist')
        self.assertEquals(playlist.type, PlaylistTypeEnum.EXPLICIT)
        self.assertEquals(playlist.video_ids, TEST_VIDEO_IDS)
        self.assertEquals(playlist.short_description, None)

    def test_instantiate_with_playlist_id(self):
        playlist = Playlist(id=TEST_PLAYLIST_ID)
        self.assertEquals(playlist.reference_id, TEST_PLAYLIST_REF_ID)

    def test_instantiate_with_reference_id(self):
        playlist = Playlist(reference_id=TEST_PLAYLIST_REF_ID)
        self.assertEquals(playlist.id, TEST_PLAYLIST_ID)

    def test_instantiate_with_invalid_parameters(self):
        try:
            playlist = Playlist(name="No type specified")
            self.fail('Should have raised an error.')
        except PyBrightcoveError, e:
            self.assertEquals(e.message, 'Invalid parameters for Video.')

    def test_save_new(self):
        playlist = Playlist(name="Unit Test Videos",
            type=PlaylistTypeEnum.EXPLICIT)
        for video in Video.find_by_tags(and_tags=['unittest', ]):
            playlist.videos.append(video)
        playlist.save()
        self.assertEquals(playlist.id > 0, True)

    def test_save_update(self):
        playlist = Playlist(id=TEST_PLAYLIST_ID)
        playlist.name = 'test-%s' % self.test_uuid
        playlist.save()
        self.assertEquals(playlist.name, 'test-%s' % self.test_uuid)

    def test_delete(self):
        playlist = Playlist(name="DELETE - Unit Test Videos",
            type=PlaylistTypeEnum.EXPLICIT)
        for video in Video.find_by_tags(and_tags=['unittest', ]):
            playlist.videos.append(video)
        playlist.save()
        playlist.delete()
        self.assertEquals(playlist.id, None)

    def test_find_by_ids(self):
        playlists = Playlist.find_by_ids(TEST_PLAYLIST_IDS)
        for playlist in playlists:
            self.assertEquals(type(playlist), Playlist)
            self.assertEquals(playlist.id in TEST_PLAYLIST_IDS, True)

    def test_find_by_reference_ids(self):
        playlists = Playlist.find_by_reference_ids(TEST_PLAYLIST_REF_IDS)
        for playlist in playlists:
            self.assertEquals(type(playlist), Playlist)
            self.assertEquals(playlist.reference_id in TEST_PLAYLIST_REF_IDS,
                True)

    def test_find_for_player_id(self):
        playlists = Playlist.find_for_player_id(23424255)
        for playlist in playlists:
            self.assertEquals(type(playlist), Playlist)

    def test_find_all(self):
        playlists = Playlist.find_all()
        for playlist in playlists:
            self.assertEquals(type(playlist), Playlist)
