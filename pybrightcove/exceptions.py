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


class PyBrightcoveError(Exception):

    def __init__(self, reason):
        super(PyBrightcoveError, self).__init__(reason)


class ImproperlyConfiguredError(PyBrightcoveError):
    pass


class NoDataFoundError(PyBrightcoveError):

    def __init__(self, reason=None):
        super(NoDataFoundError, self).__init__(reason)


class BrightcoveError(Exception):
    description = "a general error"

    def __init__(self):
        super(BrightcoveError, self).__init__(self.description)

    @staticmethod
    def raise_exception(data):
        error = BrightcoveError()
        error.raw_data = data
        if "code" in data and data["code"] in ERROR_MAP:
            error = ERROR_MAP[data["code"]]()
            error.raw_data = data
            if data.get('message', None):
                error.description = data['message']

        raise error

    def __unicode__(self):
        return u'%s' % self.description

    def __str__(self):
        return self.description


class UnknownServerError(BrightcoveError):
    description = "an unknown error occurred while processing your request"
    cause = "An unspecified and unexpected error"
    code = 100


class ServiceDeployingError(BrightcoveError):
    description = """The write API is currently unavailable due to a scheduled
            upgrade. Please check http://studio.brightcove.com/ for updates."""
    cause = """The Brightcove Write API is currently down for a scheduled
            deployment."""
    code = 101


class CallTimeoutError(BrightcoveError):
    description = """The request you made is taking longer than expected to
            return. If requesting a large amount of data please try again with
            a smaller page_size."""
    cause = """Media API calls can time out before they complete if you are
            trying to get too much data at once. The page_size argument enables
            returning data in more manageable chunks."""
    code = 103


class EnctypeError(BrightcoveError):
    description = """wrong enctype; write methods require a multipart/form-data
            POST"""
    cause = "Calling a write method with a plain old POST"
    code = 200


class GetRequiredError(BrightcoveError):
    description = """methods that retrieve data must be called using GET
            requests"""
    cause = "Calling POST instead of GET on the Read API"
    code = 201


class PostRequiredError(BrightcoveError):
    description = """methods that change data must be called using POST
            requests"""
    cause = "Calling GET instead of POST on the Write API"
    code = 202


class MissingQueryStringError(BrightcoveError):
    description = "no query string provided"
    cause = "A missing query string in GET"
    code = 203


class MissingBodyError(BrightcoveError):
    description = """POST methods require valid JSON-RPC in the POST body,
            with \"method\" and \"params\" properties"""
    cause = "A missing parameter section in POST"
    code = 204


class MalformedParametersError(BrightcoveError):
    description = """unable to parse JSON-RPC parameters; they may be malformed
            or incorrect"""
    cause = "Malformed JSON in request"
    code = 205


class InvalidMethodError(BrightcoveError):
    description = "invalid method name"
    cause = "Invalid method name"
    code = 206


class FilestreamRequiredError(BrightcoveError):
    description = """upload requires a multipart/form-data POST with a valid
            filestream"""
    cause = "Missing file stream"
    code = 207


class MissingFileNameError(BrightcoveError):
    description = "file for upload must have a filename"
    cause = "Missing file name"
    code = 208


class UnwantedFilestreamError(BrightcoveError):
    description = "non-upload methods should not include a filestream"
    cause = "A filestream was provided for a non-upload method."
    code = 209


class InvalidTokenError(BrightcoveError):
    description = "invalid token"
    cause = "The token used in the call is invalid."
    code = 210


class MissingJSONError(BrightcoveError):
    description = "Could not find JSON-RPC."
    cause = """We got a null string for either the json parameter (for a
            non-multipart post) or the first part of a multipart post."""
    code = 211


class InvalidParametersError(BrightcoveError):
    description = "parameters are the wrong type or number for this method"
    cause = "Invoking the method threw an IllegalArgumentException"
    code = 301


