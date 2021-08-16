"""
decode.py

Home of the decode function.

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
        decode is a SCTE-35 decoder function
        with input type auto-detection.
        SCTE-35 data can be parsed with just
        one function call.

        the arg stuff is the input.
        if stuff is not set, decode will attempt
        to read from sys.stdin.buffer.

        if stuff is a file, the file data
        will be read and the type of the data
        will be autodetected and decoded.

        SCTE-35 data is printed in JSON format.

        For more parsing and output control,
        see the Cue and Stream classes.

    Supported inputs:

    [ Base64 ]

            import threefive

            Bee64='/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g='
            threefive.decode(Bee64)


    [ Hex String ]

            import threefive

            hexed = '0XFC301100000000000000FFFFFF0000004F253396'
            threefive.decode(hexed)


    [ Hex Literal ]

            import threefive

            threefive.decode(0XFC301100000000000000FFFFFF0000004F253396)


    [ Integer ]

            import threefive

            big_int = 1439737590925997869941740173214217318917816529814
            threefive.decode(big_int)


    [ Mpegts File ]

            import threefive

            threefive.decode('/path/to/mpegts')


    [ Mpegts HTTP/HTTPS Streams ]

            import threefive

            threefive.decode('https://futzu.com/xaa.ts')


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
        return
    _read_stuff(stuff)
    return
