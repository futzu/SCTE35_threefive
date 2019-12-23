from .util import *


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
        if self.identifier ==  'CUEI': return True
        return False

class Avail_Descriptor(Splice_Descriptor):
    '''  
    Table 17 -  avail_descriptor()
    '''
    def __init__(self,bb,tag):
        if not super().__init__(bb,tag): return False
        self.name='Avail Descriptor'
        self.provider_avail_id=bb.read('uint:32')

	
class Dtmf_Descriptor(Splice_Descriptor):
    '''
    Table 18 -  DTMF_descriptor()
    ''' 
    def __init__(self,bb,tag):
        if not super().__init__(bb,tag): return False
        self.name='DTMF Descriptor'
        self.preroll= bb.read('uint:8')
        self.dtmf_count= bb.read('uint:3')
        reserved(bb,5)
        self.dtmf_chars=[]
        for i in range(0,self.dtmf_count): 
            self.dtmf_chars.append(bb.read('uint:8'))

	
class Segmentation_Descriptor(Splice_Descriptor):
    def __init__(self,bb,tag):
        if not super().__init__(bb,tag): return False
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
        if not super().__init__(bb,tag): return False
        self.name='Time Descriptor'
        self.TAI_seconds=bb.read('uint:48')
        self.TAI_ns=bb.read('uint:32')
        self.UTC_offset=bb.read('uint:16')

	
class Audio_Descriptor(Splice_Descriptor):
    def __init__(self,bb,tag):
        if not super().__init__(bb,tag): return False
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

