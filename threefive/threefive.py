
import base64,bitstring

def hexed(k):
    return hex(k)

def hex_decode(k):
    try:
        return bytearray.fromhex(hexed(k)[2:]).decode()
    except:
        return k

def kv_print(obj):
    try: 
        for k,v in vars(obj).items(): print(k,':',v)
    except: 
        print(obj)

def mk_bits(s):
    try: return bitstring.BitString(bytes=base64.b64decode(s))
    except:return bitstring.BitString(s)


def time_90k(k):
    t= k/90000.0    
    return f'{t :.6f}'
	
	
class Splice:
    def __init__(self,mesg):
        bb=mk_bits(mesg)
        self.descriptors=[]
        self.info_section=Splice_Info_Section(bb) 
        self.set_splice_command(bb) 
        self.info_section.descriptor_loop_length = bb.read('uint:16') 
        dll=self.info_section.descriptor_loop_length 
        while dll> 0:
            sd=Splice_Descriptor(bb)
            dll -=sd.descriptor_length+2
            self.descriptors.append(sd)
		
    def set_splice_command(self,bb):
        self.command=None
        sct=self.info_section.splice_command_type
        command_types = {0: Splice_Null,
                4: Splice_Schedule,
                5: Splice_Insert,
                6: Time_Signal,
                7: Bandwidth_Reservation,
                255: Private_Command}
        if sct in command_types.keys():  self.command=command_types[sct](bb,sct)

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
        reserved=bb.read('uint:6')
        self.break_duration= time_90k(bb.read('uint:33'))

    def splice_time(self,bb): #40bits
        self.time_specified_flag=bb.read('bool')
        if self.time_specified_flag:
            reserved=bb.read('bits:6')
            self.pts_time=time_90k(bb.read('uint:33'))
        else:
            reserved=bb.read('bits:7')


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
            reserved=bb.read('bits:7')
            if not self.splice_event_cancel_indicator:
                self.out_of_network_indicator=bb.read('bool')
                self.program_splice_flag=bb.read('bool')
                self.duration_flag=bb.read('bool')
                reserved=bb.read('uint:5')
                if self.program_splice_flag: 
                    self.utc_splice_time=bb.read('uint:32')
                if not self.program_splice_flag:
                    self.component_count=bb.read('uint:8')
                    self.components=[]
                    for j in range(0,self.component_count):
                        self.components[j]={
                            'component_tag': bb.read('uint:8'),
                            'utc_splice_time':bb.read('uint:32')}
                if self.duration_flag: 
                    self.break_duration(bb)
                self.unique_program_id= bb.read('uint:16')
                self.avail_num= bb.read('uint:8')
                self.avails_expected=bb.read('uint:8')


