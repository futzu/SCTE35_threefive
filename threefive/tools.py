from base64 import b64decode
import json
import sys


# splice command types
CMD_TYPES = [4, 5, 6, 7, 255]


def as_json(obj):
    """
    get_json()
    returns obj as json.
    """
    return json.dumps(obj, indent=2)


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


def parse_pid(byte1, byte2):
    """
    parse pid from packet
    """
    return (byte1 & 31) << 8 | byte2


def kv_clean(obj):
    """
    kv_clean removes items from a dict if the value is None
    """
    return {k: v for k, v in obj.items() if v is not None}


def kv_print(obj):
    """
    kv_print is a wrapper for printing
    a json dump of obj to sys.stderr
    """
    to_stderr(as_json(obj))


def mk_bits(stuff):
    """
    Convert Hex and Base64 strings into bytes.
    """
    if stuff[:2].lower() == "0x":
        stuff = stuff[2:]
    if stuff[:2].lower() == "fc":
        return bytes.fromhex(stuff)
    try:
        return b64decode(stuff)
    except Exception:
        return stuff


def mk_payload(data):
    """
    mkpayload strips off packet headers
    when present
    """
    if data[0] == 0x47:
        payload = data[5:]
    else:
        payload = mk_bits(data)
    return payload


def to_stderr(stuff):
    """
    Wrapper for printing to sys.stderr
    """
    print(stuff, file=sys.stderr)
