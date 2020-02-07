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
        #inv=mesg
        mesg=self.mkbits(mesg)
        bitbin=BitBin(mesg)
        self.descriptors=[]
        self.info_section=Splice_Info_Section(bitbin)
        self.set_splice_command(bitbin) 
        self.descriptorloop(bitbin)
        self.info_section.crc=bitbin.ashex(32)

    def descriptorloop(self,bitbin):
        self.info_section.descriptor_loop_length.do(bitbin) 
        dll=self.info_section.descriptor_loop_length.value
        tag_plus_header_size=2 # 1 byte for descriptor_tag, 1 byte for header?
        while dll> 0:
            try: 
                sd=self.set_splice_descriptor(bitbin)
                sdl=sd.descriptor_length
                self.descriptors.append(sd)
            except: sdl=0
            bit_move=sdl+ tag_plus_header_size
            dll -=(bit_move)


    def kvprint(self,obj):
        stuff=[]
        for k,v in vars(obj).items():
            try:
                stuff.append(f'{k} :{v.value}')
            except:
                stuff.append(f'{k} :{v}')

        print(' '.join(stuff))
                                                            
    def sectionstart(self, section_name):
        print(f'{section_name}')
                                                                                                                                                                                              
 
    def mkbits(self,s):
        if s[:2].lower()=='0x': s=s[2:]
        if s[:2].lower()=='fc': return bytes.fromhex(s)
        try: return base64.b64decode(s)
        except: return s

    def set_splice_command(self,bitbin):

        sct=self.info_section.splice_command_type.value
        if sct in self.command_map.keys(): 
            self.command = self.command_map[sct](bitbin)
   
    def set_splice_descriptor(self,bitbin):
        # splice_descriptor_tag 8 uimsbf
        tag= bitbin.asint(8)
        if tag in self.descriptor_map.keys(): 
            return self.descriptor_map[tag](bitbin,tag)
                
    def show_info_section(self):
        self.sectionstart('Splice Info Section')
        self.kvprint(self.info_section)

    def show_command(self):
        self.sectionstart('Splice Command')
        self.kvprint(self.command)
		
    def show_descriptors(self):
        for d in self.descriptors:
            idx=self.descriptors.index(d)
            self.sectionstart(f'Splice Descriptor {idx}')
            self.kvprint(d)
		
    def show(self):
        self.sectionstart('[SCTE 35 Message]')
        self.show_info_section()
        self.show_command()
        self.show_descriptors()
	
