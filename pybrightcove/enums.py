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


class SortByType(object):
    """
    PUBLISH_DATE:
        Date title was published

    CREATION_DATE:
        Date title was created.

    MODIFIED_DATE
        Date title was last modified.

    PLAYS_TOTAL
        Number of times this title has been viewed.

    PLAYS_TRAILING_WEEK
        Number of times this title has been viewed in the past 7 days
        (excluding today).
    """
    PUBLISH_DATE = "PUBLISH_DATE"
    CREATION_DATE = "CREATION_DATE"
    MODIFIED_DATE = "MODIFIED_DATE"
    PLAYS_TOTAL = "PLAYS_TOTAL"
    PLAYS_TRAILING_WEEK = "PLAYS_TRAILING_WEEK"


class SortByOrderType(object):
    """
    ASC:
        Ascending

    DESC:
        Descending
    """
    ASC = "ASC"
    DESC = "DESC"


class UploadStatusEnum(object):
    """
    UPLOADING:
        File is still uploading

    PROCESSING:
        Upload complete; being processed.

    COMPLETE:
        Upload and processing complete.

    ERROR:
        Error in upload or processing.
    """
    UPLOADING = "UPLOADING"
    PROCESSING = "PROCESSING"
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"


class EconomicsEnum(object):
    FREE = "FREE"
    AD_SUPPORTED = "AD_SUPPORTED"


class ItemStateEnum(object):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"


class PlaylistTypeEnum(object):
    """
    EXPLICIT:
        A manual playlist, the videos of which were added individually.

    OLDEST_TO_NEWEST:
        A smart playlist, ordered from oldest to newest by last-modified date.

    NEWEST_TO_OLDEST:
        A smart playlist, ordered from newest to oldest by last-modified date.

    ALPHABETICAL:
        A smart playlist, ordered alphabetically.

    PLAYS_TOTAL:
        A smart playlist, ordered by total plays.

    PLAYS_TRAILING_WEEK:
        A smart playlist, ordered by most plays in the past week.
    """
    EXPLICIT = "EXPLICIT"
    OLDEST_TO_NEWEST = "OLDEST_TO_NEWEST"
    NEWEST_TO_OLDEST = "NEWEST_TO_OLDEST"
    ALPHABETICAL = "ALPHABETICAL"
    PLAYS_TOTAL = "PLAYS_TOTAL"
    PLAYS_TRAILING_WEEK = "PLAYS_TRAILING_WEEK"


class PublicPlaylistFieldsEnum(object):
    ID = "ID"
    REFERENCE_ID = "REFERENCEID"
    NAME = "NAME"
    SHORT_DESCRIPTION = "SHORTDESCRIPTION"
    VIDEO_IDS = "VIDEOIDS"
    VIDEOS = "VIDEOS"
    THUMBNAIL_URL = "THUMBNAILURL"
    FILTER_TAGS = "FILTERTAGS"
    PLAYLIST_TYPE = "PLAYLISTTYPE"
    ACCOUNT_ID = "ACCOUNTID"


class PublicVideoFieldsEnum(object):
    ID = "ID"
    NAME = "NAME"
    SHORT_DESCRIPTION = "SHORTDESCRIPTION"
    LONG_DESCRIPTION = "LONGDESCRIPTION"
    CREATION_DATE = "CREATIONDATE"
    PUBLISHED_DATE = "PUBLISHEDDATE"
    LAST_MODIFIED_DATE = "LASTMODIFIEDDATE"
    START_DATE = "STARTDATE"
    END_DATE = "ENDDATE"
    LINK_URL = "LINKURL"
    LINK_TEXT = "LINKTEXT"
    TAGS = "TAGS"
    VIDEO_STILL_URL = "VIDEOSTILLURL"
    THUMBNAIL_URL = "THUMBNAILURL"
    REFERENCE_ID = "REFERENCEID"
    LENGTH = "LENGTH"
    ECONOMICS = "ECONOMICS"
    ITEM_STATE = "ITEMSTATE"
    PLAYS_TOTAL = "PLAYSTOTAL"
    PLAYS_TRAILING_WEEK = "PLAYSTRAILINGWEEK"
    VERSION = "VERSION"
    CUEPOINTS = "CUEPOINTS"
    SUBMISSION_INFO = "SUBMISSIONINFO"
    CUSTOM_FIELDS = "CUSTOMFIELDS"
    RELEASEDATE = "RELEASEDATE"
    FLVURL = "FLVURL"
    RENDITIONS = "RENDITIONS"
    GEO_FILTERED = "GEOFILTERED"
    GEO_RESTRICTED = "GEORESTRICTED"
    GEO_FILTER_EXCLUDE = "GEOFILTEREXCLUDE"
    EXCLUDE_LISTED_COUNTRIES = "EXCLUDELISTEDCOUNTRIES"
    GEO_FILTERED_COUNTRIES = "GEOFILTEREDCOUNTRIES"
    ALLOWED_COUNTRIES = "ALLOWEDCOUNTRIES"
    ACCOUNT_ID = "ACCOUNTID"
    FLV_FULL_LENGTH = "FLVFULLLENGTH"
    VIDEO_FULL_LENGTH = "VIDEOFULLLENGTH"


class VideoCodecEnum(object):
    UNDEFINED = "UNDEFINED"
    NONE = "NONE"
    SORENSON = "SORENSON"
    ON2 = "ON2"
    H264 = "H264"


class ImageTypeEnum(object):
    VIDEO_STILL = "VIDEO_STILL"
    SYNDICATION_STILL = "SYNDICATION_STILL"
    THUMBNAIL = "THUMBNAIL"
    BACKGROUND = "BACKGROUND"
    LOGO = "LOGO"
    LOGO_OVERLAY = "LOGO_OVERLAY"


class VideoTypeEnum(object):
    FLV_PREVIEW = "FLV_PREVIEW"
    FLV_FULL = "FLV_FULL"
    FLV_BUMPER = "FLV_BUMPER"
    DIGITAL_MASTER = "DIGITAL_MASTER"
