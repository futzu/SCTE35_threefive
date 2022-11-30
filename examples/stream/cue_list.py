"""
Example using Stream.decode() with a custom function
to return a list of cues from a video

Usage:

pypy3 cue_list.py video.ts

"""


import sys
from threefive import Stream, Cue

# A list to hold cues 
CUES=[]

def cue_func(cue):
    """
    threefive.Stream.decode cqn be passed in a
    custom function that accepts a Cue as the only arg.
    this is an example of a custom function.

    """
    CUES.append(cue)
    cue.show()


def do():
    """
    do collects a list of Cues  from a Stream
    """
    arg = sys.argv[1]
    strm = Stream(arg)
    strm.decode(func=cue_func) # cue_func is the custom function from above


if __name__ == "__main__":
    do()
    [print(cue.command.name,cue.encode()) for cue in CUES]
