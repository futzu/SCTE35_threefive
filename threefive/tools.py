import sys


# splice command types
CMD_TYPES = [5, 6, 7, 255]


def i2b(i, wide):
    """
    i2b is a wrapper for int.to_bytes
    """
    return int.to_bytes(i, wide, byteorder="big")


def ifb(bites):
    """
    ifb is a wrapper for int.from_bytes
    """
    return int.from_bytes(bites, byteorder="big")


def reserve(num):
    head = b"0b"
    one = b"1"
    bits = head + (one * num)
    return int(bits, 2)


def to_stderr(stuff):
    """
    Wrapper for printing to sys.stderr
    """
    print(stuff, file=sys.stderr)
