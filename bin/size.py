import simplejson
from subprocess import PIPE, Popen
import sys

out = Popen(['avinspect', sys.argv[1], '--json'], stdout=PIPE).communicate()[0] 
d = simplejson.loads(out)
for s in d["streams"]:
    if s["type"] == "Video":
        print "%sx%s" % (s["width"], s["height"])
