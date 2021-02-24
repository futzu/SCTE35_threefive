"""
SCTE35 Splice Descriptors
"""
from bitn import BitBin
from .base import SCTE35Base
from .segmentation import table20, table22
from .tools import k_by_v, i2b
from .upid import upid_decoder, upid_encoder


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

    def encode(self, nbin=None):
        nbin = self._chk_nbin(nbin)
        self.encode_id(nbin)
        return nbin

    def parse_id(self, bitbin):
        """
        parse splice descriptor identifier
        """
        self.identifier = bitbin.asdecodedhex(32)
        # identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
        if self.identifier != "CUEI":
            raise Exception('Descriptors should have an identifier of "CUEI"')

    def encode_id(self, nbin):
        """
        parse splice descriptor identifier
        """
        self.identifier = "CUEI"
        nbin.add_bites(self.identifier.encode("utf-8"), 32)


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
        self.parse_id(bitbin)
        self.provider_avail_id = bitbin.asint(32)

    def encode(self, nbin=None):
        """
        encode SCTE35 Avail Descriptor
        """
        nbin = super().encode(nbin)
        self.precheck(int, nbin.add_int, "provider_avail_id", 32)
        return nbin.bites


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
        self.parse_id(bitbin)
        self.preroll = bitbin.asint(8)
        self.dtmf_count = d_c = bitbin.asint(3)
        bitbin.forward(5)
        while d_c:
            d_c -= 1
            self.dtmf_chars.append(i2b(bitbin.asint(8), 1).decode("utf-8"))

    def encode(self, nbin=None):
        """
        encode SCTE35 Dtmf Descriptor
        """
        nbin = super().encode(nbin)
        self.precheck(int, nbin.add_int, "preroll", 8)
        d_c = 0
        self.precheck(int, nbin.add_int, "dtmf_count", 3)
        nbin.forward(5)
        while d_c < self.dtmf_count:
            nbin.add_int(ord(self.dtmf_chars[d_c]), 8)
            d_c += 1
        return nbin.bites


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
        self.parse_id(bitbin)
        self.tai_seconds = bitbin.asint(48)
        self.tai_ns = bitbin.asint(32)
        self.utc_offset = bitbin.asint(16)

    def encode(self, nbin=None):
        """
        encode SCTE35 Avail Descriptor
        """
        nbin = super().encode(nbin)
        self.precheck(int, nbin.add_int, "tai_seconds", 48)
        self.precheck(int, nbin.add_int, "tai_ns", 32)
        self.precheck(int, nbin.add_int, "utc_offset", 16)
        return nbin.bites


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
        self.parse_id(bitbin)
        self.audio_count = a_c = bitbin.asint(4)
        bitbin.forward(4)
        while a_c:
            a_c -= 1
            comp = {}
            comp["component_tag"] = bitbin.asint(8)
            comp["ISO_code="] = bitbin.asint(24)
            comp["bit_stream_mode"] = bitbin.asint(3)
            comp["num_channels"] = bitbin.asint(4)
            comp["full_srvc_audio"] = bitbin.asflag(1)
            self.components.append(comp)

    def encode(self, nbin=None):
        """
        encode SCTE35 Audio Descriptor
        """
        nbin = super().encode(nbin)
        nbin.add_int(self.audio_count, 4)
        nbin.forward(4)
        a_c = 0
        while a_c < self.audio_count:
            comp = self.components[a_c]
            nbin.add_int(comp["component_tag"], 8)
            nbin.add_int(comp["ISO_code="], 24)
            nbin.add_int(comp["bit_stream_mode"], 3)
            nbin.add_int(comp["num_channels"], 4)
            nbin.add_flag(comp["full_srvc_audio"])
        return nbin.bites


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
        self.parse_id(bitbin)
        self.segmentation_event_id = bitbin.ashex(32)  # 4 bytes
        self.segmentation_event_cancel_indicator = bitbin.asflag(1)
        bitbin.forward(7)  # 1 byte
        if not self.segmentation_event_cancel_indicator:
            self._decode_flags(bitbin)  # 1 byte
            if not self.program_segmentation_flag:
                self._decode_components(bitbin)
            self._decode_segmentation(bitbin)

    def encode(self, nbin=None):
        """
        encode a segmentation descriptor
        """
        nbin = super().encode(nbin)
        self.precheck(str, nbin.add_hex, "segmentation_event_id", 32)  # 4 bytes
        self.precheck(bool, nbin.add_flag, "segmentation_event_cancel_indicator", 1)
        nbin.forward(7)  # 1 byte
        if not self.segmentation_event_cancel_indicator:
            self._encode_flags(nbin)  # 1 byte
            if not self.program_segmentation_flag:
                self._encode_components(nbin)
            self._encode_segmentation(nbin)
        return nbin.bites

    def _decode_components(self, bitbin):
        self.component_count = c_c = bitbin.asint(8)  # 1 byte
        while c_c:  # 6 bytes each
            c_c -= 1
            comp = {}
            comp["component_tag"] = bitbin.asint(8)
            bitbin.forward(7)
            comp["pts_offset"] = bitbin.as90k(33)
            self.components.append(comp)

    def _encode_components(self, nbin):
        nbin.add_int(self.component_count, 8)  # 1 byte
        c_c = 0
        while c_c < self.component_count:  # 6 bytes each
            comp = self.components[c_c]
            nbin.add_int(comp["component_tag"], 8)
            nbin.forward(7)
            nbin.add_90k(comp["pts_offset"], 33)
            c_c += 1

    def _decode_flags(self, bitbin):  # 1 byte for set flags
        self.program_segmentation_flag = bitbin.asflag(1)
        self.segmentation_duration_flag = bitbin.asflag(1)
        self.delivery_not_restricted_flag = bitbin.asflag(1)
        if not self.delivery_not_restricted_flag:
            self.web_delivery_allowed_flag = bitbin.asflag(1)
            self.no_regional_blackout_flag = bitbin.asflag(1)
            self.archive_allowed_flag = bitbin.asflag(1)
            self.device_restrictions = table20[bitbin.asint(2)]
        else:
            bitbin.forward(5)

    def _encode_flags(self, nbin):  # 1 byte for set flags
        self.precheck(bool, nbin.add_flag, "program_segmentation_flag", 1)
        self.precheck(bool, nbin.add_flag, "segmentation_duration_flag", 1)
        self.precheck(bool, nbin.add_flag, "delivery_not_restricted_flag", 1)
        if not self.delivery_not_restricted_flag:
            self.precheck(bool, nbin.add_flag, "web_delivery_allowed_flag", 1)
            self.precheck(bool, nbin.add_flag, "no_regional_blackout_flag", 1)
            self.precheck(bool, nbin.add_flag, "archive_allowed_flag", 1)
            nbin.add_int(k_by_v(table20, self.device_restrictions), 2)
        else:
            nbin.reserve(5)

    def _decode_segmentation(self, bitbin):
        if self.segmentation_duration_flag:
            self.segmentation_duration_raw = bitbin.asint(40)  # 5 bytes
            self.segmentation_duration = round(
                self.segmentation_duration_raw / 90000.0, 6
            )
        self.segmentation_upid_type = bitbin.asint(8)  # 1 byte
        self.segmentation_upid_length = bitbin.asint(8)  # 1 byte
        self.segmentation_upid = upid_decoder(
            bitbin, self.segmentation_upid_type, self.segmentation_upid_length
        )
        self.segmentation_type_id = bitbin.asint(8)  # 1 byte
        if self.segmentation_type_id in table22.keys():
            self.segmentation_message = table22[self.segmentation_type_id]
            self._decode_segments(bitbin)

    def _encode_segmentation(self, nbin):
        if self.segmentation_duration_flag:
            self.precheck(int, nbin.add_int, "segmentation_duration_raw", 40)  # 5 bytes
        self.precheck(int, nbin.add_int, "segmentation_upid_type", 8)  # 1 byte
        self.precheck(int, nbin.add_int, "segmentation_upid_length", 8)  # 1 byte
        upid_encoder(
            nbin,
            self.segmentation_upid_type,
            self.segmentation_upid_length,
            self.segmentation_upid,
        )
        self.precheck(int, nbin.add_int, "segmentation_type_id", 8)  # 1 byte
        self._encode_segments(nbin)

    def _decode_segments(self, bitbin):
        self.segment_num = bitbin.asint(8)  # 1 byte
        self.segments_expected = bitbin.asint(8)  # 1 byte
        if self.segmentation_type_id in [0x34, 0x36, 0x38, 0x3A]:
            if bitbin.idx > 16:
                self.sub_segment_num = bitbin.asint(8)  # 1 byte
                self.sub_segments_expected = bitbin.asint(8)  # 1 byte
            else:
                self.sub_segment_num = self.sub_segments_expected = 0

    def _encode_segments(self, nbin):
        self.precheck(int, nbin.add_int, "segment_num", 8)  # 1 byte
        self.precheck(int, nbin.add_int, "segments_expected", 8)  # 1 byte
        # if self.segmentation_type_id in [0x34, 0x36, 0x38, 0x3A]:
        # nbin.add_int(self.sub_segment_num, 8)  # 1 byte
        #  nbin.add_int(self.sub_segments_expected, 8)  # 1 byte


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
