"""
decode.py

decode is a SCTE-35 decoder function
with input type auto-detection.

SCTE-35 data can be parsed with just
one function call.

the arg stuff is the input.
if stuff is not set, decode will attempt
to read mpegts video from sys.stdin.buffer.

SCTE-35 data is printed in JSON format.

For more parsing and output control,
see the Cue and Stream classes.

"""

import sys

from .cue import Cue
from .stream import Stream


def _read_stuff(stuff):
    try:
        # Mpegts Video
        strm = Stream(stuff)
        strm.decode()
        return True
    except:
        try:
            cue = Cue(stuff)
            cue.decode()
            cue.show()
            return True
        except:
            return False


def decode(stuff=None):
    """
    decode is a SCTE-35 decoder function
    with input type auto-detection.

    SCTE-35 data is printed in JSON format.

    Use like:

    # Base64
    stuff = '/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g='
    threefive.decode(stuff)

    # Bytes
    payload = b"\xfc0\x11\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00O%3\x96"
    threefive.decode(payload)

    # Hex String
    stuff = '0XFC301100000000000000FFFFFF0000004F253396'
    threefive.decode(stuff)

    # Hex Literal
    threefive.decode(0XFC301100000000000000FFFFFF0000004F253396)

    # Integer
    big_int = 1439737590925997869941740173214217318917816529814
    threefive.decode(big_int)

    # Mpegts File
    threefive.decode('/path/to/mpegts')

    # Mpegts HTTP/HTTPS Streams
    threefive.decode('https://futzu.com/xaa.ts')

    """
    if stuff in [None, sys.stdin.buffer]:
        # Mpegts stream or file piped in
        return Stream(sys.stdin.buffer).decode()
    if isinstance(stuff, int):
        return _read_stuff(hex(stuff))
    return _read_stuff(stuff)
