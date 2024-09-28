"""
stuff.py functions and such common to threefive.
"""

from sys import stderr


def print2(stuff=b""):
    """
    print2 prints to 2 aka stderr.
    """
    print(stuff, file=stderr, flush=True)


class dottable_dict(dict):
    """ dict implementing methods required to use dot notation """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__

