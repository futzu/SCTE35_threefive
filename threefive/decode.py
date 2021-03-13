"""
decode.py

contains the all purpose
threefive.decode() function
"""

import sys
import urllib3

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
        pass
    try:
        with open(stuff, "rb") as tsdata:
            strm = Stream(tsdata)
            strm.decode()
    except Exception:
        pass

    try:
        cue = Cue(stuff)
        cue.decode()
        cue.show()
    except Exception:
        pass


def _read_http(stuff):
    """
    _read_http reads mpegts over http or https
    and parses for SCTE35
    """
    http = urllib3.PoolManager()
    req = http.request("GET", stuff, preload_content=False)
    strm = Stream(req)
    strm.decode()


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



    # mpegts over http / https

        from threefive import decode
        decode('https://futzu.com/xaa.ts')



    stuff can be a filename or encoded string.
    if stuff is not set, reads from stdin.
    """
    if stuff in [None, sys.stdin.buffer]:
        _read_stdin()
        return
    if stuff.startswith("http"):
        _read_http(stuff)
        return
    _read_stuff(stuff)
    return
