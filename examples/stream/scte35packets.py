#!/usr/bin/env python3

"""
scte35packets.py 


    print out the raw SCTE-35 packets in a stream or file.


Use like:

    a@slow:~$ python3 scte35packets.py https://futzu.com/xaa.ts

This  functionality is also available in the threefive command line tool:

    threefive packets https://futzu.com/xaa.ts

"""


import sys
from threefive import Stream



class SupaStream(Stream):

    def _parse_scte35(self,pkt,pid):
        print(pkt)
        super()._parse_scte35(pkt,pid)


if __name__ == '__main__':
    args = sys.argv[1:]
    for arg in args:
        supa = SupaStream(arg)
        supa.decode()
