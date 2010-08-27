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

# pylint: disable=C0103,R0913,R0903,R0915,R0902,R0914,R0904,R0201

"""
The ``pybrightcove.video`` module supports all the Brightcove Video APIs.
"""

import os
import time
import hashlib
from datetime import datetime
import pybrightcove
from pybrightcove.enums import DEFAULT_SORT_BY, DEFAULT_SORT_ORDER


def is_ftp_connection(connection):
    """
    Shortcut method to test a connection for if it is an FTP connection or not.
    """
    return isinstance(connection, pybrightcove.connection.FTPConnection)

def _convert_tstamp(val):
    """
    Safe convert string timestamp into a ``datetime`` object.  Returns None if
    it can't be converted.
    """
    if val:
        return datetime.fromtimestamp(float(val) / 1000)


def _make_tstamp(val):
    """
    Converts a ``datetime`` object into a unix timestamp.
    """
    if val:
        return int(time.mktime(val.timetuple()) * 1000)


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
            self.remote_url = data["remoteUrl"]
            self.display_name = data["displayName"]

    def to_dict(self):
        """
        Converts object into a dictionary.
        """
        data = {
            'id': self.id,
            'referenceId': self.reference_id,
            'type': self.type,
            'displayName': self.display_name,
            'remoteUrl': self.remote_url}
        for key in data.keys():
            if data[key] == None:
                data.pop(key)
        return data


class Rendition(object):
    """
    The Rendition object represents one of the dynamic delivery renditions of a
    video. A Video should have not more than 10 Rendition objects [1].

    For more information, see Using dynamic delivery [2] and Creating videos
    for dynamic delivery [3].

    [1] http://support.brightcove.com/en/docs/media-api-objects-reference#Rendition
    [2] http://help.brightcove.com/publisher/docs/media/mbr.cfm
    [3] http://help.brightcove.com/developer/docs/mediaapi/create-mbr.cfm
    """

    def __init__(self, data=None):
        self.url = None
        self.encoding_rate = None
        self.frame_height = None
        self.frame_width = None
        self.size = None
        self.remote_url = None
        self.remote_stream_name = None
        self.video_duration = None
        self.video_codec = None

        if data:
            self.url = data.get('url', None)
            self.encoding_rate = data.get('encodingRate', None)
            self.frame_height = data.get('frameHeight', None)
            self.frame_width = data.get('frameWidth', None)
            self.size = data['size']
            self.remote_url = data['remoteUrl']
            self.remote_stream_name = data.get('remoteStreamName', None)
            self.video_duration = data['videoDuration']
            self.video_codec = data['videoCodec']

    def __setattr__(self, name, value):
        msg = None
        if value:
            if name == 'video_duration' and not isinstance(value, (int, long)):
                msg = "Rendition.video_duration must be the duration in "
                msg += "milliseconds as an integer or long."
            if name == 'size' and not isinstance(value, (int, long)):
                msg = "Rendition.size must be the number of bytes as an "
                msg += "integer or long."
            if name == 'video_codec' and \
                    value not in (pybrightcove.enums.VideoCodecEnum.SORENSON,
                                  pybrightcove.enums.VideoCodecEnum.ON2,
                                  pybrightcove.enums.VideoCodecEnum.H264):
                msg = "Rendition.video_codec must be SORENSON, ON2, or H264."

            if msg:
                raise pybrightcove.exceptions.PyBrightcoveError(msg)
        return super(Rendition, self).__setattr__(name, value)

    def to_dict(self):
        """
        Converts object into a dictionary.
        """
        data = {
            'url': self.url,
            'encodingRate': self.encoding_rate,
            'frameHeight': self.frame_height,
            'frameWidth': self.frame_width,
            'size': self.size,
            'remoteUrl': self.remote_url,
            'remoteStream': self.remote_stream_name,
            'videoDuration': self.video_duration,
            'videoCodec': self.video_codec}
        [data.pop(key) for key in data.keys() if data[key] is None]
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
        self.name = None
        self.video_id = None
        self.time = None
        self.force_stop = None
        self.type = None
        self.metadata = None

        if data:
            self.name = data['name']
            self.video_id = data['video_id']
            self.time = data['time']
            self.force_stop = data['forceStop']
            self.type = data['type']
            self.metadata = data['metadata']

    def to_dict(self):
        """
        Converts object into a dictionary.
        """
        data = {
            'name': self.name,
            'video_id': self.video_id,
            'time': self.time,
            'forceStop': self.force_stop,
            'type': self.type,
            'metadata': self.metadata}
        for key in data.keys():
            if data[key] == None:
                data.pop(key)
        return data


