from .util import time_90k


class Splice_Info_Section:    
    def __init__(self,bs):
        self.table_id =bs.hexed(8)
        self.section_syntax_indicator = bs.boolean(1)
        self.private = bs.boolean(1)
        self.reserved=bs.slice(2)
        self.section_length = bs.slice(12)
        self.protocol_version = bs.slice(8)
        self.encrypted_packet =  bs.boolean(1)
        self.encryption_algorithm =bs.slice(6)
        self.pts_adjustment = time_90k(bs.slice(33))
        self.cw_index = bs.hexed(8)
        self.tier = bs.hexed(12)
        self.splice_command_length = bs.slice(12)
        self.splice_command_type = bs.slice(8)
    
