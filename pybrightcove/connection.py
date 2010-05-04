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

import os
import hashlib
import simplejson
import urllib2
import urllib
import tempfile
import ftplib
from xml.dom import minidom
import pybrightcove
from pybrightcove import DEFAULT_SORT_BY, DEFAULT_SORT_ORDER


class Connection(object):

    def _set(self, param, default=None, **kwargs):
        if kwargs.get(param, None):
            setattr(self, param, kwargs[param])
        elif pybrightcove.config.config.has_option('Connection', param):
            setattr(self, param, pybrightcove.config.config.get('Connection', param))
        elif default:
            setattr(self, param, default)

    def __init__(self, **kwargs):
        # API Connection
        self._set('read_token', **kwargs)
        self._set('write_token', **kwargs)
        self._set('read_url',
            default='http://api.brightcove.com/services/library', **kwargs)
        self._set('write_url',
            default='http://api.brightcove.com/services/post', **kwargs)

        # FTP Connection
        self._set('host', default='upload.brightcove.com', **kwargs)
        self._set('user', **kwargs)
        self._set('password', **kwargs)
        self._set('publisher_id', **kwargs)
        self._set('preparer', **kwargs)
        self._set('report_success', **kwargs)

    def post(self, **kwargs):
        raise Exception("Base class must implement this method.")

    def get_list(self, **kwargs):
        raise Exception("Base class must implement this method.")

    def get_item(self, **kwargs):
        raise Exception("Base class must implement this method.")


class FTPConnection(Connection):

    def __init__(self, host=None, user=None, password=None, publisher_id=None,
        preparer=None, report_success=False):
        super(FTPConnection, self).__init__(host=host, user=user,
            password=password, publisher_id=publisher_id, preparer=preparer,
            report_success=report_success)
        self.notifications = []
        self.callback = None

    def get_manifest(self, asset_xml):
        manifest = '<?xml version="1.0" encoding="utf-8"?>'
        manifest += '<publisher-upload-manifest publisher-id="%s" ' % \
            self.publisher_id
        manifest += 'preparer="%s" ' % self.preparer
        if self.report_success:
            manifest += 'report-success="TRUE">\n'
        for notify in self.notifications:
            manifest += '<notify email="%s"/>' % notify
        if self.callback:
            manifest += '<callback entity-url="%s"/>' % self.callback
        manifest += asset_xml
        manifest += '</publisher-upload-manifest>'
        return manifest

    def _send_file(self, filename):
        ftp = ftplib.FTP(host=self.host)
        ftp.login(user=self.user, passwd=self.password)
        ftp.set_pasv(True)
        ftp.storbinary("STOR %s" % os.path.basename(filename),
            file(filename, 'rb'))

    def post(self, xml, assets):
        ## Build manifest
        manifest = self.get_manifest(xml)

        ## Make sure it is well formed at least
        minidom.parseString(manifest)

        ## Record manifest
        fp, fname = tempfile.mkstemp(suffix=".xml",
            prefix="pybrightcove-manifest")
        file(fname, 'wb').write(manifest)

        ## Upload files and manifest
        for asset in assets:
            self._send_file(asset['filename'])
        self._send_file(fname)

    def get_list(self, **kwargs):
        raise Exception("This method is invalid for an FTP Connection")

    def get_item(self, **kwargs):
        raise Exception("This method is invalid for an FTP Connection")


class APIConnection(Connection):

    def __init__(self, read_token=None, write_token=None, read_url=None,
        write_url=None):
        super(APIConnection, self).__init__(read_token=read_token,
            write_token=write_token, read_url=read_url, write_url=write_url)
        if not hasattr(self, "read_token"):
            raise pybrightcove.exceptions.ImproperlyConfiguredError("Must specify at least a read_token.")

    def _post(self, data, file_to_upload=None):
        params = {"JSONRPC": simplejson.dumps(data)}
        req = None
        if file_to_upload:
            req = pybrightcove.http_core.HttpRequest(self.write_url)
            req.method = 'POST'
            req.add_body_part("JSONRPC", simplejson.dumps(data), 'text/plain')
            req.add_body_part("filePath", file(file_to_upload, "rb"), 'application/octet-stream')
            req.end_of_parts()
            req.headers['Content-Type'] = 'multipart/form-data; boundary=%s' % pybrightcove.http_core.MIME_BOUNDARY
            req.headers['User-Agent'] = pybrightcove.config.UserAgent

            req = pybrightcove.http_core.ProxiedHttpClient().request(req)
        else:
            msg = urllib.urlencode({'json': params['JSONRPC']})
            req = urllib2.urlopen(self.write_url, msg)

        if req:
            result = simplejson.loads(req.read())
            if 'error' in result and result['error']:
                pybrightcove.exceptions.BrightcoveError.raise_exception(result['error'])
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
        if data and data.get('error', None):
            pybrightcove.exceptions.BrightcoveError.raise_exception(data['error'])
        if data == None:
            raise pybrightcove.exceptions.NoDataFoundError("No data found for %s" % repr(kwargs))
        return data

    def post(self, command, file_to_upload=None, **kwargs):
        data = {"method": command}
        params = {"token": self.write_token}
        for key in kwargs:
            if key and kwargs[key]:
                params[key] = kwargs[key]
        if file_to_upload:
            m = hashlib.md5()
            fp = file(file_to_upload, 'rb')
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
        return ItemCollection(data=data,
                              item_class=item_class,
                              connection=self)

    def get_item(self, command, **kwargs):
        data = self._get_response(command=command, **kwargs)
        return data


def item_lister(command, connection, page_size, page_number, sort_by,
    sort_order, item_class, result_set, **kwargs):
    """
    A generator function for listing Video and Playlist objects.
    """
    page = page_number
    while True:
        print ">>>", connection
        itemCollection = connection.get_list(command,
                                             page_size=page_size,
                                             page_number=page,
                                             sort_by=sort_by,
                                             sort_order=sort_order,
                                             item_class=item_class,
                                             **kwargs)
        result_set.total_count = itemCollection.total_count
        result_set.page_number = page
        for item in itemCollection.items:
            yield item
        if itemCollection.total_count < 0 or itemCollection.page_size == 0:
            break  ## TODO: This doesn't seem right but is what happens when
                   ##       fetching a list less than a single page
        if len(itemCollection.items) > 0:
            page += 1
        else:
            break


class ItemResultSet(object):

    def __init__(self, command, item_class, connection=None, page_size=100,
            page_number=0, sort_by=DEFAULT_SORT_BY, sort_order=DEFAULT_SORT_ORDER, **kwargs):
        self.command = command
        if connection:
            self.connection = connection
        else:
            self.connection = APIConnection()
        self.page_size = page_size
        self.page_number = page_number
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.item_class = item_class
        self.kwargs = kwargs
        self.total_count = None

    def __iter__(self):
        return item_lister(self.command, self.connection, self.page_size,
            self.page_number, self.sort_by, self.sort_order, self.item_class,
            self, **self.kwargs)


class ItemCollection(object):

    def __init__(self, data, item_class, connection=None):
        self.total_count = None
        self.items = None
        self.page_number = None
        self.page_size = None
        self.items = []
        self.data = data

        self.total_count = int(data['total_count'])
        self.page_number = int(data['page_number'])
        self.page_size = int(data['page_size'])
        for item in data['items']:
            self.items.append(item_class(data=item, connection=connection))
