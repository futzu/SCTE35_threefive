import sys
from threefive import Stream

"""
Stream.proxy example.
writes SCTE-35 data to stderr
writes the MPEG-TS packets to stdout
so you can pipe it.

Example:

python3 proxydemo.py video.ts | mplayer -

"""


def do():
    with open(sys.argv[1], "rb") as tsdata:
        st = Stream(tsdata)
        st.decode_proxy()


if __name__ == "__main__":
    do()

