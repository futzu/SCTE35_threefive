"""
threefive.version

Note: this is an update to the way that the version of Threefive is set.
Originally, the major, minor and patch numbers were defined in this file and
then concatenated to form the version, which was then used in the setup.py
file.
However, this led to a build-time error since the threefive module was being
used before it was built. In order to get around this, the version is now set
from a VERSION file found in the root of the module, following the same
convention as before, e.g. 2.3.75.
It is this VERSION file that needs to be updated when the version of threefive
is to be incremented.
These methods are just for convenience and for backwards compatibility with
any current consumer of the version module.
"""


def version() -> str:
    """
    version prints threefives version as a string
    """
    with open("VERSION", "r", encoding="utf-8") as ver:
        version_from_file = ver.read()
    return version_from_file


def version_number() -> int:
    """
    version_number returns version as an int.
    if version() returns 2.3.01
    version_number will return 2301
    """
    return int(version().replace(".", ""))
