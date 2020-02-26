class Splice_Info_Section:
    def __init__(self):
        self.table_id = None
        self.section_syntax_indicator = None
        self.private = None
        self.reserved = None
        self.section_length = None
        self.protocol_version = None
        self.encrypted_packet =  None
        self.encryption_algorithm = None
        self.pts_adjustment = None
        self.cw_index = None
        self.tier = None
        self.splice_command_length = None
        self.splice_command_type = None
        self.descriptor_loop_length = False
        self.crc = None

    def decode(self,bitbin):
        self.table_id = bitbin.ashex(8)
        self.section_syntax_indicator = bitbin.asflag(1)
        self.private = bitbin.asflag(1)
        self.reserved = bitbin.asint(2)
        if self.reserved != 0x3:
            raise ValueError('splice_info_section.reserved should be 0x3')
        self.section_length = bitbin.asint(12)
        self.protocol_version = bitbin.asint(8)
        self.encrypted_packet =  bitbin.asflag(1)
        self.encryption_algorithm = bitbin.asint(6)
        self.pts_adjustment = bitbin.as90k(33)
        self.cw_index = bitbin.ashex(8)
        self.tier = bitbin.ashex(12)
        self.splice_command_length = bitbin.asint(12)
        self.splice_command_type = bitbin.asint(8)
        self.descriptor_loop_length = False
