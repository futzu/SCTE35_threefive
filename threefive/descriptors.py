"""
SCTE35 Splice Descriptors
"""
from .bitn import BitBin
from .base import SCTE35Base
from .segmentation import table20, table22
from .upid import upid_decoder, upid_encoder


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
        self.tag = None
        self.descriptor_length = 0
        self.name = None
        self.identifier = None
        self.bites = bites
        self.parse_tag_and_len()
        self.parse_id()
        self.provider_avail_id = None
        self.components = None

    def parse_tag_and_len(self):
        """
        parse_tag_and_len
        parses the descriptors tag and length
        from self.bites
        """
        if self.bites:
            self.tag = self.bites[0]
            self.descriptor_length = self.bites[1]
            self.bites = self.bites[2:]

    def parse_id(self):
        """
        parse splice descriptor identifier
        """
        if self.bites:
            self.identifier = self.bites[:4].decode()
            # disabled for ffmv30
            #      if self.identifier != "CUEI":
            #          raise Exception('Identifier Is Not "CUEI"')
            self.bites = self.bites[4:]

    def encode(self, nbin=None):
        """
        SpliceDescriptor.encode
        """
        nbin = self._chk_nbin(nbin)
        self._encode_id(nbin)
        return nbin

    def _encode_id(self, nbin):
        """
        parse splice descriptor identifier
        """
        # self.identifier = "CUEI"
        id_int = int.from_bytes(self.identifier.encode(), byteorder="big")
        nbin.add_int(id_int, 32)


