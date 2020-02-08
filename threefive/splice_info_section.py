from .scte35var import *
class Splice_Info_Section:
    """
    Table 5 - splice_info_section()
    """
    def __init__(self,bitbin):
        self.table_id = S35Hex8()
        self.section_syntax_indicator = S35Flag()
        self.private = S35Flag()
        self.reserved = S35Int2()
        self.section_length = S35Int12()
        self.protocol_version = S35Int8()
        self.encrypted_packet = S35Flag()
        self.encryption_algorithm = S35Int6()
        self.pts_adjustment = S3590K(33)
        self.cw_index = S35Hex8()
        self.tier = S35Hex12()
        self.splice_command_length = S35Int12()
        self.splice_command_type = S35Int8()
        self.decode(bitbin)
        self.descriptor_loop_length=S35Int16()
 
    def decode(self,bitbin):               
        self.table_id.do(bitbin)
        self.section_syntax_indicator.do(bitbin)
        self.private.do(bitbin)
        self.reserved.do(bitbin)
        self.section_length.do(bitbin)
        self.protocol_version.do(bitbin)
        self.encrypted_packet.do(bitbin)
        self.encryption_algorithm.do(bitbin)
        self.pts_adjustment.do(bitbin)
        self.cw_index.do(bitbin)
        self.tier.do(bitbin)
        self.splice_command_length.do(bitbin)
        self.splice_command_type.do(bitbin)
     
      
      