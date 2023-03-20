"""
stuff.py functions and such common to threefive.
"""

from sys import stderr


def print2(stuff=b""):
    """
    print2 prints to 2 aka stderr.
    """
    print(stuff, file=stderr, flush=True)
