"""
threeefive.version

Used to set version in setup.py
and as an easy way to check which
version you have installed.
"""
version_tuple = (
    "2.2.35",
    "Made with a renewed enthusiasm and vigor, never seen here before, but very here now.",
)


def version():
    """
    version is set in the version_tuple
    to make it immutable.
    """
    return version_tuple[0]