class DeleteFailedError(BrightcoveError):
    description = """<message with reason for failure filled in by throwing
            method>"""
    cause = """Attempt to delete a business object failed. For example,
            attempts to delete a video that's in a manual playlist will
            fail."""
    code = 302


class RequiredParameterError(BrightcoveError):
    description = """required parameter <> was missing (<> to be filled in by
            throwing method)"""
    cause = "A required parameter was not set."
    code = 303


class IllegalValueError(BrightcoveError):
    description = """Cannot find any video with id: <>
            Cannot find the video you are trying to update: id <>
            One or more accounts in sharee_account_ids are not enabled for
                media sharing"""
    cause = """In a get_upload_status call, the video_id entered does not refer
                to a valid video in the Media Library
            In an update_video call, the video_id entered does not refer to a
                valid video in the Media Library
            In a share_video call, you do not have a sharing relationship
                established with the account whose id was entered."""
    code = 304


class IncompatibleValueError(BrightcoveError):
    description = """The geo restriction property on this video is incompatible
                with the destination account.
            The referenceId property on this video is in use by a destination
                account.
            The economics property on this video is incompatible with a
                destination account."""
    cause = """The Quova settings in the video and the destination account
                don't match.
            The reference ID is already in use in the destination account.
            Advertising must be enabled on all accounts, or disabled on all
                accounts."""
    code = 35


class FileFormatError(BrightcoveError):
    description = "The provided file was not in the expected format"
    cause = """The file provided to create_video was not in a supported file
            format."""
    code = 306


class ObjectNotFoundError(BrightcoveError):
    description = """The object specified by the given parameters could not be
            found."""
    cause = "The object with the specified id could not be found."
    code = 307


class NonmatchingChecksumError(BrightcoveError):
    description = """The provided file's MD5 digest did not match the checksum
            provided."""
    cause = """We checked an uploaded file's hash and it didn't match the
            expected checksum."""
    code = 308


class RemoteAssetsDisabledError(BrightcoveError):
    description = """This account is not approved to use remote assets."""
    cause = """You attempted to create or update a remote asset, but your
            account is not enabled for this feature."""
    code = 309


class InvalidCountryCodeError(BrightcoveError):
    description = """The following country codes are not supported for
        geo-restriction:"""
    cause = "You used an invalid country code for geo-restriction."
    code = 310


class GeoRestrictionDisabledError(BrightcoveError):
    description = "This account is not approved to use geo-restriction"
    cause = """You attempted to set geo-restriction properties for a video,
            but your account is not enabled for this feature."""
    code = 311


ERROR_MAP = {}
ERROR_MAP[100] = UnknownServerError
ERROR_MAP[101] = ServiceDeployingError
ERROR_MAP[103] = CallTimeoutError
ERROR_MAP[200] = EnctypeError
ERROR_MAP[201] = GetRequiredError
ERROR_MAP[202] = PostRequiredError
ERROR_MAP[203] = MissingQueryStringError
ERROR_MAP[204] = MissingBodyError
ERROR_MAP[205] = MalformedParametersError
ERROR_MAP[206] = InvalidMethodError
ERROR_MAP[207] = FilestreamRequiredError
ERROR_MAP[208] = MissingFileNameError
ERROR_MAP[209] = UnwantedFilestreamError
ERROR_MAP[210] = InvalidTokenError
ERROR_MAP[211] = MissingJSONError
ERROR_MAP[301] = InvalidParametersError
ERROR_MAP[302] = DeleteFailedError
ERROR_MAP[303] = RequiredParameterError
ERROR_MAP[304] = IllegalValueError
ERROR_MAP[305] = IncompatibleValueError
ERROR_MAP[306] = FileFormatError
ERROR_MAP[307] = ObjectNotFoundError
ERROR_MAP[308] = NonmatchingChecksumError
ERROR_MAP[309] = RemoteAssetsDisabledError
ERROR_MAP[310] = InvalidCountryCodeError
ERROR_MAP[311] = GeoRestrictionDisabledError
