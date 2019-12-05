from .util import *


class Splice_Info_Section:    
    def __init__(self,bb):
        self.table_id =hex(bb.read('uint:8'))
        self.section_syntax_indicator = bb.read('bool')
        self.private = bb.read('bool')
        reserved(bb,2)
        self.section_length = bb.read('uint:12')
        self.protocol_version = bb.read('uint:8')
        self.encrypted_packet =  bb.read('bool')
        self.encryption_algorithm =bb.read('uint:6')
        self.pts_adjustment = time_90k(bb.read('uint:33'))
        self.cw_index = hex(bb.read('uint:8'))
        self.tier = hex(bb.read('uint:12'))
        self.splice_command_length = bb.read('uint:12')
        self.splice_command_type = bb.read('uint:8')
         
