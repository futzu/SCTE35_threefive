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
        self.crc = None

    def decode(self, bites):
        """
        InfoSection.decode
        """
        bitbin = BitBin(bites)
        self.table_id = bitbin.as_hex(8)
        if self.table_id != "0xfc":
            raise ValueError(
                ("splice_info_section.table_id should be 0xfc Not: ", self.table_id)
            )
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

    def _encode_table_id(self, nbin):
        """
        encode SpliceInfoSection.table_id
        """
        self.table_id = "0xfc"
        nbin.add_hex(self.table_id, 8)

    def _encode_section_syntax_indicator(self, nbin):
        """
        encode SpliceInfoSection.section_syntax_indicator
        """
        self.section_syntax_indicator = False
        nbin.add_flag(self.section_syntax_indicator, 1)

    def _encode_private_flag(self, nbin):
        """
        encode SpliceInfoSection.private
        """
        self.private = False
        nbin.add_flag(self.private, 1)

    def _encode_sap(self, nbin):
        """
        the 3 reserved bits now map SAP
        """
        if self.sap_type not in sap_map.keys():
            self.sap_type = "0x3"
        self.sap_details = sap_map[self.sap_type]
        nbin.add_hex(self.sap_type, 2)

    def _encode_section_length(self, nbin):
        """
        encode SpliceInfoSection.section_length
        """
        if not self.section_length:
            self.section_length = 11
        nbin.add_int(self.section_length, 12)

    def _encode_protocol_version(self, nbin):
        """
        encode SpliceInfoSection.protocol_version
        """
        if not self.protocol_version:
            self.protocol_version = 0
        nbin.add_int(self.protocol_version, 8)

    def _encode_encrypted(self, nbin):
        """
        encode SpliceInfoSection.encrypted_packet
        and SpliceInfoSection.encyption_algorithm
        """
        if not self.encrypted_packet:
            self.encrypted_packet = False
        nbin.add_flag(self.encrypted_packet)
        if not self.encryption_algorithm:
            self.encryption_algorithm = 0
        nbin.add_int(self.encryption_algorithm, 6)

    def _encode_pts_adjustment(self, nbin):
        """
        encode SpliceInfoSection.pts_adjustment
        """
        if not self.pts_adjustment:
            self.pts_adjustment = 0.0
        nbin.add_90k(self.pts_adjustment, 33)

    def _encode_cw_index(self, nbin):
        """
        encode SpliceInfoSection.cw_index
        """
        if not self.cw_index:
            self.cw_index = "0x0"
        nbin.add_hex(self.cw_index, 8)

    def _encode_tier(self, nbin):
        """
        encode SpliceInfoSection.tier
        """
        if not self.tier:
            self.tier = "0xfff"
        nbin.add_hex(self.tier, 12)

    def _encode_splice_command(self, nbin):
        """
        encode Splice.InfoSection.splice_command_length
        and Splice.InfoSection.splice_command_type
        """
        if not self.splice_command_length:
            self.splice_command_length = 0
        nbin.add_int(self.splice_command_length, 12)
        if not self.splice_command_type:
            self.splice_command_type = 0
        nbin.add_int(self.splice_command_type, 8)

    def encode(self, nbin=None):
        """
        SpliceInfoSection.encode
        takes the vars from an instance and
        encodes them as bytes.
        """
        nbin = self._chk_nbin(nbin)
        self._encode_table_id(nbin)
        self._encode_section_syntax_indicator(nbin)
        self._encode_private_flag(nbin)
        self._encode_sap(nbin)
        self._encode_section_length(nbin)
        self._encode_protocol_version(nbin)
        self._encode_encrypted(nbin)
        self._encode_pts_adjustment(nbin)
        self._encode_cw_index(nbin)
        self._encode_tier(nbin)
        self._encode_splice_command(nbin)
        return nbin.bites
