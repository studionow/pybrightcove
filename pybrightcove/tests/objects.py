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

    def setUp(self):
        self.validTestDate = datetime(2009, 5, 27, 22, 58, 31)
        self.testDate = 1243483111000L
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
        self.video = Video(self.data)

    def test_serialization(self):
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

    def test_name(self):
        self.assertEqual(self.video.name, self.data['name'])

    def test_id(self):
        self.assertEqual(self.video.id, self.data['id'])

    def test_referenceId(self):
        self.assertEqual(self.video.referenceId, self.data['referenceId'])

    def test_accountId(self):
        self.assertEqual(self.video.accountId, self.data['accountId'])

    def test_shortDescription(self):
        self.assertEqual(self.video.shortDescription,
            self.data['shortDescription'])

    def test_longDescription(self):
        self.assertEqual(self.video.longDescription,
            self.data['longDescription'])

    def test_FLVURL(self):
        self.assertEqual(self.video.FLVURL, self.data['FLVURL'])

    def test_videoFullLength(self):
        self.assertEqual(self.video.videoFullLength, [])

    def test_creationDate(self):
        self.assertEqual(self.video.creationDate, self.validTestDate)

    def test_publishedDate(self):
        self.assertEqual(self.video.publishedDate, self.validTestDate)

    def test_lastModifiedDate(self):
        self.assertEqual(self.video.lastModifiedDate, self.validTestDate)

    def test_itemState(self):
        self.assertEqual(self.video.itemState, self.data['itemState'])

    def test_startDate(self):
        self.assertEqual(self.video.startDate, self.validTestDate)

    def test_endDate(self):
        self.assertEqual(self.video.endDate, self.validTestDate)

    def test_linkURL(self):
        self.assertEqual(self.video.linkURL, self.data['linkURL'])

    def test_linkText(self):
        self.assertEqual(self.video.linkText, self.data['linkText'])

    def test_tags(self):
        self.assertEqual(self.video.tags, [])

    def test_videoStillURL(self):
        self.assertEqual(self.video.videoStillURL, self.data['videoStillURL'])

    def test_thumbnailURL(self):
        self.assertEqual(self.video.thumbnailURL, self.data['thumbnailURL'])

    def test_length(self):
        self.assertEqual(self.video.length, self.data['length'])

    def test_geoFiltered(self):
        self.assertEqual(self.video.geoFiltered, self.data['geoFiltered'])

    def test_geoFilteredExclude(self):
        self.assertEqual(self.video.geoFilteredExclude,
            self.data['geoFilteredExclude'])

    def test_economics(self):
        self.assertEqual(self.video.economics, self.data['economics'])

    def test_playsTotal(self):
        self.assertEqual(self.video.playsTotal, self.data['playsTotal'])

    def test_playsTrailingWeek(self):
        self.assertEqual(self.video.playsTrailingWeek,
            self.data['playsTrailingWeek'])

    def test_renditions(self):
        self.assertEqual(self.video.renditions, [])

    def test_geoFilteredCountries(self):
        self.assertEqual(self.video.geoFilteredExclude,
            self.data['geoFilteredExclude'])

    def test_cuePoints(self):
        self.assertEqual(self.video.cuePoints, [])
