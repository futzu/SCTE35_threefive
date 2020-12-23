"""
section.py

SCTE35 Splice Info Section
"""
from base64 import b64encode
from threefive.tools import i2b, ifb, to_stderr


class SpliceInfoSection:
    """
    The SCTE-35 splice info section
    data.
    """

    def __init__(self):
        self.table_id = None
        self.section_syntax_indicator = None
        self.private = None
        self.reserved = None
        self.section_length = None
        self.protocol_version = None
        self.encrypted_packet = None
        self.encryption_algorithm = None
        self.pts_adjustment = None
        self.cw_index = None
        self.tier = None
        self.splice_command_length = None
        self.splice_command_type = None
        self.descriptor_loop_length = None

    def __repr__(self):
        return str(vars(self))

    def _parse_pts_adjustment(self, bites):
        """
        parse the 33 bit pts_adjustment
        from bites
        """
        self.pts_adjustment = bites[4] & 1 << 32
        self.pts_adjustment |= ifb(bites[5:9])
        self.pts_adjustment /= 90000.0

    def decode(self, bites):
        """
        decode the SCTE35 splice info section
        from bites
        """
        self.table_id = hex(bites[0])
        self.section_syntax_indicator = bites[1] >> 7 == 1
        self.private = (bites[1] >> 6) & 1 == 1
        self.reserved = hex((bites[1] >> 4) & 3)
        self.section_length = (bites[1] & 15) << 8 | bites[2]
        self.protocol_version = bites[3]
        self.encrypted_packet = bites[4] >> 7 == 1
        self.encryption_algorithm = (bites[4] >> 1) & 63
        self._parse_pts_adjustment(bites)
        self.cw_index = hex(bites[9])
        self.tier = hex(bites[10] << 4 | (bites[11] >> 4) & 15)
        self.splice_command_length = (bites[11] & 15) << 8 | bites[12]
        self.splice_command_type = bites[13]
        self.descriptor_loop_length = 0

    def encode(self):
        """
        encode the SCTE35 splice info section
        """
        first_byte = int(self.table_id, 16)
        bencoded = i2b(first_byte, 1)

        two_bytes = 0
        if self.section_syntax_indicator:
            two_bytes = 1 << 15
        if self.private:
            two_bytes += self.private << 14
        two_bytes += int(self.reserved, 16) << 12
        two_bytes += self.section_length
        bencoded += i2b(two_bytes, 2)

        proto_byte = self.protocol_version
        bencoded += i2b(proto_byte, 1)

        five_bytes = 0
        if self.encrypted_packet:
            five_bytes = 1 << 39
        five_bytes += self.encryption_algorithm << 33
        five_bytes += int(self.pts_adjustment * 90000)
        bencoded += i2b(five_bytes, 5)

        cw_byte = int(self.cw_index, 16)
        bencoded += i2b(cw_byte, 1)

        three_bytes = int(self.tier, 16) << 12
        three_bytes += self.splice_command_length
        bencoded += i2b(three_bytes, 3)

        cmd_byte = self.splice_command_type
        bencoded += i2b(cmd_byte, 1)
        to_stderr(bencoded)
        to_stderr(b64encode(bencoded))
