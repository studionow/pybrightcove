import hashlib
import simplejson
import urllib2

from pybrightcove.multipart import MultipartPostHandler
from pybrightcove import config, UserAgent
from pybrightcove.exceptions import BrightcoveClientError, BrightcoveError, BrightcoveGeneralError
from pybrightcove.video import Video
from pybrightcove.playlist import Playlist


    

class Connection(object):
    def __init__(self, url=None, read_token=None, write_token=None):
        if url:
            self.url = url
        elif config.has_option('Connection', 'url'):
            self.url = config.get('Connection', 'url')
        
        if read_token:
            self.read_token = read_token
        elif config.has_option('Connection', 'read_token'):
            self.read_token = config.get('Connection', 'read_token')
        
        if write_token:
            self.write_token = write_token
        elif config.has_option('Connection', 'write_token'):
            self.write_token = config.get('Connection', 'write_token')
            
    def _post_file(self, data, file_to_upload):
        opener = urllib2.build_opener(MultipartPostHandler)
        params = { "JSONRPC" : simplejson.dumps(data), "filePath" : open(file_to_upload, "rb") }
        r = opener.open("http://api.brightcove.com/services/post", params)
        print r.read()
        

    def create_video(self, filename, video=None, do_checksum=True, create_multiple_renditions=True, preserve_source_rendition=True):
        data = {"method":"create_video",
                "params": {
                    "token": self.write_token, 
                    "create_multiple_renditions": create_multiple_renditions,
                    "preserve_source_rendition": preserve_source_rendition
                    }
                }
        if video:
            data['params']['video'] = video.to_dict()
        if do_checksum:
            m = hashlib.md5()
            m.update(open(filename, 'rb').read())
            data['params']['file_checksum'] = m.hexdigest()
        r = self._post_file(data=data, file_to_upload=filename)
        return r

