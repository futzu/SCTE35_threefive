"""
threeefive.version

Used to set version in setup.py
and as an easy way to check which
version you have installed.
"""
version_tuple = ("2.2.31", "StreamB, The Underground Legend Returns"  )


def version():
    """
    version is set in the version_tuple
    to make it immutable.
    """
    return version_tuple[0]
