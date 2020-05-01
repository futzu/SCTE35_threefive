class Splice_Info_Section:
    def __init__(self):
         pass

    def __repr__(self):
        return str(vars(self))

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
        self.reserved = bitbin.asint(2)
        if self.reserved != 0x3:
            raise ValueError('splice_info_section.reserved should be 0x3')
        self.section_length = bitbin.asint(12)
        self.protocol_version = bitbin.asint(8)
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

    def get(self):
        return vars(self)
