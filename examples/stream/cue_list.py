import sys
from threefive import Stream

"""
Example using Stream.decode_next()
to return a list of cues from a video

Usage:

pypy3 cue_list.py video.ts

"""


def do():
    CUES = []
    arg = sys.argv[1]
    with open(arg, "rb") as vid:
        while True:
            strm = Stream(vid)
            cue = strm.decode_next()
            if not cue:
                return CUES
            if cue:
                CUES.append(cue)
                print(cue)
        return CUES


if __name__ == "__main__":
    [print(f"SCTE-35 Cue @ {cue.packet_data.pts}") for cue in do()]
