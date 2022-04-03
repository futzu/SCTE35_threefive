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
    mv = memoryview(data)
    crc = crc & 0xFFFFFFFF
    for x in mv.tobytes():
        crc = table[x ^ ((crc >> 24) & 0xFF)] ^ ((crc << 8) & 0xFFFFFF00)
    return crc


def _bitrev(x, n):
    y = 0
    for i in range(n):
        y = (y << 1) | (x & 1)
        x = x >> 1
    return y


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


def _verifyParams(poly, initCrc, xorOut):
    sizeBits = _verifyPoly(poly)
    mask = (1 << sizeBits) - 1
    initCrc = initCrc & mask
    xorOut = xorOut & mask
    return (sizeBits, initCrc, xorOut)


def _verifyPoly(poly):
    for n in (8, 16, 24, 32, 64):
        low = 1 << n
        high = low * 2
        if low <= poly < high:
            return n


def _mkTable(poly, n):
    mask = (1 << n) - 1
    poly = poly & mask
    table = [_bytecrc(i << (n - 8), poly, n) for i in range(256)]
    return table


def mkCrcFun(poly, initCrc=~0, rev=True, xorOut=0):
    (sizeBits, initCrc, xorOut) = _verifyParams(poly, initCrc, xorOut)
    return _mkCrcFun(poly, sizeBits, initCrc, rev, xorOut)[0]


def _mkCrcFun(poly, sizeBits, initCrc, rev, xorOut):
    tableList = _mkTable(poly, sizeBits)
    _fun = _crc32
    _table = tableList

    def crcfun(data, crc=initCrc, table=_table, fun=_fun):
        return fun(data, crc, table)

    return crcfun, tableList


def get_crc32_func():
    return mkCrcFun(POLY, initCrc=INIT_VALUE, rev=REVERSE, xorOut=XOR_OUT)