class Splice_Insert(Splice_Command):
    def __init__(self,bb,sct):
        self.splice_type=sct 
        self.name='Splice Insert'
        self.splice_event_id=bb.read('uint:32')
        self.splice_event_cancel_indicator=bb.read('bool')
        reserved= bb.read('bits:7')
        if not self.splice_event_cancel_indicator:    
            self.out_of_network_indicator=bb.read('bool')
            self.program_splice_flag=bb.read('bool')
            self.duration_flag=bb.read('bool')
            self.splice_immediate_flag=bb.read('bool')
            reserved= bb.read('bits:4')
            if self.program_splice_flag and not self.splice_immediate_flag: 
                self.splice_time(bb)
            if not self.program_splice_flag:
                self.component_count=bb.read('uint:8')
                self.components=[]
                for i in range(0,self.component_count): 
                    self.components[i]=bb.read('uint:8')
                if not self.splice_immediate_flag:
                    self.splice_time(bb)
            if self.duration_flag:
                self.break_duration(bb) 
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
    def __init__(self,bb):
        self.name='Unknown Descriptor'
        dscr_types={0: self.avail_descriptor,
        1: self.dtmf_descriptor,
        2: self.segmentation_descriptor,
        3: self.time_descriptor,
        4: self.audio_descriptor}   
        '''
		All splice descriptors 
		have the first six bytes in common
        '''
        # splice_descriptor_tag 8 uimsbf
        self.splice_descriptor_tag= bb.read('uint:8') 

        # descriptor_length 8 uimsbf
        self.descriptor_length = bb.read('uint:8')
        
        #identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
        self.identifier = hex_decode(bb.read('uint:32'))

        tag=self.splice_descriptor_tag
        if tag in dscr_types.keys(): dscr_types[tag](bb)

    def avail_descriptor(self,bb):
        self.name='Avail Descriptor'
        self.provider_avail_id=bb.read('uint:32')

    def dtmf_descriptor(self,bb):
        self.name='DTMF Descriptor'
        self.preroll= bb.read('uint:8')
        self.dtmf_count= bb.read('uint:3')
        reserved= bb.read('bits:5')
        self.dtmf_chars=[]
        for i in range(0,self.dtmf_count):
            self.dtmf_chars.append(bb.read('uint:8'))

    def  segmentation_descriptor(self,bb):
        self.name='Segmentation Descriptor'
        self.segmentation_event_id=hexed(bb.read('uint:32'))
        self.segmentation_event_cancel_indicator=bb.read('bool')
        reserved= bb.read('bits:7')
        if not self.segmentation_event_cancel_indicator:
            self.program_segmentation_flag=bb.read('bool')
            self.segmentation_duration_flag=bb.read('bool')
            self.delivery_not_restricted_flag=bb.read('bool')
            if not self.delivery_not_restricted_flag:
                self.web_delivery_allowed_flag=bb.read('bool')
                self.no_regional_blackout_flag=bb.read('bool')
                self.archive_allowed_flag=bb.read('bool')
                self.device_restrictions=hexed(bb.read('uint:2'))
            else: 
                reserved= bb.read('bits:5')	

            if not self.program_segmentation_flag:
                self.component_count= bb.read('uint:8')
                self.components=[]
                for i in range(0,self.component_count):
                    comp={}
                    comp['component_tag']=bb.read('uint:8')
                    reserved= bb.read('bits:7')
                    comp['pts_offset']=time_90k(bb.read('uint:33'))
                    self.components.append(comp)
            if self.segmentation_duration_flag:
                self.segmentation_duration=time_90k(bb.read('uint:40'))
            self.segmentation_upid_type=bb.read('uint:8')
            self.segmentation_upid_length=bb.read('uint:8')
            self.turner_identifier=bb.read('bits:64')
            self.segmentation_type_id=bb.read('uint:8')
            self.segment_num=bb.read('uint:8')
            self.segments_expected=bb.read('uint:8')
            if self.segmentation_type_id in [0x34, 0x36]:
                self.sub_segment_num=bb.read('uint:8')
                self.sub_segments_expected=bb.read('uint:8')
           

    def time_descriptor(self,bb):
        self.name='Time Descriptor'
        self.TAI_seconds=bb.read('uint:48')
        self.TAI_ns=bb.read('uint:32')
        self.UTC_offset=bb.read('uint:16')

    def audio_descriptor(self,bb):
        self.name='Audio Descriptor'
        self.components=[]
        self.audio_count= bb.read('uint:4') 
        reserved=bb.read('uint:4') 
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
        self.table_id =bb.read('uint:8')
        self.section_syntax_indicator = bb.read('bool')
        self.private = bb.read('bool')
        self.reserved= bb.read('uint:2')
        self.section_length = bb.read('uint:12')
        self.protocol_version = bb.read('uint:8')
        self.encrypted_packet =  bb.read('bool')
        self.encryption_algorithm =bb.read('uint:6')
        self.pts_adjustment = time_90k(bb.read('uint:33'))
        self.cw_index = bb.read('uint:8')
        self.tier = bb.read('uint:12')
        self.splice_command_length = bb.read('uint:12')
        self.splice_command_type = bb.read('uint:8')

