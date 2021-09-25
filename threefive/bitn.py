"""
The bitn.BitBin and bitn.NBin classes
"""


import sys


class BitBin:
    """
    bitn.Bitbin takes a byte string and
    converts it to a integer, a very large integer
    if needed. A 1500 bit integer is no problem.
    several methods are available for slicing off bits.
    """

    def __init__(self, bites):
        # self.bites = bites
        self.bitsize = self.idx = len(bites) << 3
        self.bits = int.from_bytes(bites, byteorder="big")

    def as_90k(self, num_bits):
        """
        Returns num_bits
        of bits as 90k time
        """
        ninetyk = self.as_int(num_bits) / 90000.0
        return round(ninetyk, 6)

    def as_int(self, num_bits):
        """
        Starting at self.idx of self.bits,
        slice off num_bits of bits.
        """
        if self.idx >= num_bits:
            self.idx -= num_bits
            return (self.bits >> (self.idx)) & ~(~0 << num_bits)
        return self.negative_shift(num_bits)

    def as_hex(self, num_bits):
        """
        Returns the hex value
        of num_bits of bits
        """
        return hex(self.as_int(num_bits))

    def as_ascii(self, num_bits):
        """
        Returns num_bits of bits
        as bytes decoded to as_ascii
        """
        stuff = self.as_int(num_bits)
        wide = num_bits >> 3
        return int.to_bytes(stuff, wide, byteorder="big").decode()

    def as_raw(self, num_bits):
        """
        Returns num_bits of bits
        as bytes
        """
        stuff = self.as_int(num_bits)
        wide = num_bits >> 3
        return int.to_bytes(stuff, wide, byteorder="big")

    def as_flag(self, num_bits=1):
        """
        Returns one bit as True or False
        """
        return self.as_int(num_bits) & 1 == 1

    def forward(self, num_bits):
        """
        Advances the start point
        forward by num_bits
        """
        self.idx -= num_bits

    def negative_shift(self, num_bits):
        """
        negative_shift is called instead of
        throwing a negative shift count error.
        """
        print(
            f"{num_bits} bits requested, but only {self.idx} bits left.",
            file=sys.stderr,
        )
        print(
            f"\n bytes remaining: {self.as_raw(self.idx)} ",
            file=sys.stderr,
        )


class NBin:
    """
    bitn.NBin is
    the reverse BitBin.
    Encodes data to integers
    and then bytes
    """

    def __init__(self):
        self.nbits = 0
        self.idx = 0
        self.bites = b""

    def nbits2bites(self):
        """
        nbits2bites converts
        the int self.nbits to bytes as self.bites
        and sets self.nbits  and self.idx to 0
        """
        bites_wide = self.idx >> 3
        self.bites += int.to_bytes(self.nbits, bites_wide, byteorder="big")
        self.nbits = 0
        self.idx = 0

    def add_bites(self, plus_bites):
        """
        add_bites appends plus_bites
        to self.bites
        """
        self.bites += plus_bites
        self.nbits2bites()

    def add_int(self, int_bits, bit_len):
        """
        left shift nbits and append new_bits
        """
        self.idx += bit_len
        self.nbits = (self.nbits << bit_len) | int_bits
        if self.idx % 8 == 0:
            self.nbits2bites()

    def add_90k(self, pts, bit_len=33):
        """
        Converts 90k  float timestamps
        to an int and appends it to nbits
        via self.add_int
        """
        ninetyk = int(pts * 90000.0)
        self.add_int(ninetyk, bit_len)

    def add_hex(self, hex_str, bit_len):
        """
        add_hex converts a
        hex encoded string to an int
        and appends it to self.nbits
        via self.add_int
        """
        dehexed = int(hex_str, 16)
        self.add_int(dehexed, bit_len)

    def add_flag(self, flg, bit_len=1):
        """
        add_flag takes a boolean
        value and adds it as an integer
        to self.nbits via self.add_int
        """
        bit_len = 1
        self.add_int(flg.real, bit_len)

    def reserve(self, num):
        """
        reserve sets 'num'  bits to 1
        and appends them to self.nbits
        via self.add_int
        """
        bit_len = 1
        while num:
            self.add_int(1, bit_len)
            num -= 1

    def forward(self, num):
        """
        Currently just an alias to reserve
        """
        self.reserve(num)

    def zeroed(self, num):
        """
        zeroed sets num bits to zero
        """
        bit_len = 1
        while num:
            self.add_int(0, bit_len)
