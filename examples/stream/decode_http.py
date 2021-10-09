"""
Parse a mpegts video over http or https

"""

from threefive import Stream

VID = "https://futzu.com/xaa.ts"

strm = Stream(VID)
strm.decode()
