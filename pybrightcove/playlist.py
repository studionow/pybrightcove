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
The ``pybrightcove.playlist`` module supports all Brightcove functions dealing
with playlist objects.
"""

import pybrightcove
from pybrightcove.enums import DEFAULT_SORT_BY, DEFAULT_SORT_ORDER

VALID_PLAYLIST_TYPES = (pybrightcove.enums.PlaylistTypeEnum.EXPLICIT,
                        pybrightcove.enums.PlaylistTypeEnum.OLDEST_TO_NEWEST,
                        pybrightcove.enums.PlaylistTypeEnum.NEWEST_TO_OLDEST,
                        pybrightcove.enums.PlaylistTypeEnum.ALPHABETICAL,
                        pybrightcove.enums.PlaylistTypeEnum.PLAYS_TOTAL,
                        pybrightcove.enums.PlaylistTypeEnum.PLAYS_TRAILING_WEEK)
                        

class Playlist(object):
    """
    The Playlist object is a collection of Videos.
    """
    # pylint: disable=C0103,R0913,R0902
    # redefine type,id builtins - refactor later
    # pylint: disable=W0622
    def __init__(self, name=None, type=None, id=None, reference_id=None,
        data=None, connection=None):
        self.id = None
        self.reference_id = None
        self.account_id = None
        self.name = None
        self.short_description = None
        self.thumbnail_url = None
        self.videos = []
        self.video_ids = []
        self.type = None

        self.raw_data = None

        self.connection = connection
        if not self.connection:
            self.connection = pybrightcove.connection.APIConnection()

        if name and type in VALID_PLAYLIST_TYPES:
            self.name = name
            self.type = type
        elif id or reference_id:
            self.id = id
            self.reference_id = reference_id
            self._find_playlist()
        elif data:
            self._load(data)
        else:
            msg = "Invalid parameters for Playlist."
            raise pybrightcove.exceptions.PyBrightcoveError(msg)

    def __setattr__(self, name, value):
        msg = None
        if value:
            if name == 'name' and len(value) > 60:
                # val = value[:60] ## Is this better?
                msg = "Playlist.name must be 60 characters or less."
            if name == 'reference_id' and len(value) > 150:
                # val = value[:150]
                msg = "Playlist.reference_id must be 150 characters or less."
            if name == 'short_description' and len(value) > 250:
                # val = value[:250]
                msg = "Playlist.short_description must be 250 chars or less."
            if name == 'type' and value not in VALID_PLAYLIST_TYPES:
                msg = "Playlist.type must be a valid PlaylistTypeEnum"
            if msg:
                raise pybrightcove.exceptions.PyBrightcoveError(msg)
        return super(Playlist, self).__setattr__(name, value)

    def _find_playlist(self):
        """
        Internal method to populate the object given the ``id`` or
        ``reference_id`` that has been set in the constructor.
        """
        data = None
        if self.id:
            data = self.connection.get_item(
                'find_playlist_by_id', playlist_id=self.id)
        elif self.reference_id:
            data = self.connection.get_item(
                'find_playlist_by_reference_id',
                reference_id=self.reference_id)

        if data:
            self._load(data)

    def _to_dict(self):
        """
        Internal method that serializes object into a dictionary.
        """
        data = {
            'name': self.name,
            'referenceId': self.reference_id,
            'shortDescription': self.short_description,
            'playlistType': self.type,
            'id': self.id}
        if self.videos:
            for video in self.videos:
                if video.id not in self.video_ids:
                    self.video_ids.append(video.id)
        if self.video_ids:
            data['videoIds'] = self.video_ids
        [data.pop(key) for key in data.keys() if data[key] == None]
        return data

    def _load(self, data):
        """
        Internal method that deserializes a ``pybrightcove.playlist.Playlist``
        object.
        """
        self.raw_data = data
        self.id = data['id']
        self.reference_id = data['referenceId']
        self.name = data['name']
        self.short_description = data['shortDescription']
        self.thumbnail_url = data['thumbnailURL']
        self.videos = []
        self.video_ids = data['videoIds']
        self.type = data['playlistType']

        for video in data.get('videos', []):
            self.videos.append(pybrightcove.video.Video(
                data=video, connection=self.connection))

    def save(self):
        """
        Create or update a playlist.
        """
        d = self._to_dict()
        if len(d.get('videoIds', [])) > 0:
            if not self.id:
                self.id = self.connection.post('create_playlist', playlist=d)
            else:
                data = self.connection.post('update_playlist', playlist=d)
                if data:
                    self._load(data)

    def delete(self, cascade=False):
        """
        Deletes this playlist.
        """
        if self.id:
            self.connection.post('delete_playlist', playlist_id=self.id,
                cascade=cascade)
            self.id = None

    @staticmethod
    def find_all(connection=None, page_size=100, page_number=0,
        sort_by=DEFAULT_SORT_BY, sort_order=DEFAULT_SORT_ORDER):
        """
        List all playlists.
        """
        return pybrightcove.connection.ItemResultSet("find_all_playlists",
            Playlist, connection, page_size, page_number, sort_by, sort_order)

    @staticmethod
    def find_by_ids(ids, connection=None, page_size=100, page_number=0,
        sort_by=DEFAULT_SORT_BY, sort_order=DEFAULT_SORT_ORDER):
        """
        List playlists by specific IDs.
        """
        ids = ','.join([str(i) for i in ids])
        return pybrightcove.connection.ItemResultSet('find_playlists_by_ids',
            Playlist, connection, page_size, page_number, sort_by, sort_order,
            playlist_ids=ids)

    @staticmethod
    def find_by_reference_ids(reference_ids, connection=None, page_size=100,
        page_number=0, sort_by=DEFAULT_SORT_BY, sort_order=DEFAULT_SORT_ORDER):
        """
        List playlists by specific reference_ids.
        """
        reference_ids = ','.join([str(i) for i in reference_ids])
        return pybrightcove.connection.ItemResultSet(
            "find_playlists_by_reference_ids", Playlist, connection, page_size,
            page_number, sort_by, sort_order, reference_ids=reference_ids)

    @staticmethod
    def find_for_player_id(player_id, connection=None, page_size=100,
        page_number=0, sort_by=DEFAULT_SORT_BY, sort_order=DEFAULT_SORT_ORDER):
        """
        List playlists for a for given player id.
        """
        return pybrightcove.connection.ItemResultSet(
            "find_playlists_for_player_id", Playlist, connection, page_size,
            page_number, sort_by, sort_order, player_id=player_id)
