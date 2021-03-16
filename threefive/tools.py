"""
tools.py

Stuff used by various classes and methods
throughout threefive.
"""
import json
import sys


def to_stderr(stuff):
    """
    Wrapper for printing to sys.stderr
    """
    print(stuff, file=sys.stderr)


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
