import sys

class SpliceDescriptor:
    def __init__(self, bitbin, tag):
        self.tag = tag
        # identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
        self.identifier = bitbin.asdecodedhex(32)
        if self.identifier != "CUEI":
            print('Descriptors should have an identifier of "CUEI"', file=sys.stderr)
                

class AvailDescriptor(SpliceDescriptor):
    """
    Table 17 -  avail_descriptor()
    """
    def __init__(self, bitbin, tag):
        super().__init__(bitbin, tag)
        self.name = "Avail Descriptor"
        self.provider_avail_id = bitbin.asint(32)


class DtmfDescriptor(SpliceDescriptor):
    """
    Table 18 -  DTMF_descriptor()
    """
    def __init__(self, bitbin, tag):
        super().__init__(bitbin, tag)
        self.name = "DTMF Descriptor"
        self.preroll = bitbin.asint(8)
        self.dtmf_count = bitbin.asint(3)
        bitbin.forward(5)
        self.dtmf_chars = []
        for i in range(0, self.dtmf_count):
            self.dtmf_chars[i] =bitbin.asint(8)


class TimeDescriptor(SpliceDescriptor):
    """
    Table 25 - time_descriptor()
    """
    def __init__(self, bitbin, tag):
        super().__init__(bitbin, tag)
        self.name = "Time Descriptor"
        self.TAI_seconds = bitbin.asint(48)
        self.TAI_ns = bitbin.asint(32)
        self.UTC_offset = bitbin.asint(16)


class AudioDescriptor(SpliceDescriptor):
    """
    Table 26 - audio_descriptor()
    """
    def __init__(self, bitbin, tag):
        super().__init__(bitbin, tag)
        self.name = "Audio Descriptor"
        self.components = []
        self.audio_count = bitbin.asint(4)
        bitbin.forward(4)
        for i in range(0, self.audio_count):
            comp = {}
            comp["component_tag"] = bitbin.asint(8)
            comp["ISO_code="] = bitbin.asint(24)
            comp["bit_stream_mode"] = bitbin.asint(3)
            comp["num_channels"] = bitbin.asint(4)
            comp["full_srvc_audio"] = bitbin.asflag(1)
            self.components[i] = comp
