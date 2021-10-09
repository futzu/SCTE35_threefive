"""
Accepts one or more urls to parse for SCTE-35 over http/https.

Usage:

python3 cool_decode_http.py https://futzu.com/xaa.ts https://example.com/video.ts

"""

import sys
from threefive import Stream


if __name__ == "__main__":
    Urls = sys.argv[1:]
    streams = [Stream(url) for url in Urls]
    for stream in streams:
        stream.decode()
