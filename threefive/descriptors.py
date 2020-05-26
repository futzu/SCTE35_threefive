class Splice_Descriptor:
    def __init__(self,bitbin,tag):
        self.tag = tag
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
        if not super().__init__(bitbin, tag):
            return False
        self.name = "Avail Descriptor"
        self.provider_avail_id = bitbin.asint(32)


class Dtmf_Descriptor(Splice_Descriptor):
    """
    Table 18 -  DTMF_descriptor()
    """
    def __init__(self, bitbin, tag):
        if not super().__init__(bitbin, tag):
            return False
        self.name = "DTMF Descriptor"
        self.preroll = bitbin.asint(8)
        self.dtmf_count = bitbin.asint(3)
        bitbin.forward(5)
        self.dtmf_chars = []
        for i in range(0, self.dtmf_count):
            self.dtmf_chars.append(bitbin.asint(8))

     
class Time_Descriptor(Splice_Descriptor):
    """
    Table 25 - time_descriptor()
    """
    def __init__(self, bitbin, tag):
        if not super().__init__(bitbin, tag):
            return False
        self.name = "Time Descriptor"
        self.TAI_seconds = bitbin.asint(48)
        self.TAI_ns = bitbin.asint(32)
        self.UTC_offset = bitbin.asint(16)


class Audio_Descriptor(Splice_Descriptor):
    """
    Table 26 - audio_descriptor()
    """
    def __init__(self, bitbin, tag):
        if not super().__init__(bitbin, tag):
            return False
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
