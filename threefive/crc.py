"""
crc.py  crc32 function for encoding.
"""

POLY = 0x104C11DB7
INIT_VALUE = 0xFFFFFFFF
ZERO = 0x0
ONE = 0x1
EIGHT = 0x8
TWENTY_FOUR = 0x18
THIRTY_TWO = 0x20
TWO_FIFTY_FIVE = 0xFF
TWO_FIFTY_SIX = 0x100


def _bytecrc(crc, poly):
    mask = ONE << (THIRTY_TWO - ONE)
    i = EIGHT
    while i:
        crc = (crc << ONE, crc << ONE ^ poly)[crc & mask != ZERO]
        i -= ONE
    return crc & INIT_VALUE


def _mk_table():
    mask = (ONE << THIRTY_TWO) - ONE
    poly = POLY & mask
    return [_bytecrc((i << TWENTY_FOUR), poly) for i in range(TWO_FIFTY_SIX)]


def crc32(data):
    """
    generate a 32 bit crc
    """
    table = _mk_table()
    crc = INIT_VALUE
    for bite in data:
        crc = table[bite ^ ((crc >> TWENTY_FOUR) & TWO_FIFTY_FIVE)] ^ (
            (crc << EIGHT) & (INIT_VALUE - TWO_FIFTY_FIVE)
        )
    return crc
