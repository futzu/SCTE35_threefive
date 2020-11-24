import sys
from .tools import to_stderr


class SpliceDescriptor:
    """
    SpliceDescriptor is the
    base class for all splice descriptors.
    It should not be used directly
    """

    def __init__(self, tag):
        self.tag = tag
        # identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
        self.identifier = None

    def decode(self, bitbin):
        """
        SpliceDescriptor subclasses
        must implement a decode method.
        """

    def encode(self):
        """
        SpliceDescriptor subclasses
        will soon implement a encode method.
        """

    def parse_id(self, bitbin):
        """
        parse splice descriptor identifier
        """
        self.identifier = bitbin.asdecodedhex(32)
        if self.identifier != "CUEI":
            to_stderr('Descriptors should have an identifier of "CUEI"')


class AvailDescriptor(SpliceDescriptor):
    """
    Table 17 -  avail_descriptor()
    """

    def __init__(self, tag):
        super().__init__(tag)
        self.name = "Avail Descriptor"
        self.provider_avail_id = None

    def decode(self, bitbin):
        self.parse_id(bitbin)
        self.provider_avail_id = bitbin.asint(32)


class DtmfDescriptor(SpliceDescriptor):
    """
    Table 18 -  DTMF_descriptor()
    """

    def __init__(self, tag):
        super().__init__(tag)
        self.name = "DTMF Descriptor"
        self.preroll = None
        self.dtmf_count = None
        self.dtmf_chars = []

    def decode(self, bitbin):
        self.parse_id(bitbin)
        self.preroll = bitbin.asint(8)
        self.dtmf_count = bitbin.asint(3)
        bitbin.forward(5)
        for i in range(0, self.dtmf_count):
            self.dtmf_chars[i] = bitbin.asint(8)


class TimeDescriptor(SpliceDescriptor):
    """
    Table 25 - time_descriptor()
    """

    def __init__(self, tag):
        super().__init__(tag)
        self.name = "Time Descriptor"
        self.tai_seconds = None
        self.tai_ns = None
        self.utc_offset = None

    def decode(self, bitbin):
        self.parse_id(bitbin)
        self.tai_seconds = bitbin.asint(48)
        self.tai_ns = bitbin.asint(32)
        self.utc_offset = bitbin.asint(16)


class AudioDescriptor(SpliceDescriptor):
    """
    Table 26 - audio_descriptor()
    """

    def __init__(self, tag):
        super().__init__(tag)
        self.name = "Audio Descriptor"
        self.components = []
        self.audio_count = None

    def decode(self, bitbin):
        self.parse_id(bitbin)
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
