import urllib
import urllib2
import hashlib
import urlparse
import socket
import errno
import simplejson


from pybrightcove import config, UserAgent
from pybrightcove.multipart import MultipartPostHandler
from pybrightcove.exceptions import BrigthcoveClientError, BrightcoveError, BrigthcoveGeneralError
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
        
    def _post_request(self, data, file_to_upload=None):
        """
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),
                                      MultipartPostHandler.MultipartPostHandler)
        params = { "username" : "bob", "password" : "riviera",
                   "file" : open("filename", "rb") }
        opener.open("http://wwww.bobsite.com/upload/", params)
        """
        # opener = urllib2.build_opener(MultipartPostHandler)
        #         params = { "JSONRPC": simplejson.dumps(data), "file": open(file_to_upload, 'rb') }
        #         response = opener.open(self..url, params)
        
        response = None
        headers = {'User-Agent':UserAgent}
        if data:
            data = urllib.urlencode(data)            
            headers['Content-Length'] = len(data)
        try:
            request = urllib2.Request(url=self.url, headers=headers, data=simplejson.dumps(data))
            response = urllib2.urlopen(request)
            if response.code < 300:
                resp_data = simplejson.loads(response.read())
                if 'error' in resp_data:
                    raise BrightcoveError(resp_data)
                return resp_data
        except KeyboardInterrupt:
            sys.exit("Keyboard Interrupt")
        except Exception, e:
            pass
        
        if response:
            raise BrightcoveGeneralError(response.code, response.msg, response.read())
        elif e:
            raise e
        else:
            raise BrightcoveClientError("Please report this exception as an issue with pyfogbugz.")


    def create_video(self, filename, video=None, do_checksum=True, create_multiple_renditions=True, preserve_source_rendition=True):
        data = {"method":"create_video",
                "params": {"token": self.write_token,
                           "create_multiple_renditions": create_multiple_renditions,
                           "preserve_source_rendition": preserve_source_rendition}}
        if video:
            data['params']['video'] = video.to_data()
        if do_checksum:
            data['params']['file_checksum'] = hashlib.md5().update(open(filename).read()).hexdigest()
        r = self._post_request(data=data, file_to_upload=filename)
        return r

