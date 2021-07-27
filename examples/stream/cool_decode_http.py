import sys
import urllib.request
from threefive import Stream

"""
An example using urllib.request for http/https.

Accepts one or more urls to parse for SCTE-35 over http/https.

Usage:

python3 cool_decode_http.py https://futzu.com/xaa.ts https://example.com/video.ts

"""


def parse_http_mpegts(url):
    with urllib.request.urlopen(url) as tsdata:
        Stream(tsdata).decode()


if __name__ == "__main__":
    urls = sys.argv[1:]
    [parse_http_mpegts(url) for url in urls]
