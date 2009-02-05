from pybrightcove.connection import Connection
from pybrightcove.video import Video

c = Connection()

import sys

video = Video()
video.title = sys.argv[1]
video.short_description = sys.argv[1]

print "Attempting to upload %s" % sys.argv[1]
c.create_video(sys.argv[1], video=video)
print "Done"