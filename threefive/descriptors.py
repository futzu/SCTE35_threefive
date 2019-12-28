from .util import *

from .tables import table22

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


	
	
