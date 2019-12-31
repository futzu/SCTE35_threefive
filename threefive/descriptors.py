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
        self.descriptor_length = bs.asint(8)
        #identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
        self.identifier = hex_decode(bs.asint(32))
        return self.identifier ==  'CUEI'
        
class Avail_Descriptor(Splice_Descriptor):
    '''  
    Table 17 -  avail_descriptor()
    '''
    def __init__(self,bs,tag):
        if not super().__init__(bs,tag): return False
        self.name='Avail Descriptor'
        self.provider_avail_id=bs.asint(32)

	
class Dtmf_Descriptor(Splice_Descriptor):
    '''
    Table 18 -  DTMF_descriptor()
    ''' 
    def __init__(self,bs,tag):
        if not super().__init__(bs,tag): return False
        self.name='DTMF Descriptor'
        self.preroll= bs.asint(8)
        self.dtmf_count= bs.asint(3)
        reserved=bs.asint(5)
        self.dtmf_chars=[]
        for i in range(0,self.dtmf_count): 
            self.dtmf_chars.append(bs.asint(8))

	
class Segmentation_Descriptor(Splice_Descriptor):
    def __init__(self,bs,tag):
        if not super().__init__(bs,tag): return False
        self.name='Segmentation Descriptor'
        self.segmentation_event_id=bs.ashex(32)
        self.segmentation_event_cancel_indicator=bs.asflag(1)
        reserved=bs.asint(7)
        if not self.segmentation_event_cancel_indicator:
            self.program_segmentation_flag=bs.asflag(1)
            self.segmentation_duration_flag=bs.asflag(1)
            self.delivery_not_restricted_flag=bs.asflag(1)
            if not self.delivery_not_restricted_flag:
                self.web_delivery_allowed_flag=bs.asflag(1)
                self.no_regional_blackout_flag=bs.asflag(1)
                self.archive_allowed_flag=bs.asflag(1)
                self.device_restrictions=bs.ashex(2)
            else: reserved=bs.asint(5)
            if not self.program_segmentation_flag:
                self.component_count= bs.asint(8)
                self.components=[]
                for i in range(0,self.component_count):
                    comp={}
                    comp['component_tag']=bs.asint(8)
                    reserved(bs,7)
                    comp['pts_offset']=time_90k(bs.asint(33))
                    self.components.append(comp)
            if self.segmentation_duration_flag: 
                self.segmentation_duration=time_90k(bs.asint(40))
            self.segmentation_upid_type=bs.asint(8)
            if self.segmentation_upid_type==8:
                self.segmentation_upid_length=bs.asint(8)
                self.turner_identifier=bs.ashex(64)
            self.segmentation_type_id=bs.asint(8)
            if self.segmentation_type_id in table22.keys():
                self.segmentation_message= table22[self.segmentation_type_id][0]
            if  self.segmentation_type_id ==0:
                self.segment_num=0
                self.segments_expected=0
            else:                
                self.segment_num=bs.asint(8)
                self.segments_expected=bs.asint(8)
            if self.segmentation_type_id in [0x34, 0x36]:
                self.sub_segment_num=bs.asint(8)
                self.sub_segments_expected=bs.asint(8)


class Time_Descriptor(Splice_Descriptor):
    def __init__(self,bs,tag):
        if not super().__init__(bs,tag): return False
        self.name='Time Descriptor'
        self.TAI_seconds=bs.asint(48)
        self.TAI_ns=bs.asint(32)
        self.UTC_offset=bs.asint(16)

	
class Audio_Descriptor(Splice_Descriptor):
    def __init__(self,bs,tag):
        if not super().__init__(bs,tag): return False
        self.name='Audio Descriptor'
        self.components=[]
        self.audio_count= bs.asint(4) 
        reserved=bs.asint(4) 
        for i in range(0,self.audio_count):
            comp={}
            comp['component_tag']=bs.asint(8)
            comp['ISO_code=']=bs.asint(24)
            comp['Bit_Stream_Mode']=bs.asint(3)
            comp['Num_Channels']=bs.asint(4)
            comp['Full_Srvc_Audio']=bs.asflag(1)
            self.components.append(comp)


	
	