class AudioDescriptor(SpliceDescriptor):
    """q
    Table 26 - audio_descriptor()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.tag = 4
        self.name = "Audio Descriptor"
        self.components = []
        self.audio_count = None

    def _decode_comp(self, bitbin):
        """
        AudioDescriptor._mk_comp parses
        for audio component data.
        """
        comp = {}
        comp["component_tag"] = bitbin.as_int(8)
        comp["ISO_code="] = bitbin.as_int(24)
        comp["bit_stream_mode"] = bitbin.as_int(3)
        comp["num_channels"] = bitbin.as_int(4)
        comp["full_srvc_audio"] = bitbin.as_flag(1)
        self.components.append(comp)

    def _encode_comp(self, comp, nbin):
        nbin.add_int(comp["component_tag"], 8)
        nbin.add_int(comp["ISO_code="], 24)
        nbin.add_int(comp["bit_stream_mode"], 3)
        nbin.add_int(comp["num_channels"], 4)
        nbin.add_flag(comp["full_srvc_audio"])

    def decode(self):
        """
        Decode SCTE35 Audio Descriptor
        """
        self.name = "Audio Descriptor"
        bitbin = BitBin(self.bites)
        a_c = bitbin.as_int(4)
        bitbin.forward(4)
        self.components = []
        while a_c:
            a_c -= 1
            self._decode_comp(bitbin)

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
            self._encode_comp(comp, nbin)
            a_c += 1
        return nbin.bites


class AvailDescriptor(SpliceDescriptor):
    """
    Table 17 -  avail_descriptor()
    """

    def decode(self):
        """
        decode SCTE35 Avail Descriptor
        """
        self.name = "Avail Descriptor"
        bitbin = BitBin(self.bites)
        self.provider_avail_id = bitbin.as_int(32)

    def encode(self, nbin=None):
        """
        encode SCTE35 Avail Descriptor
        """
        nbin = super().encode(nbin)
        self._chk_var(int, nbin.add_int, "provider_avail_id", 32)
        return nbin.bites


class DtmfDescriptor(SpliceDescriptor):
    """
    Table 18 -  DTMF_descriptor()
    """

    def __init__(self, bites):
        super().__init__(bites)
        self.preroll = None
        self.dtmf_count = None
        self.dtmf_chars = None

    def decode(self):
        """
        decode SCTE35 Dtmf Descriptor
        """
        self.name = "DTMF Descriptor"
        self.preroll = self.bites[0]
        self.dtmf_count = self.bites[1] >> 5
        self.bites = self.bites[2:]
        self.dtmf_chars = list(self.bites[: self.dtmf_count].decode())

    def encode(self, nbin=None):
        """
        encode SCTE35 Dtmf Descriptor
        """
        nbin = super().encode(nbin)
        self._chk_var(int, nbin.add_int, "preroll", 8)
        d_c = 0
        self._chk_var(int, nbin.add_int, "dtmf_count", 3)
        nbin.forward(5)
        while d_c < self.dtmf_count:
            nbin.add_int(ord(self.dtmf_chars[d_c]), 8)
            d_c += 1
        return nbin.bites


class TimeDescriptor(SpliceDescriptor):
    """
    Table 25 - time_descriptor()
    """

    def __init__(self, bites):
        super().__init__(bites)
        self.tai_seconds = None
        self.tai_ns = None
        self.utc_offset = None

    def decode(self):
        """
        decode SCTE35 Time Descriptor
        """
        self.name = "Time Descriptor"
        bitbin = BitBin(self.bites)
        self.tai_seconds = bitbin.as_int(48)
        self.tai_ns = bitbin.as_int(32)
        self.utc_offset = bitbin.as_int(16)

    def encode(self, nbin=None):
        """
        encode SCTE35 Avail Descriptor
        """
        nbin = super().encode(nbin)
        self._chk_var(int, nbin.add_int, "tai_seconds", 48)
        self._chk_var(int, nbin.add_int, "tai_ns", 32)
        self._chk_var(int, nbin.add_int, "utc_offset", 16)
        return nbin.bites


class SegmentationDescriptor(SpliceDescriptor):
    """
    Table 19 - segmentation_descriptor()
    """

    def __init__(self, bites):
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
        self.segmentation_event_id = bitbin.as_hex(32)  # 4 bytes
        self.segmentation_event_cancel_indicator = bitbin.as_flag(1)
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
        self._chk_var(str, nbin.add_hex, "segmentation_event_id", 32)  # 4 bytes
        self._chk_var(bool, nbin.add_flag, "segmentation_event_cancel_indicator", 1)
        nbin.forward(7)  # 1 byte
        if not self.segmentation_event_cancel_indicator:
            self._encode_flags(nbin)  # 1 byte
            if not self.program_segmentation_flag:
                self._encode_components(nbin)
            self._encode_segmentation(nbin)
        return nbin.bites

    def _decode_components(self, bitbin):
        self.component_count = c_c = bitbin.as_int(8)  # 1 byte
        while c_c:  # 6 bytes each
            c_c -= 1
            comp = {}
            comp["component_tag"] = bitbin.as_int(8)
            bitbin.forward(7)
            comp["pts_offset"] = bitbin.as_90k(33)
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

    def _encode_flags(self, nbin):  # 1 byte for set flags
        self._chk_var(bool, nbin.add_flag, "program_segmentation_flag", 1)
        self._chk_var(bool, nbin.add_flag, "segmentation_duration_flag", 1)
        self._chk_var(bool, nbin.add_flag, "delivery_not_restricted_flag", 1)
        if not self.delivery_not_restricted_flag:
            self._chk_var(bool, nbin.add_flag, "web_delivery_allowed_flag", 1)
            self._chk_var(bool, nbin.add_flag, "no_regional_blackout_flag", 1)
            self._chk_var(bool, nbin.add_flag, "archive_allowed_flag", 1)
            a_key = k_by_v(table20, self.device_restrictions)
            nbin.add_int(a_key, 2)
        else:
            nbin.reserve(5)

    def _decode_segmentation(self, bitbin):
        if self.segmentation_duration_flag:
            self.segmentation_duration = bitbin.as_90k(40)  # 5 bytes
        self.segmentation_upid_type = bitbin.as_int(8)  # 1 byte
        self.segmentation_upid_length = bitbin.as_int(8)  # 1 byte
        self.segmentation_upid_type_name, self.segmentation_upid = upid_decoder(
            bitbin, self.segmentation_upid_type, self.segmentation_upid_length
        )
        self.segmentation_type_id = bitbin.as_int(8)  # 1 byte
        if self.segmentation_type_id in table22.keys():
            self.segmentation_message = table22[self.segmentation_type_id]
            self._decode_segments(bitbin)

    def _encode_segmentation(self, nbin):
        if self.segmentation_duration_flag:
            self._chk_var(float, nbin.add_90k, "segmentation_duration", 40)  # 5 bytes
        self._chk_var(int, nbin.add_int, "segmentation_upid_type", 8)  # 1 byte
        self._chk_var(int, nbin.add_int, "segmentation_upid_length", 8)  # 1 byte
        upid_encoder(
            nbin,
            self.segmentation_upid_type,
            self.segmentation_upid_length,
            self.segmentation_upid,
        )
        self._chk_var(int, nbin.add_int, "segmentation_type_id", 8)  # 1 byte
        self._encode_segments(nbin)

    def _decode_segments(self, bitbin):
        self.segment_num = bitbin.as_int(8)  # 1 byte
        self.segments_expected = bitbin.as_int(8)  # 1 byte
        if self.segmentation_type_id in [0x34, 0x36, 0x38, 0x3A]:
            if bitbin.idx > 16:
                self.sub_segment_num = bitbin.as_int(8)  # 1 byte
                self.sub_segments_expected = bitbin.as_int(8)  # 1 byte
            # else:
            self.sub_segment_num = self.sub_segments_expected = 0

    def _encode_segments(self, nbin):
        self._chk_var(int, nbin.add_int, "segment_num", 8)  # 1 byte
        self._chk_var(int, nbin.add_int, "segments_expected", 8)  # 1 byte
        # if self.segmentation_type_id in [0x34, 0x36, 0x38, 0x3A]:

    # if self.segment_num and self.segment_num > 0:
    #   if self.sub_segments_expected and self.sub_segments_expected > 0:
    #     self._chk_var(int, nbin.add_int, "sub_segment_num", 8)  # 1 byte
    #   self._chk_var(int, nbin.add_int, "sub_segments_expected", 8)  # 1 byte
    # nbin.add_int(self.sub_segment_num, 8)  # 1 byte
    # nbin.add_int(self.sub_segments_expected, 8)  # 1 byte


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
