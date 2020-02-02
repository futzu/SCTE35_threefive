#!/usr/bin/env python3

import sys
import threefive

"""
example command line tool.
pass in a file name or message string to decode

example:
python cli.py '/DBIAAAAAAAA///wBQb+ek2ItgAyAhdDVUVJSAAAGH+fCAgAAAAALMvDRBEAAAIXQ1VFSUgAABl/nwgIAAAAACyk26AQAACZcuND'

or
python cli.py /path/to/mpeg.ts

"""

threefive.decode(sys.argv[1])
