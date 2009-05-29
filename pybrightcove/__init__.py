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

from pybrightcove.exceptions import PyBrightcoveError
from pybrightcove.config import Config
from pybrightcove.video import Video
from pybrightcove.playlist import Playlist
from pybrightcove.enums import SortByType, SortByOrderType

Version = '0.1'
UserAgent = 'PyBrightcove/%s (%s)' % (Version, sys.platform)
config = Config()


def item_lister(comand, connection, page_size, page_number, sort_by,
    sort_order, **kwargs):
    """
    A generator function for listing Video and Playlist objects.
    """
    page = page_number
    while True:
        itemCollection = connection.get_list_command(command,
                                                page_size=page_size,
                                                page_number=page,
                                                sort_by=sort_by,
                                                sort_order=sort_order,
                                                **kwargs)
        for item in itemCollection.items:
            yield item
        if item:
            page += 1
        else:
            break


class ItemResultSet(object):

    def __init__(self, command, connection, page_size=100, page_number=0,
            sort_by=SortByType.CREATION_DATE, sort_order=SortByOrderType.ASC,
            **kwargs):
        self.command = command
        self.connection = connection
        self.page_size = page_size
        self.page_number = page_number
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.kwargs = kwargs

    def __iter__(self):
        return item_lister(self.command, self.connection, self.page_size,
            self.page_number, self.sort_by, self.sort_order, **self.kwargs)


class ItemCollection(object):

    def __init__(self, data, collection_type):
        self.total_count = None
        self.items = None
        self.page_number = None
        self.page_size = None
        self.items = []

        self.total_count = int(data['total_count'])
        self.page_number = int(data['page_number'])
        self.page_size = int(data['page_size'])
        for item in data['items']:
            if collection_type == 'Video':
                self.items.append(Video(data=item))
            elif collection_type == 'Playlist':
                self.items.append(Playlist(data=item))
