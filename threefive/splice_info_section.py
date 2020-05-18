class Splice_Info_Section:

    def __init__(self):
        pass

    def decode(self, bitbin):
        self.table_id = bitbin.ashex(8) 
        if self.table_id != '0xfc':
            raise ValueError('splice_info_section.table_id should be 0xfc')   
        self.section_syntax_indicator = bitbin.asflag(1) 
        if self.section_syntax_indicator:
            raise ValueError('splice_info_section.section_syntax_indicator should be False')    
        self.private = bitbin.asflag(1) 
        if self.private:
            raise ValueError('splice_info_section.private should be False')    
        self.reserved = bitbin.ashex(2)
        if self.reserved != '0x3':
            raise ValueError('splice_info_section.reserved should be 0x3')
        self.section_length = bitbin.asint(12)
        if self.section_length > 4093:
            raise ValueError('splice_info_section.section_length cannot be greater than 4093') 
        self.protocol_version = bitbin.asint(8)
        if self.protocol_version != 0:
            raise ValueError('splice_info_section.protocol_version should be 0') 
        self.encrypted_packet = bitbin.asflag(1)
        self.encryption_algorithm = bitbin.asint(6)
        self.pts_adjustment = bitbin.as90k(33)
        self.cw_index = bitbin.ashex(8)
        self.tier = bitbin.ashex(12)
        if int(self.tier,16) > 4095:
            raise ValueError('splice_info_section.tier should less than 0xfff')
        self.splice_command_length = bitbin.asint(12)
        self.splice_command_type = bitbin.asint(8)
        self.descriptor_loop_length = False

    def encode(self):
        '''
        first byte is:
            table_id
        '''
        first_byte = int(self.table_id,16) 
        bencoded = int.to_bytes(first_byte, 1, byteorder='big')
        '''
        two_bytes is:
            section_syntax_indicator
            private
            reserved
            section_length
        '''
        two_bytes = 0 
        if self.section_syntax_indicator: two_bytes = (1 << 15)
        if self.private: two_bytes += (self.private << 14)
        two_bytes += (int(self.reserved,16) << 12)
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
        if self.encrypted_packet: five_bytes = (1 << 39)
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