class Video(object):
    """
    The Video object is an aggregation of metadata and asset information
    associated with a video.
    """

    # pylint: disable=W0622
    def __init__(self, filename=None, name=None, short_description=None,
        id=None, reference_id=None, renditions=None, data=None,
        connection=None):

        self._filename = None
        self.name = None
        self.short_description = None
        self.id = None
        self.reference_id = None
        self.accountId = None
        self.long_description = None
        self.flv_url = None
        self.renditions = []
        self.assets = []
        self.metadata = []
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
        self.raw_data = None

        self.connection = connection
        if not self.connection:
            self.connection = pybrightcove.connection.APIConnection()

        if is_ftp_connection(self.connection):
            if reference_id and name and short_description:
                self.reference_id = reference_id
                self.name = name
                self.short_description = short_description
            else:
                msg = "Invalid parameters for Video."
                raise pybrightcove.exceptions.PyBrightcoveError(msg)
        else:
            if ((renditions and len(renditions) > 0) or filename) and name \
                and short_description:
                if filename is not None:
                    self._filename = filename
                if renditions is not None:
                    self.renditions = renditions
                self.name = name
                self.short_description = short_description
            elif id or reference_id:
                self.id = id
                self.reference_id = reference_id
                self._find_video()
            elif data:
                self._load(data)
            else:
                msg = "Invalid parameters for Video."
                raise pybrightcove.exceptions.PyBrightcoveError(msg)

    def _find_video(self):
        """
        Lookup and populate ``pybrightcove.video.Video`` object given a video
        id or reference_id.
        """
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
        """
        Converts object into a dictionary.
        """
        for i, tag in enumerate(self.tags):
            if tag in ("", None):
                self.tags.pop(i)

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
            'id': self.id,
            'end_date': _make_tstamp(self.end_date),
            'start_date': _make_tstamp(self.start_date)}
        if len(self.renditions) > 0:
            data['renditions'] = []
            for r in self.renditions:
                data['renditions'].append(r.to_dict())
        if len(self.metadata) > 0:
            data['customFields'] = {}
            for meta in self.metadata:
                data['customFields'][meta['key']] = meta['value']
        [data.pop(key) for key in data.keys() if data[key] == None]
        return data

    def to_xml(self):
        # pylint: disable=R0912
        """
        Converts object into an XML string.
        """
        xml = ''
        for asset in self.assets:
            xml += '<asset filename="%s" ' % \
                os.path.basename(asset['filename'])
            xml += ' refid="%(refid)s"' % asset
            xml += ' size="%(size)s"' % asset
            xml += ' hash-code="%s"' % asset['hash-code']
            xml += ' type="%(type)s"' % asset
            if asset.get('encoding-rate', None):
                xml += ' encoding-rate="%s"' % asset['encoding-rate']
            if asset.get('frame-width', None):
                xml += ' frame-width="%s"' % asset['frame-width']
            if asset.get('frame-height', None):
                xml += ' frame-height="%s"' % asset['frame-height']
            if asset.get('display-name', None):
                xml += ' display-name="%s"' % asset['display-name']
            if asset.get('encode-to', None):
                xml += ' encode-to="%s"' % asset['encode-to']
            if asset.get('encode-multiple', None):
                xml += ' encode-multiple="%s"' % asset['encode-multiple']
            if asset.get('h264-preserve-as-rendition', None):
                xml += ' h264-preserve-as-rendition="%s"' % \
                    asset['h264-preserve-as-rendition']
            if asset.get('h264-no-processing', None):
                xml += ' h264-no-processing="%s"' % asset['h264-no-processing']
            xml += ' />\n'
        xml += '<title name="%(name)s" refid="%(referenceId)s" active="TRUE" '
        if self.start_date:
            xml += 'start-date="%(start_date)s" '
        if self.end_date:
            xml += 'end-date="%(end_date)s" '
        for asset in self.assets:
            if asset.get('encoding-rate', None) == None:
                choice = pybrightcove.enums.AssetTypeEnum
                if asset.get('type', None) == choice.VIDEO_FULL:
                    xml += 'video-full-refid="%s" ' % asset.get('refid')
                if asset.get('type', None) == choice.THUMBNAIL:
                    xml += 'thumbnail-refid="%s" ' % asset.get('refid')
                if asset.get('type', None) == choice.VIDEO_STILL:
                    xml += 'video-still-refid="%s" ' % asset.get('refid')
                if asset.get('type', None) == choice.FLV_BUMPER:
                    xml += 'flash-prebumper-refid="%s" ' % asset.get('refid')
        xml += '>\n'
        if self.short_description:
            xml += '<short-description><![CDATA[%(shortDescription)s]]>'
            xml += '</short-description>\n'
        if self.long_description:
            xml += '<long-description><![CDATA[%(longDescription)s]]>'
            xml += '</long-description>\n'
        for tag in self.tags:
            xml += '<tag><![CDATA[%s]]></tag>\n' % tag
        for asset in self.assets:
            if asset.get('encoding-rate', None):
                xml += '<rendition-refid>%s</rendition-refid>\n' % \
                    asset['refid']
        for meta in self.metadata:
            xml += '<custom-%s-value name="%s">%s</custom-%s-value>' % \
                (meta['type'], meta['key'], meta['value'], meta['type'])
        xml += '</title>'
        xml = xml % self._to_dict()
        return xml

    def _load(self, data):
        """
        Deserialize a dictionary of data into a ``pybrightcove.video.Video``
        object.
        """
        self.raw_data = data
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
        self.start_date = _convert_tstamp(data.get('startDate', None))
        self.end_date = _convert_tstamp(data.get('endDate', None))
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
            if name == 'name' and len(value) > 255:
                msg = "Video.name must be 255 characters or less."
            if name == 'reference_id' and len(value) > 150:
                # val = value[:150]
                msg = "Video.reference_id must be 150 characters or less."
            if name == 'long_description' and len(value) > 5000:
                # val = value[:5000]
                msg = "Video.long_description must be 5000 characters or less."
            if name == 'short_description' and len(value) > 250:
                # val = value[:250]
                msg = "Video.short_description must be 250 characters or less."
            if name == 'item_state' and value not in (
                    pybrightcove.enums.ItemStateEnum.ACTIVE,
                    pybrightcove.enums.ItemStateEnum.INACTIVE):
                msg = "Video.item_state must be either ItemStateEnum.ACTIVE or"
                msg += " ItemStateEnum.INACTIVE"
            if name == 'video_full_length' and \
                    not isinstance(value, Rendition):
                msg = "Video.video_full_length must be of type Rendition"
            if name == 'economics' and value not in \
                    (pybrightcove.enums.EconomicsEnum.FREE,
                     pybrightcove.enums.EconomicsEnum.AD_SUPPORTED):
                msg = "Video.economics must be either EconomicsEnum.FREE or "
                msg += "EconomicsEnum.AD_SUPPORTED"

            if msg:
                raise pybrightcove.exceptions.PyBrightcoveError(msg)
        return super(Video, self).__setattr__(name, value)
    
    def get_custom_metadata(self):
        """
        Fetches custom metadta for an already exisiting Video.
        """
        if self.id is not None:
            data = self.connection.get_item(
                'find_video_by_id',
                video_id=self.id,
                video_fields="customFields"
            )
            for key in data.get("customFields", {}).keys():
                val = data["customFields"].get(key)
                if val is not None:
                    self.add_custom_metadata(key, val)

    def add_custom_metadata(self, key, value, meta_type=None):
        """
        Add custom metadata to the Video.  meta_type is required for XML API.
        """
        self.metadata.append({'key': key, 'value': value, 'type': meta_type})

    def add_asset(self, filename, asset_type, display_name,
        encoding_rate=None, frame_width=None, frame_height=None,
        encode_to=None, encode_multiple=False,
        h264_preserve_as_rendition=False, h264_no_processing=False):
        """
        Add an asset to the Video object.
        """
        m = hashlib.md5()
        fp = file(filename, 'rb')
        bits = fp.read(262144)  ## 256KB
        while bits:
            m.update(bits)
            bits = fp.read(262144)
        fp.close()

        hash_code = m.hexdigest()
        refid = "%s-%s" % (os.path.basename(filename), hash_code)

        asset = {
            'filename': filename,
            'type': asset_type,
            'size': os.path.getsize(filename),
            'refid': refid,
            'hash-code': hash_code}

        if encoding_rate:
            asset.update({'encoding-rate': encoding_rate})
        if frame_width:
            asset.update({'frame-width': frame_width})
        if frame_height:
            asset.update({'frame-height': frame_height})
        if display_name:
            asset.update({'display-name': display_name})
        if encode_to:
            asset.update({'encode-to': encode_to})
            asset.update({'encode-multiple': encode_multiple})
            if encode_multiple and h264_preserve_as_rendition:
                asset.update({
                    'h264-preserve-as-rendition': h264_preserve_as_rendition})
        else:
            if h264_no_processing:
                asset.update({'h264-no-processing': h264_no_processing})
        self.assets.append(asset)

    def save(self, create_multiple_renditions=True,
        preserve_source_rendition=True,
        encode_to=pybrightcove.enums.EncodeToEnum.FLV):
        """
        Creates or updates the video
        """
        if is_ftp_connection(self.connection) and len(self.assets) > 0:
            self.connection.post(xml=self.to_xml(), assets=self.assets)
        elif not self.id and self._filename:
            self.id = self.connection.post('create_video', self._filename,
                create_multiple_renditions=create_multiple_renditions,
                preserve_source_rendition=preserve_source_rendition,
                encode_to=encode_to,
                video=self._to_dict())
        elif not self.id and len(self.renditions) > 0:
            self.id = self.connection.post('create_video',
                video=self._to_dict())
        elif self.id:
            data = self.connection.post('update_video', video=self._to_dict())
            if data:
                self._load(data)

    def delete(self, cascade=False, delete_shares=False):
        """
        Deletes the video.
        """
        if self.id:
            self.connection.post('delete_video', video_id=self.id,
                cascade=cascade, delete_shares=delete_shares)
            self.id = None ## Prevent more activity on this video id

    def get_upload_status(self):
        """
        Get the status of the video that has been uploaded.
        """
        if self.id:
            return self.connection.post('get_upload_status', video_id=self.id)

    def share(self, accounts):
        """
        Create a share
        """
        if not isinstance(accounts, (list, tuple)):
            msg = "Video.share expects an iterable argument"
            raise pybrightcove.exceptions.PyBrightcoveError(msg)
        raise pybrightcove.exceptions.PyBrightcoveError("Not yet implemented")

    def set_image(self, image, filename=None, resize=False):
        """
        Set the poster or thumbnail of a this Vidoe.
        """
        if self.id:
            data = self.connection.post('add_image', filename,
                video_id=self.id, image=image.to_dict(), resize=resize)
            if data:
                self.image = Image(data=data)

    def find_related(self, connection=None, page_size=100, page_number=0):
        """
        List all videos that are related to this one.
        """
        if self.id:
            return pybrightcove.connection.ItemResultSet('find_related_videos',
                Video, connection, page_size, page_number, None, None,
                video_id=self.id)

    def deactivate(self):
        """
        Mark a video as Inactive
        """
        self.item_state = pybrightcove.enums.ItemStateEnum.INACTIVE
        self.save()

    @staticmethod
    def delete_video(video_id, cascade=False, delete_shares=False,
        connection=None):
        """
        Delete the video represented by the ``video_id`` parameter.
        """
        c = connection
        if not c:
            c = pybrightcove.connection.APIConnection()
        c.post('delete_video', video_id=video_id, cascade=cascade,
            delete_shares=delete_shares)

    @staticmethod
    def get_status(video_id, connection=None):
        """
        Get the status of a video given the ``video_id`` parameter.
        """
        c = connection
        if not c:
            c = pybrightcove.connection.APIConnection()
        return c.post('get_upload_status', video_id=video_id)

    @staticmethod
    def activate(video_id, connection=None):
        """
        Mark a video as Active
        """
        c = connection
        if not c:
            c = pybrightcove.connection.APIConnection()
        data = c.post('update_video', video={
            'id': video_id,
            'itemState': pybrightcove.enums.ItemStateEnum.ACTIVE})
        return Video(data=data, connection=c)

    @staticmethod
    def find_modified(since, filter_list=None, connection=None, page_size=25,
        page_number=0, sort_by=DEFAULT_SORT_BY, sort_order=DEFAULT_SORT_ORDER):
        """
        List all videos modified since a certain date.
        """
        filters = []
        if filter_list is not None:
            filters = filter_list
        if not isinstance(since, datetime):
            msg = 'The parameter "since" must be a datetime object.'
            raise pybrightcove.exceptions.PyBrightcoveError(msg)
        fdate = int(since.strftime("%s")) / 60  ## Minutes since UNIX time
        return pybrightcove.connection.ItemResultSet('find_modified_videos',
            Video, connection, page_size, page_number, sort_by, sort_order,
            from_date=fdate, filter=filters)

    @staticmethod
    def find_all(connection=None, page_size=100, page_number=0,
        sort_by=DEFAULT_SORT_BY, sort_order=DEFAULT_SORT_ORDER):
        """
        List all videos.
        """
        return pybrightcove.connection.ItemResultSet('find_all_videos', Video,
            connection, page_size, page_number, sort_by, sort_order)

    @staticmethod
    def find_by_tags(and_tags=None, or_tags=None, connection=None,
        page_size=100, page_number=0, sort_by=DEFAULT_SORT_BY,
        sort_order=DEFAULT_SORT_ORDER):
        """
        List videos given a certain set of tags.
        """
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
            raise pybrightcove.exceptions.PyBrightcoveError(err)
        atags = None
        otags = None
        if and_tags:
            atags = ','.join([str(t) for t in and_tags])
        if or_tags:
            otags = ','.join([str(t) for t in or_tags])
        return pybrightcove.connection.ItemResultSet('find_videos_by_tags',
            Video, connection, page_size, page_number, sort_by, sort_order,
            and_tags=atags, or_tags=otags)

    @staticmethod
    def find_by_text(text, connection=None, page_size=100, page_number=0,
        sort_by=DEFAULT_SORT_BY, sort_order=DEFAULT_SORT_ORDER):
        """
        List videos that match the ``text`` in title or description.
        """
        return pybrightcove.connection.ItemResultSet('find_videos_by_text',
            Video, connection, page_size, page_number, sort_by, sort_order,
            text=text)

    @staticmethod
    def find_by_campaign(campaign_id, connection=None, page_size=100,
        page_number=0, sort_by=DEFAULT_SORT_BY, sort_order=DEFAULT_SORT_ORDER):
        """
        List all videos for a given campaign.
        """
        return pybrightcove.connection.ItemResultSet(
            'find_videos_by_campaign_id', Video, connection, page_size,
            page_number, sort_by, sort_order, campaign_id=campaign_id)

    @staticmethod
    def find_by_user(user_id, connection=None, page_size=100, page_number=0,
        sort_by=DEFAULT_SORT_BY, sort_order=DEFAULT_SORT_ORDER):
        """
        List all videos uploaded by a certain user.
        """
        return pybrightcove.connection.ItemResultSet('find_videos_by_user_id',
            Video, connection, page_size, page_number, sort_by, sort_order,
            user_id=user_id)

    @staticmethod
    def find_by_reference_ids(reference_ids, connection=None, page_size=100,
        page_number=0, sort_by=DEFAULT_SORT_BY, sort_order=DEFAULT_SORT_ORDER):
        """
        List all videos identified by a list of reference ids
        """
        if not isinstance(reference_ids, (list, tuple)):
            err = "Video.find_by_reference_ids expects an iterable argument"
            raise pybrightcove.exceptions.PyBrightcoveError(err)
        ids = ','.join(reference_ids)
        return pybrightcove.connection.ItemResultSet(
            'find_videos_by_reference_ids', Video, connection, page_size,
            page_number, sort_by, sort_order, reference_ids=ids)

    @staticmethod
    def find_by_ids(ids, connection=None, page_size=100, page_number=0,
        sort_by=DEFAULT_SORT_BY, sort_order=DEFAULT_SORT_ORDER):
        """
        List all videos identified by a list of Brightcove video ids
        """
        if not isinstance(ids, (list, tuple)):
            err = "Video.find_by_ids expects an iterable argument"
            raise pybrightcove.exceptions.PyBrightcoveError(err)
        ids = ','.join([str(i) for i in ids])
        return pybrightcove.connection.ItemResultSet('find_videos_by_ids',
            Video, connection, page_size, page_number, sort_by, sort_order,
            video_ids=ids)

