import sys
import m3u8  # pypy3 -mpip install m3u8
from threefive import Cue  # pypy3 -mpip install threefive


"""
HLS example using the m3u8 lib to parse the m3u8 file
and threefive to parse Scte-35 Cues. 
"""


pl = m3u8.load(sys.argv[1])
last_scte35 = None
for seg in pl.segments:
    vseg = vars(seg)
    if "scte35" in vseg:
        if vseg["cue_in"]:
            print(vseg)
        if last_scte35 != vseg["scte35"]:
            print(vseg)
            cue = Cue(vseg["scte35"])
            cue.decode()
            cue.show()
            last_scte35 = vseg["scte35"]
