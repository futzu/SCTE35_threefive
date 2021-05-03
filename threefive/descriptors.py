"""
SCTE35 Splice Descriptors
"""
from .bitn import BitBin
from .base import SCTE35Base
from .segmentation import table20, table22
from .upid import upid_decoder


def k_by_v(adict, avalue):
    """
    dict key lookup by value
    """
    for kay, vee in adict.items():
        if vee == avalue:
            return kay


class SpliceDescriptor(SCTE35Base):
    """
    SpliceDescriptor is the
    base class for all splice descriptors.
    It should not be used directly
    """

    def __init__(self, bites=None):
        self.tag = -1
        self.descriptor_length = 0
        self.identifier = None
        self.bites = bites
        if bites:
            self.tag = bites[0]
            self.descriptor_length = bites[1]
            self.bites = bites[2:]

    def _parse_id(self, bitbin):
        """
        parse splice descriptor identifier
        """
        self.identifier = bitbin.as_ascii(32)
        # identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
        if self.identifier != "CUEI":
            raise Exception('Descriptors should have an identifier of "CUEI"')


class AvailDescriptor(SpliceDescriptor):
    """
    Table 17 -  avail_descriptor()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.tag = 0
        self.name = "Avail Descriptor"
        self.provider_avail_id = None

    def decode(self):
        """
        decode SCTE35 Avail Descriptor
        """
        bitbin = BitBin(self.bites)
        self._parse_id(bitbin)
        self.provider_avail_id = bitbin.as_int(32)


class DtmfDescriptor(SpliceDescriptor):
    """
    Table 18 -  DTMF_descriptor()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.tag = 1
        self.name = "DTMF Descriptor"
        self.preroll = None
        self.dtmf_count = None
        self.dtmf_chars = []

    def decode(self):
        """
        decode SCTE35 Dtmf Descriptor
        """
        bitbin = BitBin(self.bites)
        self._parse_id(bitbin)
        self.preroll = bitbin.as_int(8)
        self.dtmf_count = d_c = bitbin.as_int(3)
        bitbin.forward(5)
        while d_c:
            d_c -= 1
            self.dtmf_chars.append(bitbin.as_ascii(8))


class TimeDescriptor(SpliceDescriptor):
    """
    Table 25 - time_descriptor()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.tag = 4
        self.name = "Time Descriptor"
        self.tai_seconds = None
        self.tai_ns = None
        self.utc_offset = None

    def decode(self):
        """
        decode SCTE35 Time Descriptor
        """
        bitbin = BitBin(self.bites)
        self._parse_id(bitbin)
        self.tai_seconds = bitbin.as_int(48)
        self.tai_ns = bitbin.as_int(32)
        self.utc_offset = bitbin.as_int(16)


class AudioDescriptor(SpliceDescriptor):
    """
    Table 26 - audio_descriptor()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.tag = 4
        self.name = "Audio Descriptor"
        self.components = []
        self.audio_count = None

    def decode(self):
        """
        Decode SCTE35 Audio Descriptor
        """
        bitbin = BitBin(self.bites)
        self._parse_id(bitbin)
        self.audio_count = a_c = bitbin.as_int(4)
        bitbin.forward(4)
        while a_c:
            a_c -= 1
            comp = {}
            comp["component_tag"] = bitbin.as_int(8)
            comp["ISO_code="] = bitbin.as_int(24)
            comp["bit_stream_mode"] = bitbin.as_int(3)
            comp["num_channels"] = bitbin.as_int(4)
            comp["full_srvc_audio"] = bitbin.as_flag(1)
            self.components.append(comp)


