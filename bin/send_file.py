from pybrightcove.connection import Connection
from pybrightcove.video import Video

c = Connection()

import sys

video = Video()
video.title = "My Test File"
video.short_description = "This is a short description"

print "Attempting to upload %s" % sys.argv[1]
c.create_video(sys.argv[1], video=video)
print "Done"