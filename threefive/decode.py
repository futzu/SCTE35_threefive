"""
decode.py

Usage:

* Base64:

    Bee64='/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g='
    threefive.decode(Bee64)


* Hex String:

    hexed = '0XFC301100000000000000FFFFFF0000004F253396'
    threefive.decode(hexed)


* Hex Value:

    threefive.decode(0XFC301100000000000000FFFFFF0000004F253396)


* Int
    big_int = 1439737590925997869941740173214217318917816529814
    threefive.decode(big_int)


* Mpegts File:

    threefive.decode('/path/to/mpegts')


* Mpegts over Http/Https

    threefive.decode('https://futzu.com/xaa.ts')

"""

import sys
import urllib.request

from .cue import Cue
from .stream import Stream

# Maximum size for a SCTE35 cue.
_MAX_CUE_SIZE = 4096


def _decode_and_show(stuff):
    cue = Cue(stuff)
    cue.decode()
    cue.show()


def _read_stdin():
    # mpegts data via stdin
    try:
        Stream(sys.stdin.buffer).decode()
    except Exception:
        # base64 or hex encoded string or raw bytes via stdin
        try:
            stuff = sys.stdin.buffer.read()
            _decode_and_show(stuff)
        except Exception:
            pass


def _read_stuff(stuff):
    # base64, binary, bytes or hex in a file
    try:
        with open(stuff, "rb") as tsdata:
            tsd = tsdata.read(_MAX_CUE_SIZE)
            _decode_and_show(tsd)
    except Exception:
        # mpegts video file
        try:
            with open(stuff, "rb") as tsdata:
                strm = Stream(tsdata)
                strm.decode()
        except Exception:
            try:
                _decode_and_show(stuff)
            except Exception:
                pass


def _read_http(stuff):
    with urllib.request.urlopen(stuff) as tsdata:
        strm = Stream(tsdata)
        strm.decode()


def decode(stuff=None):
    """
    All purpose SCTE 35 decoder function
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
    if isinstance(stuff, int):
        _read_stuff(hex(stuff))
    _read_stuff(stuff)
    return
