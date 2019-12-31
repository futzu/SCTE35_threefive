'''
three5.py is all of threefive in one file
in case you hate pip or something.

usage:

Python 3.7.4 (default, Jul 16 2019, 07:12:58) 
[GCC 9.1.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import three5
>>> three5.decode('/home/fat.ts')

'''
import base64

PACKET_SIZE=188
SYNC_BYTE=b'\x47'


def decode(stuff):
    '''
    All purpose SCTE 35 decoder function
    the  stuff arg can be     
         mpegts file, 
         binary file,
         base64 encoded string,
         binary encoded string, 
         hex encoded string.
     
    usage:

    # for a mpegts video 

    import three5
    three5.decode('/path/to/mpegts')
    
    # for a base64 encoded string

    import three5
    Bee64='/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g='
    three5.decode(Bee64)

    '''
    scte35=None
    try: 
        scte35=Splice(stuff)
        scte35.show()
    except: 
        try:  scte35=Stream(stuff,show_null=False)
        except: pass
    return scte35
    


class Stream:

    def __init__(self,tsfile=None,show_null=True):
        self.splices=[]
        self.PID=False
        self.show_null=show_null
        self.parse_tsfile(tsfile)

    def parse_tsfile(self,tsfile):
        with open(tsfile,'rb') as tsdata:
            while tsdata:
                if tsdata.read(1)==SYNC_BYTE: 
                    packet =tsdata.read(PACKET_SIZE - 1)
                    if packet: self.parse_tspacket(packet)
                    else: break
                else: return 

    def parse_tspacket(self,packet):
        if packet[4] !=0xfc :return
        two_bytes=packet[:2]
        one_byte=packet[2]
        pid=bitslice(two_bytes,12,13)
        if self.PID and (pid !=self.PID): return
        cue=packet[4:]
        try:tf=Splice(cue)
        except: return 
        if not self.PID: 
            self.PID=pid
            print(f'\n\n[  SCTE 35 Stream found with Pid {hex(self.PID)}  ]')
        if not self.show_null and (cue[13]==0) : return
        tei=bitslice(two_bytes,15,1)
        pusi=bitslice(two_bytes,14,1)
        ts_priority=bitslice(two_bytes,13,1)
        scramble=bitslice(one_byte,7,2)
        afc=bitslice(one_byte,5,2)
        count=bitslice(one_byte,3,4)
        tf.show()
        self.splices.append(tf)
        return


class Splice:
    def __init__(self,mesg):
        mesg=mk_bits(mesg)
        bs=BitSlicer(mesg)
        self.descriptors=[]
        self.info_section=Splice_Info_Section(bs)
        self.set_splice_command(bs) 
        self.info_section.descriptor_loop_length = bs.slice(16) 
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
        self.info_section.crc=hex(bs.slice(32))

    def set_splice_command(self,bs):
        cmd_types={ 0: Splice_Null,
		4: Splice_Schedule,
		5: Splice_Insert,
		6: Time_Signal,
		7: Bandwidth_Reservation,
		255: Private_Command}
        self.command=False
        sct=self.info_section.splice_command_type
        if sct in cmd_types.keys(): self.command=cmd_types[sct](bs,sct)
   
    def set_splice_descriptor(self,bs):
        dscr_types={0: Avail_Descriptor,
		1: Dtmf_Descriptor,
		2: Segmentation_Descriptor,
		3: Time_Descriptor,
		4: Audio_Descriptor}   
        # splice_descriptor_tag 8 uimsbf
        tag= bs.slice(8)
        if tag in dscr_types.keys(): return dscr_types[tag](bs,tag)
                
    def show_info_section(self):
        print('\n Splice Info Section:')
        kv_print(self.info_section)

    def show_command(self):
        print('\n Splice Command:')
        kv_print(self.command)
		
    def show_descriptors(self):
        for d in self.descriptors:
            idx=self.descriptors.index(d)
            print(f'\n Splice Descriptor {idx}:')
            kv_print(d)
		
    def show(self):
        print('\n\n[SCTE 35 Message]')
        self.show_info_section()
        self.show_command()
        self.show_descriptors()
	

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
    


class Splice_Command: 
    def break_duration(self,bs):
        self.break_auto_return= bs.boolean(1)
        reserved=bs.slice(6)
        self.break_duration= time_90k(bs.slice(33))

    def splice_time(self,bs): #40bits
        self.time_specified_flag=bs.boolean(1)
        if self.time_specified_flag:
            reserved=bs.slice(6)
            self.pts_time=time_90k(bs.slice(33))
        else: reserved=bs.slice(7)


