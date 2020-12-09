"""
threeefive.version

Used to set version in setup.py
and as an easy way to check which
version you have installed.
"""
version_tuple = (
    "2.2.39",
    "Support for parsing Streams with SCTE-35 Cues larger than 183 bytes.",
)


def version():
    """
    version is set in the version_tuple
    to make it immutable.
    """
    return version_tuple[0]


def full_version():
    return version_tuple
