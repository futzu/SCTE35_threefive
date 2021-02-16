"""
section.py

SCTE35 Splice Info Section
"""
from bitn import BitBin

sap_map = {"0x0": "Type 1", "0x1": "Type 2", "0x2": "Type 3", "0x3": "No Sap Type"}


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
        self.sap_type = None
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
        self.sap_type = sap_map[bitbin.ashex(2)]
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
