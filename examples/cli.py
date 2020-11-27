#!/usr/bin/env python3

import sys
import threefive


def do():
    try:
        threefive.decode(sys.argv[1])
    except:
        # Handles piped in data
        try:
            threefive.decode()
        except:
            pass


if __name__ == "__main__":
    do()
