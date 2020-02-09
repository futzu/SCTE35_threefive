from .scte35var import *
class Splice_Info_Section:
    """
    Table 5 - splice_info_section()
    """
    def __init__(self,bitbin):
        self.table_id = Hexed8()
        self.section_syntax_indicator = Flag()
        self.private = Flag()
        self.reserved = uInt2()
        self.section_length = uInt12()
        self.protocol_version = uInt8()
        self.encrypted_packet = Flag()
        self.encryption_algorithm = uInt6()
        self.pts_adjustment = t90K33()
        self.cw_index = Hexed8()
        self.tier = Hexed12()
        self.splice_command_length = uInt12()
        self.splice_command_type = uInt8()
        self.decode(bitbin)
        self.descriptor_loop_length=uInt16()
 
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
     
      
      