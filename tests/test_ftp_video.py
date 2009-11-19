
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

from xml.dom import minidom
import unittest
import mock
from pybrightcove import Video, enums, FTPConnection


class FTPVideoTest(unittest.TestCase):

    @mock.patch('ftplib.FTP')
    @mock.patch('hashlib.md5') # md5(), md5.hexdigest
    @mock.patch('os.path.getsize')
    @mock.patch('__builtin__.file')
    def test_batch_provision_video(self, OpenMockClass, GetSizeMockClass,
        Md5MockClass, FTPMockClass):
        o = OpenMockClass()
        o.read.return_value = None
        m = Md5MockClass()
        m.hexdigest.return_value = 'a78fa9f8asd'
        GetSizeMockClass.return_value = 10000
        f = FTPMockClass()

        ftp = FTPConnection(host='host',
                            user='user',
                            password='pass',
                            publisher_id='111111111',
                            preparer='Patrick',
                            report_success=True)
        v = Video(name="Some title",
                  reference_id='a532kallk3252a',
                  short_description="A short description.",
                  connection=ftp)
        v.long_description = "An even longer description"
        v.tags.extend(["blah", "nah", "tag"])
        v.add_asset('1500.flv',
                enums.AssetTypeEnum.VIDEO_FULL, 'High quality rendition',
                encoding_rate=1500000, frame_width=640,
                frame_height=360)
        v.add_asset('700.flv',
                enums.AssetTypeEnum.VIDEO_FULL, 'Medium quality rendition',
                encoding_rate=700000, frame_width=640,
                frame_height=360)
        v.add_asset('poster.png',
                enums.AssetTypeEnum.VIDEO_STILL, 'Poster frame',
                frame_width=640, frame_height=360)
        v.save()

        self.assertEqual('login', f.method_calls[0][0])
        self.assertEqual('set_pasv', f.method_calls[1][0])
        self.assertEqual('storbinary', f.method_calls[2][0])
        self.assertEqual('STOR 1500.flv', f.method_calls[2][1][0])

        self.assertEqual('login', f.method_calls[3][0])
        self.assertEqual('set_pasv', f.method_calls[4][0])
        self.assertEqual('storbinary', f.method_calls[5][0])
        self.assertEqual('STOR 700.flv', f.method_calls[5][1][0])

        self.assertEqual('login', f.method_calls[6][0])
        self.assertEqual('set_pasv', f.method_calls[7][0])
        self.assertEqual('storbinary', f.method_calls[8][0])
        self.assertEqual('STOR poster.png', f.method_calls[8][1][0])

        self.assertEqual('write', o.method_calls[6][0])
        valid_xml = minidom.parse(
            open('test_ftp_video_batch_provision_manifest.xml', 'rb'))
        test_xml = minidom.parseString(o.method_calls[6][1][0])
        self.assertEqual(
            valid_xml.toxml().replace('\t', '').replace('\n', ''),
            test_xml.toxml().replace('\t', '').replace('\n', ''))

    @mock.patch('ftplib.FTP')
    @mock.patch('hashlib.md5')
    @mock.patch('os.path.getsize')
    @mock.patch('__builtin__.file')
    def test_batch_provision_with_custom_metadata_video(self, OpenMockClass, 
        GetSizeMockClass, Md5MockClass, FTPMockClass):
        o = OpenMockClass()
        o.read.return_value = None
        m = Md5MockClass()
        m.hexdigest.return_value = 'a78fa9f8asd'
        GetSizeMockClass.return_value = 10000
        f = FTPMockClass()

        ftp = FTPConnection(host='host',
                            user='user',
                            password='pass',
                            publisher_id='111111111',
                            preparer='Patrick',
                            report_success=True)
        v = Video(name="Some title",
                  reference_id='a532kallk3252a',
                  short_description="A short description.",
                  connection=ftp)
        v.long_description = "An even longer description"
        v.tags.extend(["blah", "nah", "tag"])
        v.add_asset('1500.flv',
                enums.AssetTypeEnum.VIDEO_FULL, 'High quality rendition',
                encoding_rate=1500000, frame_width=640,
                frame_height=360)
        v.add_asset('700.flv',
                enums.AssetTypeEnum.VIDEO_FULL, 'Medium quality rendition',
                encoding_rate=700000, frame_width=640,
                frame_height=360)
        v.add_asset('poster.png',
                enums.AssetTypeEnum.VIDEO_STILL, 'Poster frame',
                frame_width=640, frame_height=360)

        v.add_custom_metadata("enum_one", "Value One", enums.CustomMetaType.ENUM)
        v.add_custom_metadata("enum_two", "Value Two", enums.CustomMetaType.ENUM)
        v.add_custom_metadata("key_one", "String Value One", enums.CustomMetaType.STRING)
        v.add_custom_metadata("key_two", "String Value Two", enums.CustomMetaType.STRING)
        v.save()

        self.assertEqual('login', f.method_calls[0][0])
        self.assertEqual('set_pasv', f.method_calls[1][0])
        self.assertEqual('storbinary', f.method_calls[2][0])
        self.assertEqual('STOR 1500.flv', f.method_calls[2][1][0])

        self.assertEqual('login', f.method_calls[3][0])
        self.assertEqual('set_pasv', f.method_calls[4][0])
        self.assertEqual('storbinary', f.method_calls[5][0])
        self.assertEqual('STOR 700.flv', f.method_calls[5][1][0])

        self.assertEqual('login', f.method_calls[6][0])
        self.assertEqual('set_pasv', f.method_calls[7][0])
        self.assertEqual('storbinary', f.method_calls[8][0])
        self.assertEqual('STOR poster.png', f.method_calls[8][1][0])

        self.assertEqual('write', o.method_calls[6][0])
        valid_xml = minidom.parse(
            open('test_ftp_video_batch_provision_with_custom_metadata_manifest.xml', 'rb'))
        test_xml = minidom.parseString(o.method_calls[6][1][0])
        self.assertEqual(
            valid_xml.toxml().replace('\t', '').replace('\n', ''),
            test_xml.toxml().replace('\t', '').replace('\n', ''))

