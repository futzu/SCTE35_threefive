class SpliceInfoSection:
    '''
    three5.SpliceInfoSection is used to parse
    the splice info section of SCTE-35 messages.
    '''

    def parse(self, bitbin):
        self.table_id = bitbin.ashex(8)
        self.section_syntax_indicator = bitbin.asflag(1)
        self.private = bitbin.asflag(1)
        self.reserved = bitbin.ashex(2)
        self.section_length = bitbin.asint(12)
        self.protocol_version = bitbin.asint(8)
        self.encrypted_packet = bitbin.asflag(1)
        self.encryption_algorithm = bitbin.asint(6)
        self.pts_adjustment = bitbin.as90k(33)
        self.cw_index = bitbin.ashex(8)
        self.tier = bitbin.ashex(12)
        self.splice_command_length = bitbin.asint(12)
        self.splice_command_type = bitbin.asint(8)
        self.descriptor_loop_length = 0

    def __repr__(self):
        return str(vars(self))
