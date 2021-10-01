import sys
from threefive import Stream

"""

Accepts one or more urls to parse for SCTE-35 over http/https.

Usage:

python3 cool_decode_http.py https://futzu.com/xaa.ts https://example.com/video.ts

"""


if __name__ == "__main__":
    urls = sys.argv[1:]
    [Stream(url).decode() for url in urls]
