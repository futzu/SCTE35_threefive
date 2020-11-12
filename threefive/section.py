from base64 import b64encode
import sys
from bitn import BitBin

class SpliceInfoSection:

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

    def decode(self, bites):
        bitbin = BitBin(bites)
        self.table_id = bitbin.ashex(8)
        if self.table_id != '0xfc':
            print('splice info section table id should be 0xfc', file=sys.stderr)
        self.section_syntax_indicator = bitbin.asflag(1)
        self.private = bitbin.asflag(1)
        self.reserved = bitbin.ashex(2)
        if self.reserved != '0x3':
            print('splice info section reserved should be 0x3', file=sys.stderr)
        self.section_length = bitbin.asint(12)
        self.protocol_version = bitbin.asint(8)
        if self.protocol_version != 0:
            print('splice info section protocol version should be 0', file=sys.stderr)
        self.encrypted_packet = bitbin.asflag(1)
        self.encryption_algorithm = bitbin.asint(6)
        self.pts_adjustment = bitbin.as90k(33)
        self.cw_index = bitbin.ashex(8)
        self.tier = bitbin.ashex(12)
        self.splice_command_length = bitbin.asint(12)
        self.splice_command_type = bitbin.asint(8)
        self.descriptor_loop_length = 0

    def encode(self):
        '''
        first byte is:
            table_id
        '''
        first_byte = int(self.table_id, 16)
        bencoded = int.to_bytes(first_byte, 1, byteorder='big')
        '''
        two_bytes is:
            section_syntax_indicator
            private
            reserved
            section_length
        '''
        two_bytes = 0
        if self.section_syntax_indicator:
            two_bytes = (1 << 15)
        if self.private:
            two_bytes += (self.private << 14)
        two_bytes += (int(self.reserved,  16) << 12)
        two_bytes += self.section_length
        bencoded += int.to_bytes(two_bytes, 2, byteorder='big')
        '''
        proto_byte is:
            protocol_version
        '''
        proto_byte = self.protocol_version
        bencoded += int.to_bytes(proto_byte, 1, byteorder='big')
        '''
        five_bytes is:
            encrypted_packet
            encryption_algorithm
            pts_adjustment
        '''
        five_bytes = 0
        if self.encrypted_packet:
            five_bytes = (1 << 39)
        five_bytes += (self.encryption_algorithm  << 33)
        five_bytes += int(self.pts_adjustment  * 90000)
        bencoded += int.to_bytes(five_bytes, 5, byteorder='big')
        '''
        cw_byte is:
            cw_index
        '''
        cw_byte = int(self.cw_index, 16)
        bencoded += int.to_bytes(cw_byte, 1, byteorder='big')
        '''
        three_bytes is:
            tier
            splice_command_length
        '''
        three_bytes = (int(self.tier, 16) << 12)
        three_bytes += self.splice_command_length
        bencoded += int.to_bytes(three_bytes, 3, byteorder='big')
        '''
        cmd_byte is:
            splice_command_type
        '''
        cmd_byte = self.splice_command_type
        bencoded += int.to_bytes(cmd_byte, 1, byteorder='big')
        print(bencoded)
        print(b64encode(bencoded))
