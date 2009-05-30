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

from pybrightcove import PlaylistTypeEnum
from pybrightcove import Video


class Playlist(object):
    """The Playlist object is a collection of Videos."""

    def __init__(self, data=None):
        self._id = None
        self._referenceId = None
        self._name = None
        self._shortDescription = None
        self._thumbnailURL = None
        self._filterTags = None
        self._videos = None
        self._videoIds = None
        self._playlistType = None

        if data:
            self._id = data['id']
            self._referenceId = data['referenceId']
            self._name = data['name']
            self._shortDescription = data['shortDescription']
            self._thumbnailURL = data['thumbnailURL']
            self._filterTags = data['filterTags']
            self._videoIds = data['videoIds']
            self._playlistType = data['playlistType']

            for video in data.get('videos', []):
                self.videos.append(Video(data=video))

    def get_id(self):
        return self._id

    def get_referenceId(self):
        return self._referenceId

    def set_referenceId(self, referenceId):
        self._referenceId = referenceId

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_shortDescription(self):
        return self._shortDescription

    def set_shortDescription(self, short_description):
        self._shortDescription = short_description[:250]

    def get_filterTags(self):
        if not self._filterTags:
            self._filterTags = []
        return self._filterTags

    def set_filterTags(self, tags):
        self._filterTags = tags

    def get_videoIds(self):
        if not self._videoIds:
            self._videoIds = []
        return self._videoIds

    def set_videoIds(self, video_ids):
        self._videoIds = video_ids

    def get_videos(self):
        if not self._videos:
            self._videos = []
        return self._videos

    def set_videos(self, videos):
        self._videos = videos

    def get_playlistType(self):
        return self._playlistType

    def set_playlistType(self, playlist_type):
        if playlist_type not in PlaylistTypeEnum.__dict__.values():
            raise TypeError("Invalid Playlist Type")
        self._playlistType = playlist_type

    def get_thumbnailURL(self):
        return self._thumbnailURL

    def set_thumbnailURL(self, thumbnail_url):
        self._thumbnailURL = thumbnail_url

    id = property(get_id,
        doc="""A number that uniquely identifies this Playlist.
            This id is automatically assigned when the Playlist is created.""")

    referenceId = property(get_referenceId, set_referenceId,
        doc="""A user-specified id that uniquely identifies this Playlist.""")

    name = property(get_name, set_name,
        doc="""TThe title of this Playlist. The name is a required property
            when you create a playlist.""")

    shortDescription = property(get_shortDescription, set_shortDescription,
        doc="""A short description describing this Playlist, limited to 250
            characters.""")

    filterTags = property(get_filterTags, set_filterTags,
        doc="""filterTags""")

    videoIds = property(get_videoIds, set_videoIds,
        doc="""A list of the ids of the Videos that are encapsulated in this
            Playlist.""")

    videos = property(get_videos, set_videos,
        doc="""A list of the Video objects that are encapsulated in this
            Playlist.""")

    playlistType = property(get_playlistType, set_playlistType,
        doc="""Options are OLDEST_TO_NEWEST, NEWEST_TO_OLDEST, ALPHABETICAL,
            PLAYSTRAILING, and PLAYSTRAILINGWEEK (each of which is a smart
            playlist, ordered as indicated) or EXPLICIT (a manual playlist).
            The playlistType is a required property when you create a
            playlist.""")

    thumbnailURL = property(get_thumbnailURL, set_thumbnailURL,
        doc="""The URL of the thumbnail associated with this Playlist.""")
