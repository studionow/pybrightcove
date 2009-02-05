from pybrightcove.connection import Connection
from pybrightcove.video import Video

c = Connection()

import sys

video = Video()
video.name = sys.argv[1]
video.shortDescription = sys.argv[1]*50  # Test teh property only recording what's allowed by the API
#print video.shortDescription
for tag in sys.argv[2:]:
    video.tags.append(tag)

print "Attempting to upload %s" % sys.argv[1]
c.create_video(sys.argv[1], video=video)
print "Done"
