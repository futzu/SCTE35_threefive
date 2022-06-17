"""
crc.py  comes entirely and completely from the crcmod module,
I just took the parts I need to use.

I am including the crcmod authors copyright below.

Thank you Raymond L. Buvel and Craig McQueen.

~ Adrian

"""
# -----------------------------------------------------------------------------
# Copyright (c) 2010  Raymond L. Buvel
# Copyright (c) 2010  Craig McQueen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# -----------------------------------------------------------------------------


POLY = 0x104C11DB7
INIT_VALUE = 0xFFFFFFFF
REVERSE = False
XOR_OUT = 0x00000000
CHECK = 0x0376E6E7


def _crc32(data, crc, table):
    emvee = memoryview(data)
    crc = crc & 0xFFFFFFFF
    for ex in emvee.tobytes():
        crc = table[ex ^ ((crc >> 24) & 0xFF)] ^ ((crc << 8) & 0xFFFFFF00)
    return crc


def _bitrev(ex, en):
    why = 0
    for i in range(en):
        why = (why << 1) | (ex & 1)
        ex = ex >> 1
    return why


def _bytecrc(crc, poly, n):
    mask = 1 << (n - 1)
    for i in range(8):
        if crc & mask:
            crc = (crc << 1) ^ poly
        else:
            crc = crc << 1
    mask = (1 << n) - 1
    crc = crc & mask
    return crc


def _verify_params(poly, init_crc, xor_out):
    size_bits = _verifyPoly(poly)
    mask = (1 << size_bits) - 1
    init_crc = init_crc & mask
    xor_out = xor_out & mask
    return (size_bits, init_crc, xor_out)


def _verifyPoly(poly):
    for n in (8, 16, 24, 32, 64):
        low = 1 << n
        high = low * 2
        if low <= poly < high:
            return n


def _mk_table(poly, n):
    mask = (1 << n) - 1
    poly = poly & mask
    table = [_bytecrc(i << (n - 8), poly, n) for i in range(256)]
    return table


def mk_crc_func(poly, init_crc=~0, xor_out=0):
    (size_bits, init_crc, xor_out) = _verify_params(poly, init_crc, xor_out)
    return _mk_crc_func(poly, size_bits, init_crc)[0]


def _mk_crc_func(poly, size_bits, init_crc):
    table_list = _mk_table(poly, size_bits)
    _fun = _crc32
    _table = table_list

    def crcfun(data, crc=init_crc, table=_table, fun=_fun):
        return fun(data, crc, table)

    return crcfun, table_list


def get_crc32_func():
    return mk_crc_func(POLY, init_crc=INIT_VALUE, xor_out=XOR_OUT)
