#!/usr/bin/env pypy3
"""
Parse a mpegts video over http or https
without downloading first.
"""
import urllib3
from threefive import Stream

video = "https://futzu.com/xaa.ts"

http = urllib3.PoolManager()
req = http.request("GET", video, preload_content=False)
strm = Stream(req)
strm.decode()

