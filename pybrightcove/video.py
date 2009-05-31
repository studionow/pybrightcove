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
from pybrightcove import PyBrightcoveError
from pybrightcove import SortByType, EconomicsEnum, SortByOrderType
from pybrightcove import VideoCodecEnum, ItemStateEnum
from pybrightcove import Connection, ItemResultSet


def _convert_tstamp(val):
    if val:
        return datetime.fromtimestamp(float(val)/1000)


class Image(object):
    """
    This object represents metadata about an image file in your account. Images
    are associated with videos as thumbnail images or video still images. An
    image can be a JPEG, GIF, or PNG-formatted image. Note that when creating a
    new image asset, the only property that is required is type. If you are not
    uploading a file, the remoteUrl property is also required.

    For more information, see Adding Images to Videos with the Media API [1].

    [1] http://help.brightcove.com/developer/docs/mediaapi/add_image.cfm
    """

    def __init__(self, data=None, **kwargs):
        self.id = kwargs.get('id', None)
        self.reference_id = kwargs.get('reference_id', None)
        self.type = kwargs.get('type', None)
        self.remote_url = kwargs.get('remote_url', None)
        self.display_name = kwargs.get('display_name', None)

        if data:
            self.id = data['id']
            self.reference_id = data['referenceId']
            self.type = data['type']
            self.remote_url = data["remoateUrl"]
            self.display_name = data["displayName"]

    def to_dict(self):
        data = {
            'id': self.id,
            'referenceId': self.reference_id,
            'type': self.type,
            'displayName': self.display_name,
            'remoateUrl': self.remote_url}
        for key in data.keys():
            if data[key] == None:
                data.pop(key)
        return data


class Rendition(object):
    """
    The Rendition object represents one of the dynamic delivery renditions of a
    video. A Video should have not more than 10 Renditions.

    For more information, see Using dynamic delivery [1] and Creating videos
    for dynamic delivery [2].

    [1] http://help.brightcove.com/publisher/docs/media/mbr.cfm
    [2] http://help.brightcove.com/developer/docs/mediaapi/create-mbr.cfm
    """

    def __init__(self, data=None):
        self._url = None
        self._encodingRate = None
        self._frameHeight = None
        self._frameWidth = None
        self._size = None
        self._remoteUrl = None
        self._remoteStreamName = None
        self._videoDuration = None
        self._videoCodec = None

        if data:
            self._url = data['url']
            self._encodingRate = data['encodingRate']
            self._frameHeight = data['frameHeight']
            self._frameWidth = data['frameWidth']
            self._size = data['size']
            self._remoteUrl = data['remoteUrl']
            self._remoteStreamName = data['remoteStreamName']
            self._videoDuration = data['videoDuration']
            self._videoCodec = data['videoCodec']

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

    def get_remoteUrl(self):
        return self._remoteUrl

    def set_remoteUrl(self, url):
        self._remoteUrl = url

    def get_remoteStreamName(self):
        return self._remoteStreamName

    def set_remoteStreamName(self, stream_name):
        self._remoteStreamName = stream_name

    def get_videoDuration(self):
        return self._videoDuration

    def set_videoDuration(self, duration):
        self._videoDuration = duration

    def get_videoCodec(self):
        return self._videoCodec

    def set_videoCodec(self, codec):
        if codec not in (VideoCodecEnum.SORENSON, VideoCodecEnum.ON2,
            VideoCodecEnum.H264):
            raise TypeError("Valid values are SORENSON, ON2, or H264.")
        self._videoCodec = codec

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

    remoteUrl = property(get_remoteUrl, set_remoteUrl,
        doc="""Required, for remote assets. The complete path to the file
            hosted on the remote server. If the file is served using
            progressive download, then you must include the file name and
            extension for the file. You can also use a URL that re-directs
            to a URL that includes the file name and extension. If the file
            is served using Flash streaming, use the remoteStreamName
            attribute to provide the stream name.""")

    remoteStream = property(get_remoteStreamName, set_remoteStreamName,
        doc="""[Optional - required for streaming remote assets only] A stream
            name for Flash streaming appended to the value of the remoteUrl
            property.""")

    videoDuration = property(get_videoDuration, set_videoDuration,
        doc="Required. The length of the remote video asset in milliseconds.")

    videoCodec = property(get_videoCodec, set_videoCodec,
        doc="Required. Valid values are SORENSON, ON2, and H264.")

    def to_dict(self):
        data = {
            'url': self.url,
            'encodingRate': self.encodingRate,
            'frameHeight': self.frameHeight,
            'frameWidth': self.frameWidth,
            'size': self.size,
            'remoteUrl': self.remoteUrl,
            'remoteStream': self.remoteStream}
        for key in data.keys():
            if data[key] == None:
                data.pop(key)
        return data


