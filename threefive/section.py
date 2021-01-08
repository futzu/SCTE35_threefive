"""
section.py

SCTE35 Splice Info Section
"""
from threefive.tools import ifb


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
        if self.table_id != "0xfc":
            return False
        self.section_syntax_indicator = bites[1] >> 7 == 1
        self.private = (bites[1] >> 6) & 1 == 1
        self.reserved = hex((bites[1] >> 4) & 3)
        if self.reserved != "0x3":
            return False
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
