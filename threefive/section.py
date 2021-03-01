"""
section.py

SCTE35 Splice Info Section
"""
from bitn import BitBin, NBin
from .base import SCTE35Base

sap_map = {"0x0": "Type 1", "0x1": "Type 2", "0x2": "Type 3", "0x3": "No Sap Type"}


class SpliceInfoSection(SCTE35Base):
    """
    The SCTE-35 splice info section
    data.
    """

    def __init__(self):
        self.table_id = None
        self.section_syntax_indicator = None
        self.private = None
        self.sap_type = None
        self.sap_details = None
        self.section_length = None
        self.protocol_version = None
        self.encrypted_packet = None
        self.encryption_algorithm = None
        self.pts_adjustment = None
        self.cw_index = None
        self.tier = None
        self.splice_command_length = None
        self.splice_command_type = None
        self.descriptor_loop_length = 0

    def __repr__(self):
        return str(vars(self))

    def decode(self, bites):
        bitbin = BitBin(bites)
        self.table_id = bitbin.ashex(8)
        if self.table_id != "0xfc":
            raise Exception("splice_info_section.table_id should be 0xfc")
        self.section_syntax_indicator = bitbin.asflag(1)
        self.private = bitbin.asflag(1)
        self.sap_type = bitbin.ashex(2)
        self.sap_details = sap_map[self.sap_type]
        self.section_length = bitbin.asint(12)
        self.protocol_version = bitbin.asint(8)
        if self.protocol_version != 0:
            raise Exception("splice_info_section.protocol_version should be 0")
        self.encrypted_packet = bitbin.asflag(1)
        self.encryption_algorithm = bitbin.asint(6)
        self.pts_adjustment = bitbin.as90k(33)
        self.cw_index = bitbin.ashex(8)
        self.tier = bitbin.ashex(12)
        self.splice_command_length = bitbin.asint(12)
        self.splice_command_type = bitbin.asint(8)

    def encode(self, nbin=None):
        """
        SpliceInfoSection.encode
        takes the vars from an instance and
        encodes them as bytes.
        """
        nbin = NBin()
        self.table_id = "0xfc"
        nbin.add_hex(self.table_id, 8)  # self.table_id
        self.section_syntax_indicator = False
        nbin.add_flag(self.section_syntax_indicator, 1)  # self.section_syntax_indicator
        self.private = False
        nbin.add_flag(self.private, 1)  # self.private
        if self.sap_type not in sap_map.keys():
            self.sap_type = "0x3"
        self.sap_details = sap_map[self.sap_type]
        nbin.add_hex(self.sap_type, 2)
        if not self.section_length:
            self.section_length = 11
        nbin.add_int(self.section_length, 12)
        if not self.protocol_version:
            self.protocol_version = 0
        nbin.add_int(self.protocol_version, 8)
        if not self.encrypted_packet:
            self.encrypted_packet = False
        nbin.add_flag(self.encrypted_packet)
        if not self.encryption_algorithm:
            self.encryption_algorithm = 0
        nbin.add_int(self.encryption_algorithm, 6)
        if not self.pts_adjustment:
            self.pts_adjustment = 0.0
        nbin.add_90k(self.pts_adjustment, 33)
        if not self.cw_index:
            self.cw_index = "0x0"
        nbin.add_hex(self.cw_index, 8)
        if not self.tier:
            self.tier = "0xfff"
        nbin.add_hex(self.tier, 12)
        if not self.splice_command_length:
            self.splice_command_length = 0
        nbin.add_int(self.splice_command_length, 12)
        if not self.splice_command_type:
            self.splice_command_type = 0
        nbin.add_int(self.splice_command_type, 8)
        return nbin.bites
