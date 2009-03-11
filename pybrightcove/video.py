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

from datetime import datetime
from pybrightcove.enums import EconomicsEnum


def _convert_tstamp(val):
    if val:
        return datetime.fromtimestamp(float(val)/1000)


class Rendition(object):

    def __init__(self, data=None):
        self._url = None
        self._encodingRate = None
        self._frameHeight = None
        self._frameWidth = None
        self._size = None

        if data:
            self._url = data['url']
            self._encodingRate = data['encodingRate']
            self._frameHeight = data['frameHeight']
            self._frameWidth = data['frameWidth']
            self._size = data['size']

    def get_url(self):
        return self._url

    def get_encodingRate(self):
        return self._encodingRate

    def get_frameHeight(self):
        return self._frameHeight

    def get_frameWidth(self):
        return self._frameWidth

    def get_size(self):
        return self._size

    url = property(get_url,
        doc="The URL of the rendition file.")
    encodingRate = property(get_encodingRate,
        doc="The rendition's encoding rate in bits per second.")
    frameHeight = property(get_frameHeight,
        doc="The rendition's display height, in pixels.")
    frameWidth = property(get_frameWidth,
        doc="The rendition's display width, in pixels.")
    size = property(get_size,
        doc="The file size of the rendition, in bytes.")


class CuePoint(object):

    def __init__(self, data=None):
        self._name = None
        self._video_id = None
        self._time = None
        self._forceStop = None
        self._type = None
        self._metadata = None

        if data:
            self.name = data['name']
            self._video_id = data['video_id']
            self._time = data['time']
            self.forceStop = data['forceStop']
            self._type = data['type']
            self.metadata = data['metadata']

    def get_name(self):
        return self._name

    def get_video_id(self):
        return self._video_id

    def get_time(self):
        return self._time

    def get_forceStop(self):
        return self._forceStop

    def set_forceStop(self, force_stop):
        self._forceStop = force_stop

    def get_type(self):
        return self._type

    def get_metadata(self):
        return self._metadata

    def set_metadata(self, meta):
        self._metadata = meta

    name = property(get_name,
        doc = "A name for the cue point, so that you can refer to it.")
    video_id = property(get_video_id,
        doc = """A comma-separated list of the ids of one or more videos
                that this cue point applies to.""")
    time = property(get_time,
        doc = """The time of the cue point, measured in milliseconds from
                the beginning of the video.""")
    forceStop = property(get_forceStop, set_forceStop,
        doc = """If true, the video stops playback at the cue point. This
                setting is valid only for AD type cue points.""")
    cue_type = property(get_type,
        doc = """An integer code corresponding to the type of cue point.
                One of 0 (AD), 1 (CODE), or 2 (CHAPTER). An AD cue point
                is used to trigger mid-roll ad requests. A CHAPTER cue
                point indicates a chapter or scene break in the video.
                A CODE cue point causes an event that you can listen
                for and respond to.""")
    metadata = property(get_metadata, set_metadata,
        doc = "A string that can be passed along with a CODE cue point.")


