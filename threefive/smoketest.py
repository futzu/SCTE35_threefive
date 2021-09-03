"""
smoke_test.py
"""

from .decode import decode

# The format for tests is a dict of { "test_name" : value to pass to threefive.decode}
ten_tests = {
    "Base64": "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g=",
    "Bytes": b"\xfc0\x11\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00O%3\x96",
    "Hex String": "0XFC301100000000000000FFFFFF0000004F253396",
    "Hex Literal": 0xFC301100000000000000FFFFFF0000004F253396,
    "Integer": 1439737590925997869941740173214217318917816529814,
    "HTTP/HTTPS Streams": "https://futzu.com/xaa.ts",
    # "Bad" tests are expected to fail.
    "Bad Base64 ": "/DAvAf45AA",
    "Bad File": "/you/me/fake.file",
    "Bad Integer": -0.345,
    " Bad String": "your momma",
}


def _decode_test(test_name, test_data):
    passed = "✔"
    failed = "✘"
    print(f"testing {test_name}\n Data: {test_data}\n")
    if decode(test_data):
        return passed
    return failed


def smoke(tests=None):
    """
    calls threefive.decode using the values in tests.
    The format for tests:
    { "test_name" : value to pass to threefive.decode}

    example:

     my_tests ={
    "Base64": "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g=",
    "Bytes": b"\xfc0\x11\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00O%3\x96"
    }

    import threefive
    threefive.smoke_test(my_tests)

    """
    if not tests:
        tests = ten_tests
    results = {k: _decode_test(k, v) for k, v in tests.items()}
    print("Smoke Test\n")
    {print(f"{k}  {v}") for k, v in results.items()}


if __name__ == "__main__":
    smoke()
