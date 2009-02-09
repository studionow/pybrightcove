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

import sys
from pybrightcove.config import Config
from pybrightcove.video import Video
from pybrightcove.playlist import Playlist

Version = '0.1'
UserAgent = 'PyBrightcove/%s (%s)' % (Version, sys.platform)
config = Config()


class ItemCollection(object):

    def __init__(self, data=None, collection_type=None):
        self._total_count = None
        self._items = None
        self._page_number = None
        self._page_size = None

        if data and collection_type:
            self._total_count = data['total_count']
            self._page_number = data['page_number']
            self._page_size = data['page_size']
            for item in data['items']:
                if collection_type == 'Video':
                    self.items.append(Video(data=item))
                elif collection_type == 'Playlist':
                    self.items.append(Playlist(data=item))

    def get_total_count(self):
        return self._total_count

    def get_page_number(self):
        return self._page_number

    def get_page_size(self):
        return self._page_size

    def get_items(self):
        if not self._items:
            self._items = []
        return self._items

    total_count = property(get_total_count,
        doc="The total number of videos in the collection.")
    page_number = property(get_page_number,
        doc="Which page of the results this ItemCollection represents.")
    page_size = property(get_page_size,
        doc="How many items a page consists of.")
    items = property(get_items,
        doc="The actual items that this collection contains.")