class CuePoint(object):
    """
    The CuePoint object is a marker set at a precise time point in the duration
    of a video. You can use cue points to trigger mid-roll ads or to separate
    chapters or scenes in a long-form video.

    For more information, see Setting CuePoints with the Media API [1].

    [1] http://help.brightcove.com/developer/docs/mediaapi/cue-points.cfm
    """

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

    def to_dict(self):
        data = {
            'name': self.name,
            'video_id': self.video_id,
            'time': self.time,
            'forceStop': self.forceStop,
            'cue_type': self.cue_type}
        for key in data.keys():
            if data[key] == None:
                data.pop(key)
        return data


class Video(object):
    """
    The Video object is an aggregation of metadata and asset information
    associated with a video.

    id
        A number that uniquely identifies this Video, assigned by Brightcove
        when the Video is created.

    reference_id
        A user-specified id that uniquely identifies this Video.  The
        reference_id can be used as a foreign-key to identify this video in
        another system.

    name
        The title of this Video. The name is a required property when you
        create a video.

    account_id
        A number, assigned by Brightcove, that uniquely identifies the account
        to which this Video belongs.

    short_description
        A short description describing this Video, limited to 256 characters.
        The short_description is a required property when you create a video.

    long_description
        A longer description of this Video, limited to 5000 characters.

    flv_url
        The URL of the video file for this Video. Note that this property can
        be accessed with the Media API only with a special read or write token.

    renditions
        An array of Renditions that represent the dynamic delivery renditions
        available for this Video.

    video_full_length
        A single Rendition that represents the the video file for this Video.
        Note that this property can be accessed with the Media API only with
        a special read or write token.

    creation_date
        The date this Video was created.

    published_date
        The date this Video was last made active.

    last_modified_date
        The date this Video was last modified.

    item_state
        An ItemStateEnum. One of ACTIVE, INACTIVE, or DELETED. You can set this
        property only to ACTIVE or INACTIVE; you cannot delete a video by
        setting its itemState to DELETED.

    start_date
        The first date this Video is available to be played.

    end_date
        The last date this Video is available to be played.

    link_url
        An optional URL to a related item.

    link_text
        The text displayed for the linkURL.

    tags
        A list of Strings representing the tags assigned to this Video.

    video_still_url
        The URL to the video still image associated with this Video. Video
        stills are 480x360 pixels.

    thumbnail_url
        The URL to the thumbnail image associated with this Video. Thumbnails
        are 120x90 pixels.

    length
        The length of this video in milliseconds.

    economics
        Either FREE or AD_SUPPORTED. AD_SUPPORTED means that ad requests are
        enabled for this Video.

    geo_filtered
        True indicates that the video is geo-restricted.

    geo_filtered_countries
        A list of the ISO-3166 two-letter codes of the countries to enforce
        geo-restriction rules on. Use lowercase for the country codes.

    geo_filtered_exclude
        If true, the video can be viewed in all countries except those listed
        in geo_filtered_countries; if false, the video can be viewed only in
        the countries listed in geo_filtered_countries.

    cue_points
        A List of the CuePoints objects assigned to this Video.

    plays_total
        How many times this Video has been played since its creation.

    plays_trailing_week
        How many times this Video has been played within the past seven days,
        exclusive of today.
    """

    def __init__(self, filename=None, name=None, short_description=None,
        id=None, reference_id=None, data=None, connection=None):

        self._filename = None
        self.name = None
        self.short_description = None
        self.id = None
        self.reference_id = None
        self.accountId = None
        self.long_description = None
        self.flv_url = None
        self.renditions = []
        self.video_full_length = None
        self.creation_date = None
        self.published_date = None
        self.last_modified_date = None
        self.item_state = None
        self.start_date = None
        self.end_date = None
        self.link_url = None
        self.link_text = None
        self.tags = []
        self.video_still_url = None
        self.thumbnail_url = None
        self.length = None
        self.economics = None
        self.geo_filtered = None
        self.geo_filtered_countries = None
        self.geo_filtered_exclude = None
        self.cue_points = None
        self.plays_total = None
        self.plays_trailing_week = None

        self.image = None

        self.connection = connection
        if not self.connection:
            self.connection = Connection()

        if filename and name and short_description:
            self._filename = filename
            self.name = name
            self.short_description = short_description
        elif id or reference_id:
            self.id = id
            self.reference_id = reference_id
            self._find_video()
        elif data:
            self._load(data)
        else:
            raise PyBrightcoveError('Invalid parameters for Video.')

    def _find_video(self):
        data = None
        if self.id:
            data = self.connection.get_item(
                'find_video_by_id', video_id=self.id)
        elif self.reference_id:
            data = self.connection.get_item(
                'find_video_by_reference_id', reference_id=self.reference_id)

        if data:
            self._load(data)

    def _to_dict(self):
        data = {
            'name': self.name,
            'referenceId': self.reference_id,
            'shortDescription': self.short_description,
            'longDescription': self.long_description,
            'itemState': self.item_state,
            'linkURL': self.link_url,
            'linkText': self.link_text,
            'tags': self.tags,
            'economics': self.economics,

            # TODO: Don't support the saving/updating of these values yet.
            #'geoFiltered': self.geo_filtered,
            #'geoFilteredCountries': self.geo_filtered_countries,
            #'geoFilteredExclude': self.geo_filtered_exclude,
            #'cuePoints': self.cue_points,
            #'renditions': self.renditions,
            #'videoFullLength': self.video_full_length
        }
        [data.pop(key) for key in data.keys() if data[key] == None]
        return data

    def _load(self, data):
        self.creation_date = _convert_tstamp(data['creationDate'])
        self.economics = data['economics']
        self.id = data['id']
        self.last_modified_date = _convert_tstamp(data['lastModifiedDate'])
        self.length = data['length']
        self.link_text = data['linkText']
        self.link_url = data['linkURL']
        self.long_description = data['longDescription']
        self.name = data['name']
        self.plays_total = data['playsTotal']
        self.plays_trailing_week = data['playsTrailingWeek']
        self.published_date = _convert_tstamp(data['publishedDate'])
        self.reference_id = data['referenceId']
        self.short_description = data['shortDescription']
        self.tags = []
        for tag in data['tags']:
            self.tags.append(tag)
        self.thumbnail_url = data['thumbnailURL']
        self.video_still_url = data['videoStillURL']

    def __setattr__(self, name, value):
        msg = None
        if value:
            if name == 'name' and len(value) > 60:
                # val = value[:60] ## Is this better?
                msg = "Video.name must be 60 characters or less."
            if name == 'reference_id' and len(value) > 150:
                # val = value[:150]
                msg = "Video.reference_id must be 150 characters or less."
            if name == 'long_description' and len(value) > 5000:
                # val = value[:5000]
                msg = "Video.long_description must be 5000 characters or less."
            if name == 'short_description' and len(value) > 250:
                # val = value[:250]
                msg = "Video.short_description must be 250 characters or less."
            if name == 'item_state' and value not in (ItemStateEnum.ACTIVE,
                                                      ItemStateEnum.INACTIVE):
                msg = "Video.item_state must be either ItemStateEnum.ACTIVE or"
                msg += " ItemStateEnum.INACTIVE"
            if name == 'video_full_length' and \
                    not isinstance(value, Rendition):
                msg = "Video.video_full_length must be of type Rendition"
            if name == 'economics' and \
                    value not in (EconomicsEnum.FREE,
                                  EconomicsEnum.AD_SUPPORTED):
                msg = "Video.economics must be either EconomicsEnum.FREE or "
                msg += "EconomicsEnum.AD_SUPPORTED"

            if msg:
                raise PyBrightcoveError(msg)
        return super(Video, self).__setattr__(name, value)

    def save(self):
        """
        Creates or updates the video
        """
        if not self.id and self._filename:
            self.id = self.connection.post('create_video', self._filename,
                create_multiple_renditions=True,
                preserve_source_rendition=True,
                video=self._to_dict())
        elif self.id:
            data = self.connection.post('update_video', video=self._to_dict())
            if data:
                self._load(data)

    def delete(self, cascade=False, delete_shares=False):
        if self.id:
            self.connection.post('delete_video', video_id=self.id,
                cascade=cascade, delete_shares=delete_shares)
            self.id = None ## Prevent more activity on this video id

    def get_upload_status(self):
        if self.id:
            return self.connection.post('get_upload_status', video_id=self.id)

    def share(self, accounts):
        if not isinstance(accounts, (list, tuple)):
            raise PyBrightcoveError("Video.share expects an iterable argument")
        raise PyBrightcoveError("Not yet implemented")

    def set_image(self, image, filename=None, resize=True):
        if self.id:
            data = self.connection.post('add_image', filename,
                video_id=self.id, image=image.to_dict(), resize=resize)
            if data:
                self.image = Image(data=data)

    def find_releated(self):
        raise PyBrightcoveError("Not yet implemented")

    @staticmethod
    def find_all(connection=None, page_size=100, page_number=0,
        sort_by=SortByType.CREATION_DATE, sort_order=SortByOrderType.ASC):
        return ItemResultSet('find_all_videos', Video, connection, page_size,
            page_number, sort_by, sort_order)

    @staticmethod
    def find_by_tags(and_tags=None, or_tags=None):
        err = None
        if not and_tags and not or_tags:
            err = "You must supply at least one of either and_tags or or_tags."
        if and_tags and not isinstance(and_tags, (tuple, list)):
            err = "The and_tags argument for Video.find_by_tags must an "
            err += "iterable"
        if or_tags and not isinstance(or_tags, (tuple, list)):
            err = "The or_tags argument for Video.find_by_tags must an "
            err += "iterable"
        if err:
            raise PyBrightcoveError(err)
        raise PyBrightcoveError("Not yet implemented")

    @staticmethod
    def find_by_text(text):
        raise PyBrightcoveError("Not yet implemented")

    @staticmethod
    def find_by_campaign(campaign_id):
        raise PyBrightcoveError("Not yet implemented")

    @staticmethod
    def find_by_user(user_id):
        raise PyBrightcoveError("Not yet implemented")

    @staticmethod
    def find_by_reference_ids(reference_ids):
        if not isinstance(reference_ids, (list, tuple)):
            err = "Video.find_by_reference_ids expects an iterable argument"
            raise PyBrightcoveError(err)
        raise PyBrightcoveError("Not yet implemented")

    @staticmethod
    def find_by_ids(ids):
        if not isinstance(ids, (list, tuple)):
            err = "Video.find_by_ids expects an iterable argument"
            raise PyBrightcoveError(err)
        raise PyBrightcoveError("Not yet implemented")
