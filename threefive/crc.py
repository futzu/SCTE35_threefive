"""
crc.py  crc32 function for encoding.
"""

POLY = 0x104C11DB7
INIT_VALUE = 0xFFFFFFFF
FOUR_BYTES = 0x20
THREE_BYTES = 0x18


def _bytecrc(crc, poly):
    mask = 1 << (FOUR_BYTES - 1)
    i = 8
    while i:
        crc = (crc << 1, crc << 1 ^ poly)[crc & mask != 0]
        i -= 1
    return crc & INIT_VALUE


def _mk_table():
    mask = (1 << FOUR_BYTES) - 1
    poly = POLY & mask
    return [_bytecrc((i << THREE_BYTES), poly) for i in range(256)]


def crc32(data):
    """
    generate a 32 bit crc
    """
    table = _mk_table()
    crc = INIT_VALUE
    for bite in data:
        crc = table[bite ^ ((crc >> THREE_BYTES) & 0xFF)] ^ ((crc << 8) & 0xFFFFFF00)
    return crc
