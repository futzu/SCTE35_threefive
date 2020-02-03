class Splice_Info_Section:
    """
    Table 5 - splice_info_section()
    """
    def __init__(self, bs = None):
        if not bs: self.novalues()
        else: self.parsevalues(bs)
 
    def novalues(self):
        '''
        create a splice_info_section instance
        with all vars set to None
        '''                 
        self.table_id = None
        self.section_syntax_indicator = None
        self.private = None
        self.reserved = None
        self.section_length = None
        self.protocol_version = None
        self.encrypted_packet = None
        self.encryption_algorithm =None
        self.pts_adjustment = None
        self.cw_index = None
        self.tier = None
        self.splice_command_length = None
        self.splice_command_type = None

    def parsevalues(self, bs):
        '''
        create a splice_info_section instance
        and set vars from bs
        '''
        self.table_id = bs.ashex(8)
        self.section_syntax_indicator = bs.asflag(1)
        self.private = bs.asflag(1)
        self.reserved = bs.asint(2)
        self.section_length = bs.asint(12)
        self.protocol_version = bs.asint(8)
        self.encrypted_packet = bs.asflag(1)
        self.encryption_algorithm = bs.asint(6)
        self.pts_adjustment = bs.as90k(33)
        self.cw_index = bs.ashex(8)
        self.tier = bs.ashex(12)
        self.splice_command_length = bs.asint(12)
        self.splice_command_type = bs.asint(8)
