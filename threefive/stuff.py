"""
stuff.py functions and such common to threefive.
"""

from sys import stderr


def print2(stuff=b""):
    """
    print2 prints to 2 aka stderr.
    """
    print(stuff, file=stderr, flush=True)


def camel_case(k):
    """
    camel_case changes camel case xml names
    to underscore_format names.
    """
    k = "".join([f"_{i.lower()}" if i.isupper() else i for i in k])
    return (k, k[1:])[k[0] == "_"]


def convert_xml_value(v):
    """
    convert_xml_value converts an xml value
    to ints, floats and booleans.
    """
    if v.isdigit():
        return int(v)
    if v.replace(".", "").isdigit():
        return float(v)
    if v in ["false", "False"]:
        return False
    if v in ["true", "True"]:
        return True
    return v
"""
stuff.py functions and such common to threefive.
"""

from sys import stderr


def print2(stuff=b""):
    """
    print2 prints to 2 aka stderr.
    """
    print(stuff, file=stderr, flush=True)
