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
import cookielib

from pybrightcove       import config, UserAgent
from pybrightcove.video import Video
    

class Connection(object):
    def __init__(self, read_token=None, write_token=None, read_url=None, write_url=None):
        if read_token:
            self.read_token = read_token
        elif config.has_option('Connection', 'read_token'):
            self.read_token = config.get('Connection', 'read_token')
        
        if write_token:
            self.write_token = write_token
        elif config.has_option('Connection', 'write_token'):
            self.write_token = config.get('Connection', 'write_token')
        
        if read_url:
            self.read_url = read_url
        elif config.has_option('Connection', 'read_url'):
            self.read_url = config.get('Connection', 'read_url')
        
        if write_url:
            self.write_url = write_url
        elif config.has_option('Connection', 'write_url'):
            self.write_url = config.get('Connection', 'write_url')
        
            
    def _post_file(self, data, file_to_upload):
        from pybrightcove.multipart import MultipartPostHandler
        cookies = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), MultipartPostHandler)
        params = { "JSONRPC" : simplejson.dumps(data), "filePath" : open(file_to_upload, "rb") }
        r = opener.open(self.write_url, params)
        print r.read()
        

    def create_video(self, filename, video, do_checksum=True, create_multiple_renditions=True, preserve_source_rendition=True):
        data = {
            "method":"create_video",
            "params": {
                "token": self.write_token, 
                "create_multiple_renditions": create_multiple_renditions,
                "preserve_source_rendition": preserve_source_rendition,
                "video": video.to_dict()
                }
            }
                
        if do_checksum:
            m = hashlib.md5()
            m.update(open(filename, 'rb').read())
            data['params']['file_checksum'] = m.hexdigest()
            
        r = self._post_file(data=data, file_to_upload=filename)
        return r

