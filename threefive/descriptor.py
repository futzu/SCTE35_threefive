class SpliceDescriptor:
    ''' 
    descriptor.SpliceDescriptor handles avail descriptors,
        dtmf descriptors, time descriptors and audio descriptors.
    segmentation.SegmentationDescriptor handles segmentation descriptors.
    '''
    def __repr__(self):
        return str(vars(self))
    
    def chk_identifier(self,bitbin):
        # identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
        self.identifier = bitbin.asdecodedhex(32)
        if self.identifier != "CUEI":
            raise ValueError(
                'All descriptors must have a identifier of "CUEI"')
        
    def parse(self,bitbin,tag):
        sd_map = { 0: self.avail_descriptor,
           1: self.dtmf_descriptor,
          # 2: SegmentationDescriptor see three5.segmentation 
           3: self.time_descriptor,
           4: self.audio_descriptor }
        self.tag = tag
        self.chk_identifier(bitbin)
        sd_map[tag](bitbin)

    def avail_descriptor(self,bitbin):
        """
        Table 17 -  avail_descriptor()
        """
        self.name = "Avail Descriptor"
        self.provider_avail_id = bitbin.asint(32)

    def dtmf_descriptor(self,bitbin):
        """
        Table 18 -  DTMF_descriptor()
        """
        self.name = "DTMF Descriptor"
        self.preroll = bitbin.asint(8)
        self.dtmf_count = bitbin.asint(3)
        bitbin.forward(5)
        self.dtmf_chars = []
        for i in range(0, self.dtmf_count):
            self.dtmf_chars.append(bitbin.asint(8))

    def time_descriptor(self,bitbin):
        """
        Table 25 - time_descriptor()
        """
        self.name = "Time Descriptor"
        self.TAI_seconds = bitbin.asint(48)
        self.TAI_ns = bitbin.asint(32)
        self.UTC_offset = bitbin.asint(16)

    def audio_descriptor(self,bitbin):
        """
        Table 26 - audio_descriptor()
        """
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
