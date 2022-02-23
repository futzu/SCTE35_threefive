#!/usr/bin/env python3

"""
re_cc.py clears and sets 
continuity counters in mpegts files.

use like:

        python3 re_cc.py video.ts

        
"""

import os
import sys

PACKET_SIZE = 188
PCOUNT = 300

pids = []
counters = []


def set_cc(pkt):
    pid = (pkt[1] & 0x0F) << 8 | pkt[2]
    if pid == 0x1FFF:
        return pkt
    new_cc = 0
    if pid in pids:
        last_cc = counters[pids.index(pid)]
        if last_cc != 15:
            new_cc = last_cc + 1
    pkt[3] &= 0xF0
    pkt[3] += new_cc
    counters[pids.index(pid)] = new_cc
    return pkt


if __name__ == "__main__":
    args = sys.argv[1:]
    for arg in args:
        with open(arg, "rb") as infile:
            with open(f"{arg}.tmp", "wb+") as outfile:
                for chunk in iter(partial(infile.read, PACKET_SIZE * PCOUNT), b""):
                    chunky = memoryview(bytearray(chunk))
                    chunks = [
                        set_cc(chunky[i : i + PACKET_SIZE])
                        for i in range(0, len(chunky), PACKET_SIZE)
                    ]
                    outfile.write(b"".join(chunks))

        os.rename(outfile, infile)
