"""
Stream.proxy example.
writes SCTE-35 data to stderr
writes the MPEG-TS packets to stdout
so you can pipe it.

Example:

python3 decode_proxy.py video.ts | mplayer -

"""
import sys
from threefive import Stream


def do():
    """
    do creates a  Stream instance with sys.argv[1]
    and then calls Stream.decode_proxy()
    """
    strm = Stream(sys.argv[1])
    strm.decode_proxy()


if __name__ == "__main__":
    do()