class Video(object):

    def __init__(self, data=None):
        self._name = None
        self._id = None
        self._referenceId = None
        self._accountId = None
        self._shortDescription = None
        self._longDescription = None
        self._FLVURL = None
        self._renditions = None
        self._creationDate = None
        self._publishedDate = None
        self._lastModifiedDate = None
        self._startDate = None
        self._endDate = None
        self._linkURL = None
        self._linkText = None
        self._tags = None
        self._videoStillURL = None
        self._thumbnailURL = None
        self._length = None
        self._economics = None
        self._cuePoints = None
        self._playsTotal = None
        self._playsTrailingWeek = None

        if data:
            self.name = data.get('name', None)
            self._id = data.get('id', None)
            self.referenceId = data.get('referenceId', None)
            self._accountId = data.get('accountId', None)
            self.shortDescription = data.get('shortDescription', None)
            self.longDescription = data.get('longDescription', None)
            self._FLVURL = data.get('FLVURL', None)
            self._creationDate = _convert_tstamp(
                data.get('creationDate', None))
            self._publishedDate = _convert_tstamp(
                data.get('publishedDate', None))
            self._lastModifiedDate = _convert_tstamp(
                data.get('lastModifiedDate', None))
            self._startDate = _convert_tstamp(data.get('startDate', None))
            self._endDate = _convert_tstamp(data.get('endDate', None))
            self.linkURL = data.get('linkURL', None)
            self.linkText = data.get('linkText', None)
            self.tags = data.get('tags', None)
            self._videoStillURL = data.get('videoStillURL', None)
            self._thumbnailURL = data.get('thumbnailURL', None)
            self._length = data.get('length', None)
            self.economics = data.get('economics', None)
            self._playsTotal = data.get('playsTotal', None)
            self._playsTrailingWeek = data.get('playsTrailingWeek', None)

            for rendition in data.get('renditions', []):
                self.renditions.append(Rendition(data=rendition))
            for cuePoint in data.get('cuePoints', []):
                self.cuePoints.append(CuePoint(data=cuePoint))

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name[:60]

    def get_id(self):
        return self._id

    def get_referenceId(self):
        return self._referenceId

    def set_referenceId(self, refid):
        if refid:
            self._referenceId = refid[:150]

    def get_accountId(self):
        return self._accountId

    def get_shortDescription(self):
        return self._shortDescription

    def set_shortDescription(self, desc):
        if desc:
            self._shortDescription = desc[:250]

    def get_longDescription(self):
        return self._longDescription

    def set_longDescription(self, desc):
        if desc:
            self._longDescription = desc[:5000]

    def get_flvurl(self):
        return self._FLVURL

    def get_renditions(self):
        if self._renditions == None:
            self._renditions = []
        return self._renditions

    def set_renditions(self, renditions):
        self._renditions = renditions

    def get_creationDate(self):
        return self._creationDate

    def get_publishedDate(self):
        return self._publishedDate

    def get_lastModifiedDate(self):
        return self._lastModifiedDate

    def get_startDate(self):
        return self._startDate

    def get_endDate(self):
        return self._endDate

    def get_linkURL(self):
        return self._linkURL

    def set_linkURL(self, url):
        self._linkURL = url

    def get_linkText(self):
        return self._linkText

    def set_linkText(self, text):
        self._linkText = text

    def get_tags(self):
        if self._tags == None:
            self._tags = []
        return self._tags

    def set_tags(self, tags):
        self._tags = tags

    def get_videoStillURL(self):
        return self._videoStillURL

    def get_thumbnailURL(self):
        return self._thumbnailURL

    def get_length(self):
        return self._length

    def get_economics(self):
        return self._economics

    def set_economics(self, model):
        if model not in (EconomicsEnum.FREE, EconomicsEnum.AD_SUPPORTED):
            self._economics = EconomicsEnum.FREE
        else:
            self._economics = model

    def get_cuePoints(self):
        if self._cuePoints == None:
            self._cuePoints = []
        return self._cuePoints

    def set_cuePoints(self, points):
        self._cuePoints = points

    def get_playsTotal(self):
        return self._playsTotal

    def get_playsTrailingWeek(self):
        return self._playsTrailingWeek


    name = property(get_name, set_name,
        doc = """The title of this Video. The name is a required property when
            you create a video.""")
    id = property(get_id,
        doc = """A number that uniquely identifies this Video, assigned by
            Brightcove when the Video is created.""")
    referenceId = property(get_referenceId, set_referenceId,
        doc = """A user-specified id that uniquely identifies this Video.
            ReferenceID can be used as a foreign-key to identify this video
            in another system.""")
    accountId = property(get_accountId,
        doc = """A number, assigned by Brightcove, that uniquely identifies
            the account to which this Video belongs.""")
    shortDescription = property(get_shortDescription, set_shortDescription,
        doc = """A short description describing this Video, limited to 256
            characters. The shortDescription is a required property when you
            create a video.""")
    longDescription = property(get_longDescription, set_longDescription,
        doc = """A longer description of this Video, limited to 5000
            characters.""")
    FLVURL = property(get_flvurl,
        doc = """The URL of the video file for this Video. Note that this
            property can be accessed with the Media API only with a special
            read or write token. See Accessing Video Content with the Media
            API.""")
    renditions = property(get_renditions, set_renditions,
        doc = """An array of Renditions that represent the dynamic delivery
            renditions available for this Video.""")
    creationDate = property(get_creationDate,
        doc = """The date this Video was created, represented as the number
            of milliseconds since the Unix epoch.""")
    publishedDate = property(get_publishedDate,
        doc = """The date this Video was last made active, represented as the
            number of milliseconds since the Unix epoch.""")
    lastModifiedDate = property(get_lastModifiedDate,
        doc = """The date this Video was last modified, represented as the
            number of milliseconds since the Unix epoch.""")
    startDate = property(get_startDate,
        doc = """The first date this Video is available to be played,
            represented as the number of milliseconds since the Unix epoch.""")
    endDate = property(get_endDate,
        doc = """The last date this Video is available to be played,
            represented as the number of milliseconds since the Unix epoch.""")
    linkURL = property(get_linkURL, set_linkURL,
        doc = """An optional URL to a related item.""")
    linkText = property(get_linkText, set_linkText,
        doc = """The text displayed for the linkURL.""")
    tags = property(get_tags, set_tags,
        doc = """A list of Strings representing the tags assigned to this
            Video.""")
    videoStillURL = property(get_videoStillURL,
        doc = """The URL to the video still image associated with this
            Video. Video stills are 480x360 pixels.""")
    thumbnailURL = property(get_thumbnailURL,
        doc = """The URL to the thumbnail image associated with this Video.
            Thumbnails are 120x90 pixels.""")
    length = property(get_length,
        doc = "The length of this video in milliseconds.")
    economics = property(get_economics, set_economics,
        doc = """Either FREE or AD_SUPPORTED. AD_SUPPORTED means that ad
            requests are enabled for this Video.""")
    cuePoints = property(get_cuePoints, set_cuePoints,
        doc = """A List of the CuePoints objects assigned to this Video.""")
    playsTotal = property(get_playsTotal,
        doc = """How many times this Video has been played since its
            creation.""")
    playsTrailingWeek = property(get_playsTrailingWeek,
        doc = """How many times this Video has been played within the past
            seven days, exclusive of today.""")

    def to_dict(self):
        data = {
            'name': self.name,
            'id': self.id,
            'referenceId': self.referenceId,
            'accountId': self.accountId,
            'shortDescription': self.shortDescription,
            'longDescription': self.longDescription,
            'FLVURL': self.FLVURL,
            'renditions': self.renditions,
            'creationDate': self.creationDate,
            'publishedDate': self.publishedDate,
            'lastModifiedDate': self.lastModifiedDate,
            'startDate': self.startDate,
            'endDate': self.endDate,
            'linkURL': self.linkURL,
            'linkText': self.linkText,
            'tags': self.tags,
            'videoStillURL': self.videoStillURL,
            'thumbnailURL': self.thumbnailURL,
            'length': self.length,
            'economics': self.economics,
            'cuePoints': self.cuePoints,
            'playsTotal': self.playsTotal,
            'playsTrailingWeek': self.playsTrailingWeek}
        for key in data.keys():
            if data[key] == None:
                data.pop(key)
        return data
