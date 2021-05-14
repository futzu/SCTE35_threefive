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
    _read_stdin handles piped in data
    """
    return Stream(sys.stdin.buffer).decode()


def _read_stuff(stuff):
    """
    reads filename or a string
    """
    try:

        # if stuff is a file containing a
        # base64, binary, bytes, hex or hex string
        with open(stuff, "rb") as tsdata:
            tsd = tsdata.read(_MAX_CUE_SIZE)
            cue = Cue(tsd)
            cue.decode()
            cue.show()
    except ValueError:
        pass
    try:

        # if stuff is a mpegts stream file.

        with open(stuff, "rb") as tsdata:
            strm = Stream(tsdata).decode()
            strm.decode()
    except ValueError:
        pass
    try:

        # if stuff is a Base64, Binary, Byte, or Hex
        # encoded string to parse as a SCTE-35 Cue.

        cue = Cue(stuff)
        cue.decode()
        cue.show()
    except ValueError:
        pass


def _read_http(stuff):
    """
    _read_http if stuff is a
    http or https url string.
    """
    with urllib.request.urlopen(stuff) as tsdata:
        strm = Stream(tsdata)
        strm.decode()


def decode(stuff=None):

    """
    All purpose SCTE 35 decoder function

    # MPEG-TS video file

        import threefive
        threefive.decode('/path/to/mpegts')


    # Base64 encoded string

        import threefive
        Bee64='/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g='
        threefive.decode(Bee64)


    # MPEG-TS over HTTP or HTTPS

        from threefive import decode
        decode('https://futzu.com/xaa.ts')


    # Data piped in

        cat SCTE-35.ts | python3 -c 'import threefive; threefive.decode()'

    """
    if stuff in [None]:  # piped in data
        if _read_stdin():
            return
    if isinstance(stuff, str):
        stuff = stuff.encode()
    if isinstance(stuff, bytes):
        if stuff.startswith(b"http"):
            stuff = stuff.decode()
            _read_http(stuff)
            return
    _read_stuff(stuff)
    return
