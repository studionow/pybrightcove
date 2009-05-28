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

"""
Test the Media API Objects:
- Video
- Playlist
- CuePoint
- Rendition
- Image
"""

import unittest
from datetime import datetime
from pybrightcove.video import Video
from pybrightcove.enums import ItemStateEnum, EconomicsEnum


class VideoTest(unittest.TestCase):
    ## datetime.datetime(2009, 5, 27, 22, 58, 31, 711678)
    testDate = 1243483111000L

    def setUp(self):
        self.data = {
            'name': "Test Video",
            'id': 23424245,
            'referenceId': 'MY REFERENCE ID',
            'accountId': 'AXafalj3lkafd',
            'shortDescription': "The quick brown fox.",
            'longDescription': "my long description",
            'FLVURL': "http://myflvurl.com",
            'creationDate': self.testDate,
            'publishedDate': self.testDate,
            'lastModifiedDate': self.testDate,
            'startDate': self.testDate,
            'itemState': ItemStateEnum.ACTIVE,
            'endDate': self.testDate,
            'linkURL': 'http://linkurl.com',
            'linkText': 'My link text',
            'tags': None,
            'videoStillURL': 'http://stillurl.com',
            'thumbnailURL': 'http://thumburl.com',
            'length': 30000,
            'economics': EconomicsEnum.FREE,
            'geoFiltered': False,
            'geoFilteredExclude': False,
            'geoFilteredCountries': ['us', ],
            'playsTotal': 50,
            'playsTrailingWeek': 7}

    def test_deserialization(self):
        v = Video(data=self.data)
        new_dict = v.to_dict()
        dt = datetime(2009, 5, 27, 22, 58, 31)
        for key in new_dict.keys():
            if key in self.data:
                if self.data[key] == self.testDate:
                    self.assertEqual(new_dict[key], dt)
                elif key == 'tags':
                    self.assertEqual(new_dict[key], [])
                else:
                    self.assertEqual(new_dict[key], self.data[key])

    def test_serialization(self):
        pass

    def test_name(self):
        pass

    def test_id(self):
        pass

    def test_referenceId(self):
        pass

    def test_accountId(self):
        pass

    def test_shortDescription(self):
        pass

    def test_longDescription(self):
        pass

    def test_FLVURL(self):
        pass

    def test_videoFullLength(self):
        pass

    def test_creationDate(self):
        pass

    def test_publishedDate(self):
        pass

    def test_lastModifiedDate(self):
        pass

    def test_itemState(self):
        pass

    def test_startDate(self):
        pass

    def test_endDate(self):
        pass

    def test_linkURL(self):
        pass

    def test_linkText(self):
        pass

    def test_tags(self):
        pass

    def test_videoStillURL(self):
        pass

    def test_thumbnailURL(self):
        pass

    def test_length(self):
        pass

    def test_geoFiltered(self):
        pass

    def test_geoFilteredExclude(self):
        pass

    def test_economics(self):
        pass

    def test_playsTotal(self):
        pass

    def test_playsTrailingWeek(self):
        pass

    def test_renditions(self):
        pass

    def test_geoFilteredCountries(self):
        pass

    def test_cuePoints(self):
        pass
