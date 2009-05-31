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

import hashlib
import simplejson
import urllib2
import urllib
import cookielib
from pybrightcove import config, UserAgent
from pybrightcove import SortByType, SortByOrderType
from pybrightcove import BrightcoveError
from pybrightcove.multipart import MultipartPostHandler


class Connection(object):

    def __init__(self, read_token=None, write_token=None, **kwargs):
        if read_token:
            self.read_token = read_token
        elif config.has_option('Connection', 'read_token'):
            self.read_token = config.get('Connection', 'read_token')

        if write_token:
            self.write_token = write_token
        elif config.has_option('Connection', 'write_token'):
            self.write_token = config.get('Connection', 'write_token')

        if 'read_url' in kwargs:
            self.read_url = kwargs['read_url']
        elif config.has_option('Connection', 'read_url'):
            self.read_url = config.get('Connection', 'read_url')

        if 'write_url' in kwargs:
            self.write_url = kwargs['write_url']
        elif config.has_option('Connection', 'write_url'):
            self.write_url = config.get('Connection', 'write_url')

    def _post(self, data, file_to_upload=None):
        params = {"JSONRPC": simplejson.dumps(data)}
        req = None
        if file_to_upload:
            cookies = cookielib.CookieJar()
            cproc = urllib2.HTTPCookieProcessor(cookies)
            opener = urllib2.build_opener(cproc, MultipartPostHandler)
            params["filePath"] = open(file_to_upload, "rb")
            req = opener.open(self.write_url, params)
        else:
            msg = urllib.urlencode({'json': params['JSONRPC']})
            req = urllib2.urlopen(self.write_url, msg)

        if req:
            result = simplejson.loads(req.read())
            if 'error' in result and result['error']:
                BrightcoveError.raise_exception(result['error'])
            return result['result']

    def _get_response(self, **kwargs):
        url = self.read_url + "?output=JSON&token=%s" % self.read_token
        for key in kwargs:
            if key and kwargs[key]:
                val = kwargs[key]
                if isinstance(val, (list, tuple)):
                    val = ",".join(val)
                url += "&%s=%s" % (key, val)
        req = urllib2.urlopen(url)
        data = simplejson.loads(req.read())
        if 'error' in data and data['error']:
            BrightcoveError.raise_exception(data['error'])
        return data

    def post(self, command, file_to_upload=None, **kwargs):
        data = {"method": command}
        params = {"token": self.write_token}
        for key in kwargs:
            if key and kwargs[key]:
                params[key] = kwargs[key]
        if file_to_upload:
            m = hashlib.md5()
            fp = open(file_to_upload, 'rb')
            bits = fp.read(262144)  ## 256KB
            while bits:
                m.update(bits)
                bits = fp.read(262144)
            fp.close()
            params['file_checksum'] = m.hexdigest()
        data['params'] = params

        return self._post(data=data, file_to_upload=file_to_upload)

    def get_list(self, command, item_class, page_size, page_number, sort_by,
        sort_order, **kwargs):
        """
        Not intended to be called directly, but rather through an by the
        ItemResultSet object iterator.
        """
        data = self._get_response(command=command,
                                  page_size=page_size,
                                  page_number=page_number,
                                  sort_by=sort_by,
                                  sort_order=sort_order,
                                  video_fields=None,
                                  get_item_count="true",
                                  **kwargs)
        return ItemCollection(data=data, item_class=item_class)

    def get_item(self, command, **kwargs):
        data = self._get_response(command=command, **kwargs)
        return data


def item_lister(command, connection, page_size, page_number, sort_by,
    sort_order, item_class, **kwargs):
    """
    A generator function for listing Video and Playlist objects.
    """
    page = page_number
    while True:
        itemCollection = connection.get_list(command,
                                             page_size=page_size,
                                             page_number=page,
                                             sort_by=sort_by,
                                             sort_order=sort_order,
                                             item_class=item_class,
                                             **kwargs)
        for item in itemCollection.items:
            yield item
        if len(itemCollection.items) > 0:
            page += 1
        else:
            break


class ItemResultSet(object):

    def __init__(self, command, item_class, connection=None, page_size=100,
            page_number=0, sort_by=SortByType.CREATION_DATE,
            sort_order=SortByOrderType.ASC, **kwargs):
        self.command = command
        if connection:
            self.connection = connection
        else:
            self.connection = Connection()
        self.page_size = page_size
        self.page_number = page_number
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.item_class = item_class
        self.kwargs = kwargs

    def __iter__(self):
        return item_lister(self.command, self.connection, self.page_size,
            self.page_number, self.sort_by, self.sort_order, self.item_class,
            **self.kwargs)


class ItemCollection(object):

    def __init__(self, data, item_class):
        self.total_count = None
        self.items = None
        self.page_number = None
        self.page_size = None
        self.items = []

        self.total_count = int(data['total_count'])
        self.page_number = int(data['page_number'])
        self.page_size = int(data['page_size'])
        for item in data['items']:
            self.items.append(item_class(data=item))
