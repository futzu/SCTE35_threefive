import base64
import bitstring
import threefive.tables as tables


def hex_decode(k):
    try: return bytearray.fromhex(hex(k)[2:]).decode()
    except: return k


def kv_print(obj):
    dotdot=' : '
    for k,v in vars(obj).items(): print(f'{k}{dotdot}{v}')
 

def mk_bits(s):
    try: return bitstring.BitString(bytes=base64.b64decode(s))
    except: return bitstring.BitStream(s)

	
def time_90k(k):
    t= k/90000.0    
    return f'{t :.6f}'


def reserved(bb,bst):
    bb.bitpos+=bst


class Splice:
    def __init__(self,mesg):
        bb=mk_bits(mesg)
        self.descriptors=[]
        self.info_section=Splice_Info_Section(bb) 
        self.set_splice_command(bb) 
        self.info_section.descriptor_loop_length = bb.read('uint:16') 
        tag_plus_header_size=2 # 1 byte for descriptor_tag, 1 byte for header?
        dll=self.info_section.descriptor_loop_length
        while dll> 0:
            bitstart=bb.bitpos
            sd=self.set_splice_descriptor(bb)
            try: sdl=sd.descriptor_length
            except: sdl=0
            bit_move=sdl+ tag_plus_header_size
            dll -=(bit_move)
            self.descriptors.append(sd)
            bb.bitpos=bitstart+(bit_move*8)
        self.info_section.crc=hex(bb.read('uint:32'))

    def set_splice_command(self,bb):
        cmd_types={0: Splice_Null,
		4: Splice_Schedule,
		5: Splice_Insert,
		6: Time_Signal,
		7: Bandwidth_Reservation,
		255: Private_Command}
        self.command=None
        sct=self.info_section.splice_command_type
        if sct in cmd_types.keys(): self.command=cmd_types[sct](bb,sct)

    def set_splice_descriptor(self,bb):
        dscr_types={0: Avail_Descriptor,
		1: Dtmf_Descriptor,
		2: Segmentation_Descriptor,
		3: Time_Descriptor,
		4: Audio_Descriptor}   
        # splice_descriptor_tag 8 uimsbf
        tag= bb.read('uint:8')
        if tag in dscr_types.keys(): return dscr_types[tag](bb,tag) 		

    def show_info_section(self):
        print('\n[ Splice Info Section ]')
        kv_print(self.info_section)

    def show_command(self):
        print('\n[ Splice Command ]')
        kv_print(self.command)
		
    def show_descriptors(self):
        for d in self.descriptors:
            idx=self.descriptors.index(d)
            print('\n[ Splice Descriptor ',idx,' ]')
            kv_print(d)
		
    def show(self):
        self.show_info_section()
        self.show_command()
        self.show_descriptors()
	
	
class Splice_Command: 
    def break_duration(self,bb):
        self.break_auto_return= bb.read('bool')
        reserved(bb,6)
        self.break_duration= time_90k(bb.read('uint:33'))

    def splice_time(self,bb): #40bits
        self.time_specified_flag=bb.read('bool')
        if self.time_specified_flag:
            reserved(bb,6)
            self.pts_time=time_90k(bb.read('uint:33'))
        else: reserved(bb,7)


class Splice_Null(Splice_Command):
    def __init__(self,bb,sct):
        self.splice_type=sct
        self.name='Splice Null'

             
class Splice_Schedule(Splice_Command):
    def __init__(self,bb,sct):
        self.splice_type=sct
        self.name='Splice Schedule'
        splice_count=bb.read('uint:8')
        for i in range(0,splice_count):            
            self.splice_event_id= bb.read('uint:32')
            self.splice_event_cancel_indicator= bb.read('bool')
            reserved(bb,7)
            if not self.splice_event_cancel_indicator:
                self.out_of_network_indicator=bb.read('bool')
                self.program_splice_flag=bb.read('bool')
                self.duration_flag=bb.read('bool')
                reserved(bb,5)
                if self.program_splice_flag:  
                    self.utc_splice_time=bb.read('uint:32')
                else:
                    self.component_count=bb.read('uint:8')
                    self.components=[]
                    for j in range(0,self.component_count):
                        self.components[j]={
                            'component_tag': bb.read('uint:8'),
                            'utc_splice_time':bb.read('uint:32')}
                if self.duration_flag: self.break_duration(bb)
                self.unique_program_id= bb.read('uint:16')
                self.avail_num= bb.read('uint:8')
                self.avails_expected=bb.read('uint:8')


class Splice_Insert(Splice_Command):
    def __init__(self,bb,sct):
        self.splice_type=sct 
        self.name='Splice Insert'
        self.splice_event_id=bb.read('uint:32')
        self.splice_event_cancel_indicator=bb.read('bool')
        reserved(bb,7)
        if not self.splice_event_cancel_indicator:    
            self.out_of_network_indicator=bb.read('bool')
            self.program_splice_flag=bb.read('bool')
            self.duration_flag=bb.read('bool')
            self.splice_immediate_flag=bb.read('bool')
            reserved(bb,4)
            if self.program_splice_flag and not self.splice_immediate_flag: 
                self.splice_time(bb)
            if not self.program_splice_flag:
                self.component_count=bb.read('uint:8')
                self.components=[]
                for i in range(0,self.component_count):  
                    self.components[i]=bb.read('uint:8')
                if not self.splice_immediate_flag: self.splice_time(bb)
            if self.duration_flag: self.break_duration(bb) 
            self.unique_program_id=bb.read('uint:16')
            self.avail_num=bb.read('uint:8')
            self.avail_expected=bb.read('uint:8')


