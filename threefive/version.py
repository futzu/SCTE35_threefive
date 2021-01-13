"""
threeefive.version

Used to set version in setup.py
and as an easy way to check which
version you have installed.
"""
version_tuple = (
    "2.2.53",
    "Two Two fifty-three ..... `",
)


def version():
    """
    version is set in the version_tuple
    to make it immutable.
    """
    return version_tuple[0]


def full_version():
    """
    returns full version tuple
    """
    return version_tuple