class Splice_Null(Splice_Command):
    def __init__(self,bs,sct):
        self.splice_type=sct
        self.name='Splice Null'

             
class Splice_Schedule(Splice_Command):
    def __init__(self,bs,sct):
        self.splice_type=sct
        self.name='Splice Schedule'
        splice_count=bs.slice(8)
        for i in range(0,splice_count):            
            self.splice_event_id= bs.slice(32)
            self.splice_event_cancel_indicator= bs.boolean(1)
            reserved=bs.slice(7)
            if not self.splice_event_cancel_indicator:
                self.out_of_network_indicator=bs.boolean(1)
                self.program_splice_flag=bs.boolean(1)
                self.duration_flag=bs.boolean(1)
                reserved=bs.slice(5)
                if self.program_splice_flag:  
                    self.utc_splice_time=bs.slice(32)
                else:
                    self.component_count=bs.slice(8)
                    self.components=[]
                    for j in range(0,self.component_count):
                        self.components[j]={
                            'component_tag': bs.slice(8),
                            'utc_splice_time':bs.slice(32)}
                if self.duration_flag: self.break_duration(bs)
                self.unique_program_id= bs.slice(16)
                self.avail_num= bs.slice(8)
                self.avails_expected=bs.slice(8)


class Splice_Insert(Splice_Command):
    def __init__(self,bs,sct):
        self.splice_type=sct 
        self.name='Splice Insert'
        self.splice_event_id=bs.slice(32)
        self.splice_event_cancel_indicator=bs.boolean(1)
        reserved=bs.slice(7)
        if not self.splice_event_cancel_indicator:    
            self.out_of_network_indicator=bs.boolean(1)
            self.program_splice_flag=bs.boolean(1)
            self.duration_flag=bs.boolean(1)
            self.splice_immediate_flag=bs.boolean(1)
            reserved=bs.slice(4)
            if self.program_splice_flag and not self.splice_immediate_flag: 
                self.splice_time(bs)
            if not self.program_splice_flag:
                self.component_count=bs.slice(8)
                self.components=[]
                for i in range(0,self.component_count):  
                    self.components[i]=bs.slice(8)
                if not self.splice_immediate_flag: self.splice_time(bs)
            if self.duration_flag: self.break_duration(bs) 
            self.unique_program_id=bs.slice(16)
            self.avail_num=bs.slice(8)
            self.avail_expected=bs.slice(8)


class Time_Signal(Splice_Command):
    def __init__(self,bs,sct):
        self.splice_type=sct
        self.name='Time Signal'
        self.splice_time(bs)


class Bandwidth_Reservation(Splice_Command):
    def __init__(self,bs,sct):
        self.splice_type=sct
        self.name='Bandwidth Reservation'


class Private_Command(Splice_Command):
    def __init__(self,bs,sct):
        self.splice_type=sct
        self.name='Private Command'



class Splice_Descriptor:
    '''
    the first six bytes of all descriptors:
    
        splice_descriptor_tag    8 uimsbf 
        descriptor_length        8 uimsbf 
        identifier              32 uimsbf 
    '''
    def __init__(self,bs,tag):
        self.name='Unknown Descriptor'
        self.splice_descriptor_tag=tag
        self.descriptor_length = bs.slice(8)
        #identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
        self.identifier = hex_decode(bs.slice(32))
        return self.identifier ==  'CUEI'
        
class Avail_Descriptor(Splice_Descriptor):
    '''  
    Table 17 -  avail_descriptor()
    '''
    def __init__(self,bs,tag):
        if not super().__init__(bs,tag): return False
        self.name='Avail Descriptor'
        self.provider_avail_id=bs.slice(32)

	
class Dtmf_Descriptor(Splice_Descriptor):
    '''
    Table 18 -  DTMF_descriptor()
    ''' 
    def __init__(self,bs,tag):
        if not super().__init__(bs,tag): return False
        self.name='DTMF Descriptor'
        self.preroll= bs.slice(8)
        self.dtmf_count= bs.slice(3)
        reserved=bs.slice(5)
        self.dtmf_chars=[]
        for i in range(0,self.dtmf_count): 
            self.dtmf_chars.append(bs.slice(8))

	
