"""
decode.py

contains the all purpose
threefive.decode() function
"""

import sys
import urllib.request

from .cue import Cue
from .stream import Stream

# Maximum size for a SCTE35 cue.
_MAX_CUE_SIZE = 4096


def _read_stdin():
    """
    handles piped in data
    """
    try:
        # mpegts
        Stream(sys.stdin.buffer).decode()
    except Exception:
        try:
            # base64, binary, bytes or hex
            stuff = sys.stdin.buffer.read()
            cue = Cue(stuff)
            cue.decode()
            cue.show()
        except Exception:
            pass


def _read_stuff(stuff):
    """
    reads filename or a string
    """
    try:
        # base64, binary, bytes or hex in a file
        with open(stuff, "rb") as tsdata:
            tsd = tsdata.read(_MAX_CUE_SIZE)
            cue = Cue(tsd)
            cue.decode()
            cue.show()
    except Exception:
        pass
    try:
        # mpegts
        with open(stuff, "rb") as tsdata:
            strm = Stream(tsdata)
            strm.decode()
    except Exception:
        pass
    try:
        # base64, binary, bytes or hex
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
    with urllib.request.urlopen(stuff) as tsdata:
        strm = Stream(tsdata)
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


    # hex, base64, binary, bytes, or mpegts from sys.stdin.buffer

        from threefive import decode
        decode()


    """
    if stuff in [None, sys.stdin.buffer]:
        _read_stdin()
        return
    if isinstance(stuff, str):
        if stuff.startswith("http"):
            _read_http(stuff)
            return
    if isinstance(stuff, bytes):
        if stuff.startswith(b"http"):
            _read_http(stuff.decode())
            return
    _read_stuff(stuff)
    return
