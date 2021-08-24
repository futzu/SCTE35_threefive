""
threeefive.version

Odd number versions are releases.
Even number versions are testing builds between releases.

Used to set version in setup.py
and as an easy way to check which
version you have installed.
"""

MAJOR = 2
MINOR = 2
MAINTAINENCE = 99


def version():
    """
    version prints threefive's version as a string
    """
    print(f"{MAJOR}.{MINOR}.{MAINTAINENCE}")


def version_number():
    """
    version_number returns threefive's version
    as an int for easy checking.
    """
    return (MAJOR * 1000) + (MINOR * 100) + MAINTAINENCE