class Segmentation_Descriptor(Splice_Descriptor):
    def __init__(self,bs,tag):
        if not super().__init__(bs,tag): return False
        self.name='Segmentation Descriptor'
        self.segmentation_event_id=bs.hexed(32)
        self.segmentation_event_cancel_indicator=bs.boolean(1)
        reserved=bs.slice(7)
        if not self.segmentation_event_cancel_indicator:
            self.program_segmentation_flag=bs.boolean(1)
            self.segmentation_duration_flag=bs.boolean(1)
            self.delivery_not_restricted_flag=bs.boolean(1)
            if not self.delivery_not_restricted_flag:
                self.web_delivery_allowed_flag=bs.boolean(1)
                self.no_regional_blackout_flag=bs.boolean(1)
                self.archive_allowed_flag=bs.boolean(1)
                self.device_restrictions=bs.hexed(2)
            else: reserved=bs.slice(5)
            if not self.program_segmentation_flag:
                self.component_count= bs.slice(8)
                self.components=[]
                for i in range(0,self.component_count):
                    comp={}
                    comp['component_tag']=bs.slice(8)
                    reserved(bs,7)
                    comp['pts_offset']=time_90k(bs.slice(33))
                    self.components.append(comp)
            if self.segmentation_duration_flag: 
                self.segmentation_duration=time_90k(bs.slice(40))
            self.segmentation_upid_type=bs.slice(8)
            if self.segmentation_upid_type==8:
                self.segmentation_upid_length=bs.slice(8)
                self.turner_identifier=bs.hexed(64)
            self.segmentation_type_id=bs.slice(8)
            if self.segmentation_type_id in table22.keys():
                self.segmentation_message= table22[self.segmentation_type_id][0]
            if  self.segmentation_type_id ==0:
                self.segment_num=0
                self.segments_expected=0
            else:                
                self.segment_num=bs.slice(8)
                self.segments_expected=bs.slice(8)
            if self.segmentation_type_id in [0x34, 0x36]:
                self.sub_segment_num=bs.slice(8)
                self.sub_segments_expected=bs.slice(8)


class Time_Descriptor(Splice_Descriptor):
    def __init__(self,bs,tag):
        if not super().__init__(bs,tag): return False
        self.name='Time Descriptor'
        self.TAI_seconds=bs.slice(48)
        self.TAI_ns=bs.slice(32)
        self.UTC_offset=bs.slice(16)

	
class Audio_Descriptor(Splice_Descriptor):
    def __init__(self,bs,tag):
        if not super().__init__(bs,tag): return False
        self.name='Audio Descriptor'
        self.components=[]
        self.audio_count= bs.slice(4) 
        reserved=bs.slice(4) 
        for i in range(0,self.audio_count):
            comp={}
            comp['component_tag']=bs.slice(8)
            comp['ISO_code=']=bs.slice(24)
            comp['Bit_Stream_Mode']=bs.slice(3)
            comp['Num_Channels']=bs.slice(4)
            comp['Full_Srvc_Audio']=bs.boolean(1)
            self.components.append(comp)



class BitSlicer:
    def __init__(self,bites):
        '''
        From bytes to bits
        '''
        if not isinstance(bites,bytes):
            raise TypeError('bites needs to be type bytes')
        self.bit_idx=(len(bites)*8)
        self.bits=int.from_bytes(bites,byteorder='big')
           
    def slice(self,num_bits):
        '''
        Starting at self.bit_idx of self.bits, slice off num_bits of bits.
        ''' 
        bitslice= (self.bits >> (self.bit_idx-num_bits)) & ~(~0 << num_bits)
        self.bit_idx -=num_bits
        return bitslice
        
    def hexed(self,num_bits):
        '''
        return the hex value of a bitslice
        '''
        return hex(self.slice(num_bits))
        
    def boolean(self,num_bits=1):
        '''
        returns one bit as True or False
        '''
        return  self.slice(num_bits) ==1



def bitslice(data,bit_idx,num_bits):
    if type(data) == bytes: data=int.from_bytes(data,byteorder='big')
    return (data >> (bit_idx+1-num_bits)) & ~(~0 << num_bits)


def hex_decode(k):
    try: return bytearray.fromhex(hex(k)[2:]).decode()
    except: return k

def kv_print(obj):
    print(f'\t{vars(obj)}')
 
def mk_bits(s):
    if s[:2].lower()=='0x': s=s[2:]
    if s[:2].lower()=='fc': return bytes.fromhex(s)
    try: return base64.b64decode(s)
    except: return s

def time_90k(k):
    t= k/90000.0    
    return f'{t :.6f}'


def not_zero(i):
    return i !=0

def gte_zero(i):
    return i >=0

def MPU():
    pass

def MID():
    pass
	
