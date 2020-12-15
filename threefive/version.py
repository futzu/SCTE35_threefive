"""
threeefive.version

Used to set version in setup.py
and as an easy way to check which
version you have installed.
"""
version_tuple = (
    "2.2.43",
    "Two Two forty-three",
)


def version():
    """
    version is set in the version_tuple
    to make it immutable.
    """
    return version_tuple[0]


def full_version():
    return version_tuple
