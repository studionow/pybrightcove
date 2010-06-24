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
Configuration for pybrightcove is fairly simple and uses standard ini type file
structure found in ``~/.pybrightcove`` for a user level one or 
``/etc/pybrightcove.cfg`` for one at the system level.  User config files
supercede those at the system level.
"""

import os
import sys
import ConfigParser

from pybrightcove import __version__


USER_CONFIG_PATH = os.path.expanduser('~/.pybrightcove')
CONFIG_PATH = '/etc/pybrightcove.cfg'
CONFIG_LOCATIONS = [CONFIG_PATH, USER_CONFIG_PATH]
USER_AGENT = 'PyBrightcove/%s (%s)' % (__version__, sys.platform)


def has_option(section, name):
    """
    Wrapper around ConfigParser's ``has_option`` method.
    """
    cfg = ConfigParser.SafeConfigParser({"working_dir": "/tmp", "debug": "0"})
    cfg.read(CONFIG_LOCATIONS)
    return cfg.has_option(section, name)


def get(section, name):
    """
    Wrapper around ConfigParser's ``get`` method.
    """
    cfg = ConfigParser.SafeConfigParser({"working_dir": "/tmp", "debug": "0"})
    cfg.read(CONFIG_LOCATIONS)
    val = cfg.get(section, name)
    return val.strip("'").strip('"')

