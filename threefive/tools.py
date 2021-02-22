"""
tools.py

Stuff used by various classes and methods
throughout threefive.
"""
import json
import sys


def i2b(i, wide):
    """
    i2b is a wrapper for int.to_bytes
    """
    return int.to_bytes(i, wide, byteorder="big")


def ifb(bites):
    """
    ifb is a wrapper for int.from_bytes
    """
    return int.from_bytes(bites, byteorder="big")


def to_stderr(stuff):
    """
    Wrapper for printing to sys.stderr
    """
    print(stuff, file=sys.stderr)


def k_by_v(adict, avalue):
    """
    dict key lookup by value
    """
    for k, v in adict.items():
        if v == avalue:
            return k


def loader(obj, stuff):
    """
    loader is used to load
    data from a dict or json string
    into a class instance.
    """
    if isinstance(stuff, str):
        stuff = json.loads(stuff)
    if isinstance(stuff, dict):
        obj.__dict__.update(stuff)
