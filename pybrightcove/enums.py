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


class EconomicsEnum(object):
    FREE = "FREE"
    AD_SUPPORTED = "AD_SUPPORTED"


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
    pass
