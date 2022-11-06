"""
crc.py  crc32 function for encoding.

"""

POLY = 0x104C11DB7
INIT_VALUE = 0xFFFFFFFF
SIZE_BITS = 32


def _bytecrc(crc, poly, num):
    mask = 1 << (num - 1)
    i = 8
    while i:
        crc = (crc << 1, crc << 1 ^ poly)[crc & mask != 0]
        i -= 1
    mask = (1 << num) - 1
    crc = crc & mask
    return crc


def _mk_table():
    mask = (1 << SIZE_BITS) - 1
    poly = POLY & mask
    return [_bytecrc(i << (SIZE_BITS - 8), poly, SIZE_BITS) for i in range(256)]


def crc32(data):
    table = _mk_table()
    emvee = memoryview(data)
    crc = INIT_VALUE & 0xFFFFFFFF
    for bite in emvee.tobytes():
        crc = table[bite ^ ((crc >> 24) & 0xFF)] ^ ((crc << 8) & 0xFFFFFF00)
    return crc
