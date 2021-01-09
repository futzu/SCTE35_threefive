"""
decode.py

contains the all purpose
threefive.decode() function
"""

import sys

from .cue import Cue
from .stream import Stream

# Maximum size for a SCTE35 cue.
_MAX_CUE_SIZE = 4096


def _read_stdin():
    """
    handles piped in data
    """
    try:
        Stream(sys.stdin.buffer).decode()
    except:
        try:
            stuff = sys.stdin.buffer.read()
            cue = Cue(stuff)
            cue.decode()
            cue.show()
        except:
            pass


def _read_stuff(stuff):
    """
    reads filename or a string
    """
    try:
        with open(stuff, "rb") as tsdata:
            tsd = tsdata.read(_MAX_CUE_SIZE)
            cue = Cue(tsd)
            cue.decode()
            cue.show()
    except Exception:
        try:
            cue = Cue(stuff)
            cue.decode()
            cue.show()
        except Exception:
            try:
                with open(stuff, "rb") as tsdata:
                    Stream(tsdata).decode()
            except Exception:
                pass
    return


def decode(stuff=None):

    """
    All purpose SCTE 35 decoder function

    # for a mpegts video

        import threefive
        threefive.decode('/path/to/mpegts')

    # for a base64 encoded string

        import threefive
        Bee64='/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g='
        threefive.decode(Bee64)

    stuff can be a filename or encoded string.
    if stuff is not set, reads from stdin.
    """
    if stuff in [None, sys.stdin.buffer]:
        _read_stdin()
    else:
        _read_stuff(stuff)
