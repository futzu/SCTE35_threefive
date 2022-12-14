"""
crc.py  crc32 function for encoding.

"""

POLY = 0x104C11DB7
INIT_VALUE = 0xFFFFFFFF
SIZE_BITS = 32


def _bytecrc(crc, poly):
    mask = 1 << ( SIZE_BITS- 1)   
    i = 8
    while i:
        crc = (crc << 1, crc << 1 ^ poly)[crc & mask != 0]
        i -= 1
    return crc & INIT_VALUE


def _mk_table():
    mask = (1 << SIZE_BITS) - 1
    poly = POLY & mask
    return [_bytecrc(i << (SIZE_BITS - 8), poly) for i in range(256)]


def crc32(data):
    """
    generate a 32 bit crc
    """
    table = _mk_table()
    emvee = memoryview(data)
    crc = INIT_VALUE 
    for bite in emvee.tobytes():
        crc = table[bite ^ ((crc >> 24) & 0xFF)] ^ ((crc << 8) & 0xFFFFFF00)
    return crc

