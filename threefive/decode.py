"""
decode.py

decode is a SCTE-35 decoder function
with input type auto-detection.

SCTE-35 data can be parsed with just
one function call.

the arg stuff is the input.
if stuff is not set, decode will attempt
to read mpegts video from sys.stdin.buffer.

if stuff is a file, the file data
will be read and the type of the data
will be autodetected and decoded.

SCTE-35 data is printed in JSON format.

For more parsing and output control,
see the Cue and Stream classes.

"""

import sys

from .cue import Cue
from .stream import Stream
from .reader import reader

# Maximum size for a SCTE35 cue.
_MAX_CUE_SIZE = 4096


def _decode_and_show(stuff):
    cue = Cue(stuff)
    if cue.decode():
        cue.show()
        return True
    return False


def _read_stuff(stuff):

    try:
        # Base64, Hex, Bytes, or Int Cues in a File
        with reader(stuff) as tsdata:
            tsd = tsdata.read(_MAX_CUE_SIZE)
            _decode_and_show(tsd)
            return True
    except:
        try:
            # Mpegts Video
            strm = Stream(stuff)
            strm.decode()
            return True
        except:
            try:
                # Base64, Hex, Bytes, or Int Cue Strings
                _decode_and_show(stuff)
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
