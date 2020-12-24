#!/usr/bin/env python3
"""

Usage One:
----------

    Pass one or more files,
    Base64 encoded strings,
    or Hex encoded strings
    on the command line.

        pypy3 cli.py ../u.ts \
                /usr/a/35.ts \
                "0xFC301100000000000000FFFFFF0000004F253396" \
                "/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo=" \
                /usr/a/cue.ts


Usage Two:
----------

    Pipe data into cli.py

        cat video.ts | pypy3 cli.py

"""

import sys
import threefive


def do():
    if not sys.argv[1:]:
        threefive.decode()
    else:
        try:
            args = sys.argv[1:]
            for arg in args:
                print(f"Next is {arg}\n\n")
                threefive.decode(arg)
        except:
            pass


if __name__ == "__main__":
    do()
