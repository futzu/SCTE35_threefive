
class Splice_Info_Section: 
    '''
    Table 5 - splice_info_section()
    '''   
    def __init__(self,bs):
        self.table_id =bs.ashex(8)
        self.section_syntax_indicator = bs.asflag(1)
        self.private = bs.asflag(1)
        self.reserved=bs.asint(2)
        self.section_length = bs.asint(12)
        self.protocol_version = bs.asint(8)
        self.encrypted_packet =  bs.asflag(1)
        self.encryption_algorithm =bs.asint(6)
        self.pts_adjustment = bs.as90k(33)
        self.cw_index = bs.ashex(8)
        self.tier = bs.ashex(12)
        self.splice_command_length = bs.asint(12)
        self.splice_command_type = bs.asint(8)
    