class SegmentationDescriptor(SpliceDescriptor):
    """
    Table 19 - segmentation_descriptor()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.tag = 2
        self.name = "Segmentation Descriptor"
        self.segmentation_event_id = None
        self.segmentation_event_cancel_indicator = None
        self.component_count = None
        self.components = []
        self.program_segmentation_flag = None
        self.segmentation_duration_flag = None
        self.delivery_not_restricted_flag = None
        self.web_delivery_allowed_flag = None
        self.no_regional_blackout_flag = None
        self.archive_allowed_flag = None
        self.device_restrictions = None
        self.segmentation_duration = None
        self.segmentation_duration_raw = None
        self.segmentation_message = None
        self.segmentation_upid_type = None
        self.segmentation_upid_type_name = None
        self.segmentation_upid_length = None
        self.segmentation_upid = None
        self.segmentation_type_id = None
        self.segment_num = None
        self.segments_expected = None
        self.sub_segment_num = None
        self.sub_segments_expected = None

    def decode(self):
        """
        decode a segmentation descriptor
        """
        bitbin = BitBin(self.bites)
        self._parse_id(bitbin)
        self.segmentation_event_id = bitbin.as_hex(32)  # 4 bytes
        self.segmentation_event_cancel_indicator = bitbin.as_flag(1)
        bitbin.forward(7)  # 1 byte
        if not self.segmentation_event_cancel_indicator:
            self._decode_flags(bitbin)  # 1 byte
            if not self.program_segmentation_flag:
                self._decode_components(bitbin)
            self._decode_segmentation(bitbin)

    def _decode_components(self, bitbin):
        self.component_count = c_c = bitbin.as_int(8)  # 1 byte
        while c_c:  # 6 bytes each
            c_c -= 1
            comp = {}
            comp["component_tag"] = bitbin.as_int(8)
            bitbin.forward(7)
            comp["pts_offset"] = bitbin.as_90k(33)
            self.components.append(comp)

    def _decode_flags(self, bitbin):  # 1 byte for set flags
        self.program_segmentation_flag = bitbin.as_flag(1)
        self.segmentation_duration_flag = bitbin.as_flag(1)
        self.delivery_not_restricted_flag = bitbin.as_flag(1)
        if not self.delivery_not_restricted_flag:
            self.web_delivery_allowed_flag = bitbin.as_flag(1)
            self.no_regional_blackout_flag = bitbin.as_flag(1)
            self.archive_allowed_flag = bitbin.as_flag(1)
            self.device_restrictions = table20[bitbin.as_int(2)]
        else:
            bitbin.forward(5)

    def _decode_segmentation(self, bitbin):
        if self.segmentation_duration_flag:
            self.segmentation_duration_raw = bitbin.as_int(40)  # 5 bytes
            self.segmentation_duration = round(
                self.segmentation_duration_raw / 90000.0, 6
            )
        self.segmentation_upid_type = bitbin.as_int(8)  # 1 byte
        self.segmentation_upid_length = bitbin.as_int(8)  # 1 byte
        self.segmentation_upid_type_name, self.segmentation_upid = upid_decoder(
            bitbin, self.segmentation_upid_type, self.segmentation_upid_length
        )
        self.segmentation_type_id = bitbin.as_int(8)  # 1 byte
        if self.segmentation_type_id in table22.keys():
            self.segmentation_message = table22[self.segmentation_type_id]
            self._decode_segments(bitbin)

    def _decode_segments(self, bitbin):
        self.segment_num = bitbin.as_int(8)  # 1 byte
        self.segments_expected = bitbin.as_int(8)  # 1 byte
        if self.segmentation_type_id in [0x34, 0x36, 0x38, 0x3A]:
            if bitbin.idx > 16:
                self.sub_segment_num = bitbin.as_int(8)  # 1 byte
                self.sub_segments_expected = bitbin.as_int(8)  # 1 byte
            else:
                self.sub_segment_num = self.sub_segments_expected = 0


# map of known descriptors and associated classes
descriptor_map = {
    0: AvailDescriptor,
    1: DtmfDescriptor,
    2: SegmentationDescriptor,
    3: TimeDescriptor,
    4: AudioDescriptor,
}


def splice_descriptor(bites):
    """
    splice_descriptor reads the
    descriptor tag and decodes and
    returns an instance self._descriptor_map[tag]
    """
    # splice_descriptor_tag 8 uimsbf
    tag = bites[0]
    if tag not in descriptor_map:
        return False
    spliced = descriptor_map[tag](bites)
    spliced.decode()
    return spliced
