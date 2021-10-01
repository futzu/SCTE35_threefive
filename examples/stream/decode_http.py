#!/usr/bin/env pypy3
"""
Parse a mpegts video over http or https

"""
from threefive import Stream

video = "https://futzu.com/xaa.ts"

strm = Stream(video)
strm.decode()
