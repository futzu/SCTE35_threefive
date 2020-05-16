from .tables import table20, table21, table22


class Splice_Descriptor:
    def __init__(self,bitbin,tag):
        self.tag =tag
        # identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
        self.identifier = bitbin.asdecodedhex(32)
        if self.identifier != "CUEI":
            raise ValueError(
                'All descriptors must have a identifier of "CUEI"')
        else:
            return self.identifier


class Avail_Descriptor(Splice_Descriptor):
    """
    Table 17 -  avail_descriptor()
    """
    def __init__(self, bitbin, tag):
        if not super().__init__(bitbin, tag): return False
        self.name = "Avail Descriptor"
        self.provider_avail_id = bitbin.asint(32)


class Dtmf_Descriptor(Splice_Descriptor):
    """
    Table 18 -  DTMF_descriptor()
    """
    def __init__(self, bitbin, tag):
        if not super().__init__(bitbin, tag): return False
        self.name = "DTMF Descriptor"
        self.preroll = bitbin.asint(8)
        self.dtmf_count = bitbin.asint(3)
        bitbin.forward(5)
        self.dtmf_chars = []
        for i in range(0, self.dtmf_count):
            self.dtmf_chars.append(bitbin.asint(8))

            
class Segmentation_Descriptor(Splice_Descriptor):
    """
    Table 19 - segmentation_descriptor()
    """
  
    
    def __init__(self, bitbin, tag):
        if not super().__init__(bitbin, tag): return False
        self.bitbin = bitbin
        self.name = "Segmentation Descriptor"
        self.segmentation_event_id = self.bitbin.ashex(32)
        self.segmentation_event_cancel_indicator = self.bitbin.asflag(1)
        self.bitbin.forward(7)
        if not self.segmentation_event_cancel_indicator:
            self.set_flags()
            if not self.program_segmentation_flag:
                self.component_count = self.bitbin.asint(8)
                self.components = []
                for i in range(0, self.component_count):
                    comp = {}
                    comp["component_tag"] = self.bitbin.asint(8)
                    self.bitbin.forward(7)
                    comp["pts_offset"] = self.bitbin.as90k(33)
                    self.components.append(comp)
            self.set_segmentation()  
      
    def set_flags(self):
        self.program_segmentation_flag = self.bitbin.asflag(1)
        self.segmentation_duration_flag = self.bitbin.asflag(1)
        self.delivery_not_restricted_flag = self.bitbin.asflag(1)
        if not self.delivery_not_restricted_flag:
            self.web_delivery_allowed_flag = self.bitbin.asflag(1)
            self.no_regional_blackout_flag = self.bitbin.asflag(1)
            self.archive_allowed_flag = self.bitbin.asflag(1)
            self.device_restrictions = table20[self.bitbin.asint(2)]
        else:
            self.bitbin.forward(5)

    def set_segmentation(self):
        if self.segmentation_duration_flag:
            self.segmentation_duration = self.bitbin.as90k(40)
        self.segmentation_upid_type = self.bitbin.asint(8)
        self.segmentation_upid_length = self.bitbin.asint(8)
        self.set_segmentation_upid()
        self.segmentation_type_id = self.bitbin.asint(8)

        if self.segmentation_type_id in table22.keys():
            self.segmentation_message = table22[self.segmentation_type_id][0]
            self.set_segments()
        self.bitbin = None   
            
    def set_segmentation_upid(self):
        print(self.segmentation_upid_type)
        '''
        These segmentation upid types
        do not yet have formatted output.
        0x05: ISAN,
        0x06: ISAN",
        0x07: TID",
        0x09: ADI",
        0x0b: ATSC",
        0x0d: MID",
        0x0e: ADS Info
        '''
        
        upid_map={
            0x02: self.AdID,
            0x03: self.AdID,
            0x04: self.UMID,
            0x08: self.airID,
            0x0a: self.EIDR,
            0x0c: self.MPU,
            0x0d: self.MID,
            0x0f: self.URI

            }
        upid_id=""
        if self.segmentation_upid_type in upid_map.keys():
            upid_id= upid_map[self.segmentation_upid_type]()
        else:
            upid_id =self.bitbin.asint(self.segmentation_upid_length*8)
        self.segmentation_upid =f'{table21[self.segmentation_upid_type][1]}:{upid_id}'

    def set_segments(self): 
        print(vars(self))
        print (self.bitbin.idx)
        self.segment_num = self.bitbin.asint(8)
        self.segments_expected = self.bitbin.asint(8)
        if self.segmentation_type_id in [0x34, 0x36, 0x38, 0x3a]:
            '''
            if there are 16 more bits in self.bitbin, read them.
            '''
            if self.bitbin.idx >= 16:
                self.sub_segment_num = self.bitbin.asint(8)
                self.sub_segments_expected = self.bitbin.asint(8)


    def AdID(self):
        return self.URI()
    
    def airID(self):
        return self.bitbin.ashex(self.segmentation_upid_length*8)
    
    def UMID(self):
        n=8
        pre = ''.join(self.airID().split('x',1))
        return '.'.join([pre[i:i+n] for i in range(0, len(pre), n)])
        
    def MID(self):
        return 'Not Yet Implemented'
        
    def MPU(self):
        bitcount= (self.segmentation_upid_length*8)
        format_identifier = self.bitbin.asint(32)
        private_data = self.bitbin.asint(bitcount -32)
        return {'format identifier':format_identifier,
                'private data':private_data}

    def EIDR(self):
        pre= self.bitbin.asint(16)
        post =self.bitbin.ashex(80)
        return f'10.{pre}/{post[2:6]}-{post[6:10]}-{post[10:14]}-{post[14:18]}-T'        

    def URI(self):
        return self.bitbin.asdecodedhex(self.segmentation_upid_length*8)


class Time_Descriptor(Splice_Descriptor):
    """
    Table 25 - time_descriptor()
    """
    def __init__(self, bitbin, tag):
        if not super().__init__(bitbin, tag): return False
        self.name = "Time Descriptor"
        self.TAI_seconds = bitbin.asint(48)
        self.TAI_ns = bitbin.asint(32)
        self.UTC_offset = bitbin.asint(16)


class Audio_Descriptor(Splice_Descriptor):
    """
    Table 26 - audio_descriptor()
    """
    def __init__(self, bitbin, tag):
        if not super().__init__(bitbin, tag): return False
        self.name = "Audio Descriptor"
        self.components = []
        self.audio_count = bitbin.asint(4)
        reserved = bitbin.asint(4)
        for i in range(0, self.audio_count):
            comp = {}
            comp["component_tag"] = bitbin.asint(8)
            comp["ISO_code="] = bitbin.asint(24)
            comp["bit_stream_mode"] = bitbin.asint(3)
            comp["num_channels"] = bitbin.asint(4)
            comp["full_srvc_audio"] = bitbin.asflag(1)
            self.components.append(comp)
