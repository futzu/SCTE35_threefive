from .splice_commands import *
from .descriptors import *
from .splice_info_section import Splice_Info_Section
from  bitn import BitBin
import base64
import json


class Splice:

    descriptor_map = {0: Avail_Descriptor,
                    1: Dtmf_Descriptor,
                    2: Segmentation_Descriptor,
                    3: Time_Descriptor,
                    4: Audio_Descriptor}   

    command_map = { 0: Splice_Null,
                4: Splice_Schedule,
                5: Splice_Insert,
                6: Time_Signal,
                7: Bandwidth_Reservation,
                255: Private_Command}

    def __init__(self,mesg):
        mesg=self.mkbits(mesg)
        self.bitbin=BitBin(mesg)
        self.descriptors=[]
        self.info_section= None
        self.command = None
        self.do()
        
    def do(self):        
        self.info_section=Splice_Info_Section(self.bitbin)
        self.set_splice_command() 
        self.descriptorloop()
        self.info_section.crc=self.bitbin.ashex(32)

    def descriptorloop(self):
        self.info_section.descriptor_loop_length=self.bitbin.asint(16)
        dll=self.info_section.descriptor_loop_length
        tag_plus_header_size=2 # 1 byte for descriptor_tag, 1 byte for header?
        while dll> 0:
            try: 
                sd=self.set_splice_descriptor()
                sdl=sd.descriptor_length
                self.descriptors.append(sd)
            except: sdl=0
            bit_move=sdl+ tag_plus_header_size
            dll -=(bit_move)


    def kvprint(self,obj):
        print(f'{json.dumps(vars(obj))}')
                                                            
    def sectionstart(self, section_name):
        print(f'{section_name}')
                                                                                                                                                                                              
 
    def mkbits(self,s):
        if s[:2].lower()=='0x': s=s[2:]
        if s[:2].lower()=='fc': return bytes.fromhex(s)
        try: return base64.b64decode(s)
        except: return s

    def set_splice_command(self):
        sct=self.info_section.splice_command_type
        if sct not in self.command_map.keys():
            raise ValueError('unknown splice command type') 
        self.command = self.command_map[sct](self.bitbin)
    
   
    def set_splice_descriptor(self):
        # splice_descriptor_tag 8 uimsbf
        tag= self.bitbin.asint(8)
        if tag in self.descriptor_map.keys(): 
            return self.descriptor_map[tag](self.bitbin,tag)
                
    def show_info_section(self):
        if self.info_section and self.command:
            self.sectionstart('Splice Info Section')
            self.kvprint(self.info_section)
        else:
            return False
            
    def show_command(self):
        if self.command:
            self.sectionstart('Splice Command')
            self.kvprint(self.command)
        else:
            return False
            	
    def show_descriptors(self):
        if len(self.descriptors) > 0:
            for d in self.descriptors:
                idx=self.descriptors.index(d)
                self.sectionstart(f'Splice Descriptor {idx}')
                self.kvprint(d)
		
    def show(self):
        if self.info_section and self.command:
            self.sectionstart('[SCTE 35 Message]')
            self.show_info_section()
            self.show_command()
            self.show_descriptors()
        else:
        
            return False
	
