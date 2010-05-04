import unittest
import uuid
from datetime import datetime, timedelta
import pybrightcove
import mock


# httplib.HTTPConnection
# httplib.HTTPSConnection
# urllib2.urlopen
# tempfile.mkstemp
# ftplib.FTP

class APIConnectionTest(unittest.TestCase):

    def setUp(self):
        self.api = pybrightcove.APIConnection(read_token="read", write_token="write")

    def test_instantiate_valid(self):
        self.assertTrue(hasattr(self.api, "read_token"))
        self.assertTrue(hasattr(self.api, "write_token"))
        self.assertTrue(hasattr(self.api, "read_url"))
        self.assertTrue(hasattr(self.api, "write_url"))
        self.assertEquals(self.api.read_token, "read")
        self.assertEquals(self.api.write_token, "write")
        self.assertTrue(self.api.read_url.startswith('http'))
        self.assertTrue(self.api.write_url.startswith('http'))

    def test_instantiate_invalid(self):
        try:
            c = pybrightcove.APIConnection()
            self.fail("pybrightcove.exceptions.ImproperlyConfiguredError expected")
        except pybrightcove.exceptions.ImproperlyConfiguredError:
            pass

    @mock.patch('urllib2.urlopen')
    def test_post(self, UrlOpenMock):
        u = UrlOpenMock()
        u.read.return_value = '{"result": {"status": "OK"}}'
        d = self.api.post('get_upload_status', video_id=1000)
        self.assertEquals(d, {"status": "OK"})

    @mock.patch('httplib.HTTPConnection')
    @mock.patch('os.fstat')
    @mock.patch("__builtin__.file")
    def test_post_file(self, FileMock, FDStatMock, HTTPMock):
        h = HTTPMock()
        h.getresponse.return_value.read.return_value = '{"result": {"video": 1}}'
        FDStatMock.return_value = [0, 1, 2, 3, 4, 5, 1000]
        f = FileMock()
        f.name = 'bears.mov'
        f.read.return_value = ''
        video = pybrightcove.video.Video(filename='bears.mov', name='The Bears',
            short_description='Opening roll for an exciting soccer match.',
            connection=self.api)
        video.tags.append('unittest')
        vid = self.api.post('create_video', "bears.mov",
                create_multiple_renditions=True,
                preserve_source_rendition=True,
                encode_to=pybrightcove.enums.EncodeToEnum.FLV,
                video=video._to_dict())
        self.assertEquals(vid, {"video": 1})

    @mock.patch('urllib2.urlopen')
    def test_get_list(self, UrlOpenMock):
        u = UrlOpenMock()
        u.read.return_value = '{"result": {"status": "OK"}}'
        d = self.api.get_item('get_video', video_id=1000)
        self.assertEquals(d, {"result": {"status": "OK"}})

    @mock.patch('urllib2.urlopen')
    def test_get_item(self, UrlOpenMock):
        u = UrlOpenMock()
        
        u.read.return_value = '{"total_count": 5, "page_number": 2, "page_size": 10, "items":[]}'
        d = self.api.get_list('whatever_list', pybrightcove.Video, 10, 2, pybrightcove.enums.DEFAULT_SORT_BY, pybrightcove.enums.DEFAULT_SORT_ORDER)
        self.assertEquals(d.data, {"total_count": 5, "page_number": 2, "page_size": 10, "items":[]})
        self.assertEquals(d.page_size, 10)
        self.assertEquals(d.total_count, 5)
        self.assertEquals(d.page_number, 2)

