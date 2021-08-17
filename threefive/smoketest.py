"""
smoke_test.py
"""

from .decode import decode

six = {
    "Base64": "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g=",
    "Bytes": b"\xfc0\x11\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00O%3\x96",
    "Hex String": "0XFC301100000000000000FFFFFF0000004F253396",
    "Hex Literal": 0xFC301100000000000000FFFFFF0000004F253396,
    "Integer": 1439737590925997869941740173214217318917816529814,
    "HTTP/HTTPS Streams": "https://futzu.com/xaa.ts",
    "Bad Base64 ": "/DAvAf45AA",
    "Bad File": "/you/me/fake.file",
    "Bad Integer": -0.345,
    " Bad String": "your momma",
}


def _decode_test(test_data):
    passed = "✔"
    failed = "✘"
    try:
        decode(test_data)
        return passed
    except:
        return failed


def smoke_test(tests=None):
    """
    calls threefive.decode using the values in tests.
    """
    if not tests:
        tests = six
    results = {k: _decode_test(v) for k, v in tests.items()}
    print("Smoke Test\n")
    {print(f"{k}  {v}") for k, v in results.items()}


if __name__ == "__main__":
    smoke_test(six)
