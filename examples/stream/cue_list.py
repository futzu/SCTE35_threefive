"""
Example using Stream.decode_next()
to return a list of cues from a video

Usage:

pypy3 cue_list.py video.ts

"""


import sys
from threefive import Stream


def do():
    """
    do collects a list of Cues  from a Stream
    """
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
        return CUES


if __name__ == "__main__":
    for cue in do():
        print(f"{cue.command.name} @ {cue.packet_data.pts}")
