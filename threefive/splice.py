from .splice_commands import *
from .descriptors import *
from .splice_info_section import Splice_Info_Section
from  bitslicer9k import Slicer9k
import base64


descriptor_map={0: Avail_Descriptor,
                1: Dtmf_Descriptor,
                2: Segmentation_Descriptor,
                3: Time_Descriptor,
                4: Audio_Descriptor}   

command_map={ 0: Splice_Null,
            4: Splice_Schedule,
            5: Splice_Insert,
            6: Time_Signal,
            7: Bandwidth_Reservation,
            255: Private_Command}


class Splice:
    def __init__(self,mesg):
        mesg=self.mkbits(mesg)
        bs=Slicer9k(mesg)
        self.descriptors=[]
        self.info_section=Splice_Info_Section(bs)
        self.set_splice_command(bs) 
        self.descriptorloop(bs)
        self.info_section.crc=bs.ashex(32)

    def descriptorloop(self,bs):
        self.info_section.descriptor_loop_length = bs.asint(16) 
        tag_plus_header_size=2 # 1 byte for descriptor_tag, 1 byte for header?
        dll=self.info_section.descriptor_loop_length
        while dll> 0:
            try: 
                sd=self.set_splice_descriptor(bs)
                sdl=sd.descriptor_length
                self.descriptors.append(sd)
            except: sdl=0
            bit_move=sdl+ tag_plus_header_size
            dll -=(bit_move)

    def kvprint(self,obj):
        stuff=[]
        for k,v in vars(obj).items(): stuff.append(f'{k} :\033[92m{v} \033[0m')
        print(' '.join(stuff))
	
    def mkbits(self,s):
        if s[:2].lower()=='0x': s=s[2:]
        if s[:2].lower()=='fc': return bytes.fromhex(s)
        try: return base64.b64decode(s)
        except: return s

    def set_splice_command(self,bs):
        sct=self.info_section.splice_command_type
        if sct in command_map.keys(): self.command=command_map[sct](bs,sct)
   
    def set_splice_descriptor(self,bs):
        # splice_descriptor_tag 8 uimsbf
        tag= bs.asint(8)
        if tag in descriptor_map.keys(): return descriptor_map[tag](bs,tag)
                
    def show_info_section(self):
        print('\n Splice Info Section:')
        self.kvprint(self.info_section)

    def show_command(self):
        print('\n Splice Command:')
        self.kvprint(self.command)
		
    def show_descriptors(self):
        for d in self.descriptors:
            idx=self.descriptors.index(d)
            print(f'\n Splice Descriptor {idx}:')
            self.kvprint(d)
		
    def show(self):
        print('\n\n[SCTE 35 Message]')
        self.show_info_section()
        self.show_command()
        self.show_descriptors()
	