'''
Table 20 from page 58 of
https://www.scte.org/SCTEDocs/Standards/ANSI_SCTE%2035%202019r1.pdf

Restrict Group 0 – This segment is restricted for a class of devices 
defined by an out of band message that describes which devices are excluded.

Restrict Group 1 – This segment is restricted for a class of devices 
defined by an out of band message that describes which devices are excluded.  

Restrict Group 2 – This segment is restricted for a class of devices 
defined by an out of band message that describes which devices are excluded. 
'''
table20={
0x00: 'Restrict Group 0',
0x01: 'Restrict Group 1',
0x02: 'Restrict Group 2',
0x03: 'No Restrictions'}

	
table21={
0x00: [	0,None],
0x01: [	gte_zero,'User Defined'],
0x02: [	8,'ISCI'],
0x03: [	12,	'Ad-ID'],
0x04: [	32,	'UMID'],
0x05: [	8, 'ISAN'],
0x06: [	12,'ISAN'],
0x07: [	12,'TID'],
0x08: [	8,'AiringID'],
0x09: [	gte_zero,'ADI'],	
0x0A: [	12,	'EIDR'],
0x0B: [	gte_zero,'ATSC'],
0x0C: [	gte_zero,MPU],
0x0D: [	gte_zero,MID],
0x0E: [	gte_zero,'ADS Info'],
0x0F: [	gte_zero,'URI'],
0x10-0xff: [gte_zero,'Reserved']}


'''
table 22 from page 62 of 
https://www.scte.org/SCTEDocs/Standards/ANSI_SCTE%2035%202019r1.pdf
I am using the segmentation_type_id as a key.

Segmentation_type_id = [segmentation_message,
			segment_num,
			segments_expected,
			sub_segment_num,
			sub_segments_expected]
'''
table22={
0x00  : [ "Not Indicated",0,0, None,None],
0x01  : [ "Content Identification",0,0, None,None],
0x10  : [ "Program Start",1,1, None,None],
0x11  : [ "Program End",1,1, None,None],
0x12 : [ "Program Early Termination",1,1, None,None],
0x13 : [ "Program Breakaway",1,1, None,None],
0x14 : [ "Program Resumption",1,1, None,None],
0x15  : [ "Program Runover Planned",1,1, None,None],
0x16  : [ "Program RunoverUnplanned",1,1, None,None],
0x17 : [ "Program Overlap Start",1,1, None,None],
0x18  : [ "Program Blackout Override",0,0, None,None],
0x19 : [ "Program Start – In Progress",1,1, None,None],
0x20 : [ "Chapter Start",not_zero,not_zero, None,None],
0x21 : [ "Chapter End",not_zero,not_zero, None,None],
0x22 : [ "Break Start",gte_zero,gte_zero, None,None],
0x23 : [ "Break End",gte_zero,gte_zero, None,None],
0x24 : [ "Opening Credit Start",1,1, None,None],
0x25 : [ "Opening Credit End",1,1, None,None],
0x26 : [ "Closing Credit Start",1,1, None,None],
0x27 : [ "Closing Credit End",1,1, None,None],
0x30 : [ "Provider Advertisement Start",gte_zero,gte_zero, None,None],
0x31 : [ "Provider Advertisement End",gte_zero,gte_zero, None,None],
0x32 : [ "Distributor Advertisement Start",gte_zero,gte_zero, None,None],
0x33 : [ "Distributor Advertisement End",gte_zero,gte_zero, None,None],
0x34 : [ "Provider Placement Opportunity Start",gte_zero,gte_zero,gte_zero,gte_zero],
0x35 : [ "Provider Placement Opportunity End",gte_zero,gte_zero, None,None],
0x36 : [ "Distributor Placement Opportunity Start",gte_zero,gte_zero,gte_zero,gte_zero],
0x37 : [ "Distributor Placement Opportunity End",gte_zero,gte_zero, None,None],
0x38 : [ "Provider Overlay Placement Opportunity Start",gte_zero,gte_zero,gte_zero,gte_zero],
0x39 : [ "Provider Overlay Placement Opportunity End",gte_zero,gte_zero, None,None],
0x3A : [ "Distributor Overlay Placement Opportunity Start",gte_zero,gte_zero,gte_zero,gte_zero],
0x3B : [ "Distributor Overlay Placement Opportunity End",gte_zero,gte_zero, None,None],
0x40  : [ "Unscheduled Event Start",0,0, None,None],
0x41  : [ "Unscheduled Event End",0,0, None,None],
0x50  : [ "Network Start",0,0, None,None],
0x51  : [ "Network End",0,0, None,None],
0x3B : [ "Distributor Overlay Placement Opportunity End",gte_zero,gte_zero, None,None],
0x40  : [ "Unscheduled Event Start",0,0, None,None],
0x41  : [ "Unscheduled Event End",0,0, None,None],
0x50  : [ "Network Start",0,0, None,None],
0x51  : [ "Network End",0,0, None,None]}




	
	

	
