"""
threeefive.version

Odd number versions are releases.
Even number versions are testing builds between releases.

Used to set version in setup.py
and as an easy way to check which
version you have installed.
"""
MAJOR = 2
MINOR = 2
MAINTAINENCE = 98


def version():
    """
    version is set in the version_tuple
    to make it immutable.
    """
    return f"{MAJOR}.{MINOR}.{MAINTAINENCE}"


def version_tuple():
    """
    returns MAJOR,MINOR,MAINTAINENCE tuple
    """
    return MAJOR, MINOR, MAINTAINENCE
