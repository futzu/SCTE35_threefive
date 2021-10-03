"""
The reader function
"""


import urllib.request


def reader(uri):
    """
    reader returns an open file handle
    for files or http(s) urls
    """
    if uri.startswith("http"):
        return urllib.request.urlopen(uri)
    return open(uri, "rb")
