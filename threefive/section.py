"""
section.py

SCTE35 Splice Info Section
"""
from bitn import BitBin, NBin
from threefive.tools import ifb, to_stderr


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

    def decode(self, bites):
        bitbin = BitBin(bites)
        self.table_id = bitbin.ashex(8)
        if self.table_id != "0xfc":
            raise ValueError("splice_info_section.table_id should be 0xfc")
        self.section_syntax_indicator = bitbin.asflag(1)
        self.private = bitbin.asflag(1)
        self.reserved = bitbin.ashex(2)
        if self.reserved != "0x3":
            raise ValueError("splice_info_section.reserved should be 0x3")
        self.section_length = bitbin.asint(12)
        self.protocol_version = bitbin.asint(8)
        if self.protocol_version != 0:
            raise ValueError("splice_info_section.protocol_version should be 0")
        self.encrypted_packet = bitbin.asflag(1)
        self.encryption_algorithm = bitbin.asint(6)
        self.pts_adjustment = bitbin.as90k(33)
        self.cw_index = bitbin.ashex(8)
        self.tier = bitbin.ashex(12)
        self.splice_command_length = bitbin.asint(12)
        self.splice_command_type = bitbin.asint(8)
        self.descriptor_loop_length = 0

    def encode(self, nbin=None):
        """
        SpliceInfoSection.encode
        takes the vars from an instance and
        encodes them as bytes.
        """
        if not nbin:
            nbin = NBin()
        nbin.add_hex("0xfc", 8)  # self.table_id
        nbin.add_int(0, 1)  # self.section_syntax_indicator
        nbin.add_int(0, 1)  # self.private
        nbin.reserve(2)
        nbin.add_int(self.section_length, 12)
        nbin.add_int(0, 8)
        nbin.add_flag(self.encrypted_packet)
        nbin.add_int(self.encryption_algorithm, 6)
        nbin.add_90k(self.pts_adjustment, 33)
        nbin.add_hex(self.cw_index, 8)
        nbin.add_hex(self.tier, 12)
        nbin.add_int(self.splice_command_length, 12)
        nbin.add_int(self.splice_command_type, 8)
        return nbin
