"""
section.py

SCTE35 Splice Info Section
"""
from .bitn import BitBin
from .base import SCTE35Base

sap_map = {
    "0x0": "Type 1 Closed GOP with no leading pictures",
    "0x1": "Type 2 Closed GOP with leading pictures",
    "0x2": "Type 3 Open GOP",
    "0x3": "No Sap Type",
}


class SpliceInfoSection(SCTE35Base):
    """
    The SCTE-35 splice info section
    data.
    """

    def __init__(self):
        self.table_id = None
        self.section_syntax_indicator = None
        self.private = None
        # sap_type used to be marked reserved.
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

    def decode(self, bites):
        """
        InfoSection.decode
        """
        bitbin = BitBin(bites)
        self.table_id = bitbin.as_hex(8)
        if self.table_id != "0xfc":
            raise ValueError("splice_info_section.table_id should be 0xfc")
        self.section_syntax_indicator = bitbin.as_flag(1)
        if self.section_syntax_indicator != 0:
            raise ValueError("section_syntax_indicator should be 0")
        self.private = bitbin.as_flag(1)
        self.sap_type = bitbin.as_hex(2)
        self.sap_details = sap_map[self.sap_type]
        self.section_length = bitbin.as_int(12)
        self.protocol_version = bitbin.as_int(8)
        if self.protocol_version != 0:
            raise ValueError("splice_info_section.protocol_version should be 0")
        self.encrypted_packet = bitbin.as_flag(1)
        self.encryption_algorithm = bitbin.as_int(6)
        self.pts_adjustment = bitbin.as_90k(33)
        self.cw_index = bitbin.as_hex(8)
        self.tier = bitbin.as_hex(12)
        self.splice_command_length = bitbin.as_int(12)
        self.splice_command_type = bitbin.as_int(8)