class Time_Signal(Splice_Command):
    def __init__(self,bb,sct):
        self.splice_type=sct
        self.name='Time Signal'
        self.splice_time(bb)


class Bandwidth_Reservation(Splice_Command):
    def __init__(self,bb,sct):
        self.splice_type=sct
        self.name='Bandwidth Reservation'


class Private_Command(Splice_Command):
    def __init__(self,bb,sct):
        self.splice_type=sct
        self.name='Private Command'


class Splice_Descriptor:
    '''
    the first six bytes of all descriptors:
    
        splice_descriptor_tag    8 uimsbf 
        descriptor_length        8 uimsbf 
        identifier              32 uimsbf 
    '''
    def __init__(self,bb,tag):
        self.name='Unknown Descriptor'
        self.splice_descriptor_tag=tag
        self.descriptor_length = bb.read('uint:8')
        #identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
        self.identifier = hex_decode(bb.read('uint:32'))
        try: self.identifier == 'CUEI'
        except:
            print('descriptor identifier is ',self.identifier , 'should be CUEI')


class Avail_Descriptor(Splice_Descriptor):
    '''  
    Table 17 -  avail_descriptor()
    '''
    def __init__(self,bb,tag):
        super().__init__(bb,tag)
        self.name='Avail Descriptor'
        self.provider_avail_id=bb.read('uint:32')

	
class Dtmf_Descriptor(Splice_Descriptor):
    '''
    Table 18 -  DTMF_descriptor()
    ''' 
    def __init__(self,bb,tag):
        super().__init__(bb,tag)
        self.name='DTMF Descriptor'
        self.preroll= bb.read('uint:8')
        self.dtmf_count= bb.read('uint:3')
        reserved(bb,5)
        self.dtmf_chars=[]
        for i in range(0,self.dtmf_count): 
            self.dtmf_chars.append(bb.read('uint:8'))

	
class Segmentation_Descriptor(Splice_Descriptor):
    def __init__(self,bb,tag):
        super().__init__(bb,tag)
        self.name='Segmentation Descriptor'
        self.segmentation_event_id=hex(bb.read('uint:32'))
        self.segmentation_event_cancel_indicator=bb.read('bool')
        reserved(bb,7)
        if not self.segmentation_event_cancel_indicator:
            self.program_segmentation_flag=bb.read('bool')
            self.segmentation_duration_flag=bb.read('bool')
            self.delivery_not_restricted_flag=bb.read('bool')
            if not self.delivery_not_restricted_flag:
                self.web_delivery_allowed_flag=bb.read('bool')
                self.no_regional_blackout_flag=bb.read('bool')
                self.archive_allowed_flag=bb.read('bool')
                self.device_restrictions=hex(bb.read('uint:2'))
            else: reserved(bb,5)
            if not self.program_segmentation_flag:
                self.component_count= bb.read('uint:8')
                self.components=[]
                for i in range(0,self.component_count):
                    comp={}
                    comp['component_tag']=bb.read('uint:8')
                    reserved(bb,7)
                    comp['pts_offset']=time_90k(bb.read('uint:33'))
                    self.components.append(comp)
            if self.segmentation_duration_flag: 
                self.segmentation_duration=time_90k(bb.read('uint:40'))
            self.segmentation_upid_type=bb.read('uint:8')
            if self.segmentation_upid_type==8:
                self.segmentation_upid_length=bb.read('uint:8')
                self.turner_identifier=bb.read('bits:64')
            self.segmentation_type_id=bb.read('uint:8')
            if self.segmentation_type_id in tables.table22.keys():
                self.segmentation_message= tables.table22[self.segmentation_type_id][0]
            if  self.segmentation_type_id ==0:
                self.segment_num=0
                self.segments_expected=0
            else:                
                self.segment_num=bb.read('uint:8')
                self.segments_expected=bb.read('uint:8')
            if self.segmentation_type_id in [0x34, 0x36]:
                self.sub_segment_num=bb.read('uint:8')
                self.sub_segments_expected=bb.read('uint:8')


class Time_Descriptor(Splice_Descriptor):
    def __init__(self,bb,tag):
        super().__init__(bb,tag)
        self.name='Time Descriptor'
        self.TAI_seconds=bb.read('uint:48')
        self.TAI_ns=bb.read('uint:32')
        self.UTC_offset=bb.read('uint:16')

	
class Audio_Descriptor(Splice_Descriptor):
    def __init__(self,bb,tag):
        super().__init__(bb,tag)
        self.name='Audio Descriptor'
        self.components=[]
        self.audio_count= bb.read('uint:4') 
        reserved(bb,4) 
        for i in range(0,self.audio_count):
            comp={}
            comp['component_tag']=bb.read('uint:8')
            comp['ISO_code=']=bb.read('uint:24')
            comp['Bit_Stream_Mode']=bb.read('uint:3')
            comp['Num_Channels']=bb.read('uint:4')
            comp['Full_Srvc_Audio']=bb.read('bool')
            self.components.append(comp)


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

