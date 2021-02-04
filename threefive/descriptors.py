"""
SCTE35 Splice Descriptors
"""
from bitn import BitBin, NBin
from .segmentation import table20, table22
from .tools import k_by_v, i2b, ifb, to_stderr


class SpliceDescriptor:
    """
    SpliceDescriptor is the
    base class for all splice descriptors.
    It should not be used directly
    """

    def __init__(self, bites=None):
        self.tag = None
        self.descriptor_length = None
        self.identifier = None
        self.bites = bites
        if bites:
            self.tag = bites[0]
            self.descriptor_length = bites[1]
            self.bites = bites[2:]

    def decode(self):
        """
        SpliceDescriptor subclasses
        must implement a decode method.
        """

    def encode_meta(self, nbin):
        nbin.add_int(self.tag, 8)
        nbin.add_int(self.descriptor_length, 8)

    def encode(self, nbin=None):
        if not nbin:
            nbin = NBin()
        self.encode_meta(nbin)
        self.encode_id(nbin)
        return nbin

    def parse_id(self, bitbin):
        """
        parse splice descriptor identifier
        """
        self.identifier = bitbin.asdecodedhex(32)
        # identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
        if self.identifier != "CUEI":
            to_stderr('Descriptors should have an identifier of "CUEI"')

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
        nbin.add_int(self.provider_avail_id, 32)
        return nbin


class DtmfDescriptor(SpliceDescriptor):
    """
    Table 18 -  DTMF_descriptor()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
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
        nbin.add_int(self.preroll, 8)
        d_c = 0
        nbin.add_int(self.dtmf_count, 3)
        nbin.forward(5)
        while d_c < self.dtmf_count:
            nbin.add_int(ord(self.dtmf_chars[d_c]), 8)
            d_c += 1
        return nbin


class TimeDescriptor(SpliceDescriptor):
    """
    Table 25 - time_descriptor()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
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
        nbin.add_int(self.tai_seconds, 48)
        nbin.add_int(self.tai_ns, 32)
        nbin.add_int(self.utc_offset, 16)
        return nbin


class AudioDescriptor(SpliceDescriptor):
    """
    Table 26 - audio_descriptor()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
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
        return nbin


class SegmentationDescriptor(SpliceDescriptor):
    """
    Table 19 - segmentation_descriptor()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
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
        nbin.add_hex(self.segmentation_event_id, 32)  # 4 bytes
        nbin.add_flag(self.segmentation_event_cancel_indicator)
        nbin.forward(7)  # 1 byte
        if not self.segmentation_event_cancel_indicator:
            self._encode_flags(nbin)  # 1 byte
            if not self.program_segmentation_flag:
                self._encode_components(nbin)
            self._encode_segmentation(nbin)

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
        nbin.add_flag(self.program_segmentation_flag)
        nbin.add_flag(self.segmentation_duration_flag)
        nbin.add_flag(self.delivery_not_restricted_flag)
        if not self.delivery_not_restricted_flag:
            nbin.add_flag(self.web_delivery_allowed_flag)
            nbin.add_flag(self.no_regional_blackout_flag)
            nbin.add_flag(self.archive_allowed_flag)
            nbin.add_int(k_by_v(table20, self.device_restrictions), 2)
        else:
            nbin.forward(5)

    def _decode_segmentation(self, bitbin):
        if self.segmentation_duration_flag:
            self.segmentation_duration = bitbin.as90k(40)  # 5 bytes
        self.segmentation_upid_type = bitbin.asint(8)  # 1 byte
        self.segmentation_upid_length = bitbin.asint(8)  # 1 byte
        self.segmentation_upid = self._decode_segmentation_upid(
            bitbin, self.segmentation_upid_type, self.segmentation_upid_length
        )
        self.segmentation_type_id = bitbin.asint(8)  # 1 byte
        if self.segmentation_type_id in table22.keys():
            self.segmentation_message = table22[self.segmentation_type_id]
            self._decode_segments(bitbin)
        bitbin = None

    def _encode_segmentation(self, nbin):
        if self.segmentation_duration_flag:
            nbin.add_90k(self.segmentation_duration, 40)  # 5 bytes
        nbin.add_int(self.segmentation_upid_type, 8)  # 1 byte
        nbin.add_int(self.segmentation_upid_length, 8)  # 1 byte
        self._encode_segmentation_upid(
            nbin, self.segmentation_upid_type, self.segmentation_upid_length
        )
        nbin.add_int(self.segmentation_type_id, 8)  # 1 byte
        # if self.segmentation_type_id in table22.keys():
        #   self.segmentation_message = table22[self.segmentation_type_id]
        self._encode_segments(nbin)

    def _decode_segmentation_upid(self, bitbin, upid_type, upid_length):

        upid_map = {
            0x02: ["Deprecated", self._uri],
            0x03: ["Ad ID", self._uri],
            0x04: ["UMID", self._umid],
            0x05: ["ISAN", self._isan],
            0x06: ["ISAN", self._isan],  # works
            0x07: ["TID", self._uri],
            0x08: ["AiringID", self._air_id],
            0x09: ["ADI", self._uri],
            0x0A: ["EIDR", self._eidr],
            0x0B: ["ATSC", self._atsc],
            0x0C: ["MPU", self._mpu],
            0x0D: ["MID", self._mid],  # works
            0x0E: ["ADS Info", self._uri],  # works
            0x0F: ["URI", self._uri],  # works
        }

        upid_id = ""
        if upid_type in upid_map.keys():
            upid_id = upid_map[upid_type][1](bitbin, upid_length)
            if upid_type != 0x09:
                return f"{upid_map[upid_type][0]}:{upid_id}"
        return upid_id

    def _encode_segmentation_upid(self, nbin, upid_type, upid_length):
        """
            0x02  # works
            0x03  # works
            0x04
            0x05  # works
            0x06 
            0x07  # works
            0x08
            0x09
            0x0A # maybe works
            0x0B
            0x0C
            0x0D 
            0x0E  # works
            0x0F  # works
        """
        if upid_type in [0x02, 0x03, 0x07, 0x0E, 0x0F]:
            seg_upid = (self.segmentation_upid.split(":", 1)[1]).encode("utf-8")
            nbin.add_bites(seg_upid, (upid_length << 3))
            return
        if upid_type in [0x0A]:
            # 0xa : EIDR:10.5240/f85a-e100-b068-5b8f-T
            pre, post = self.segmentation_upid[8:].split("/")
            nbin.add_int(int(pre), 16)
            repost = post.replace("-T", "").replace("-", "")  # .encode("utf-8")
            nbin.add_hex(repost, 80)
            return
        if upid_type in [0x08]:
            aired = self.segmentation_upid.split(":", 1)[1]
            aired = (aired[:-(upid_length)]).encode("utf-8")
            nbin.add_bites(aired, (upid_length << 3))

    def _decode_segments(self, bitbin):
        self.segment_num = bitbin.asint(8)  # 1 byte
        self.segments_expected = bitbin.asint(8)  # 1 byte
        if self.segmentation_type_id in [0x34, 0x36, 0x38, 0x3A]:
            """
            if there are 16 more bits in bitbin, read them.
            """
            if bitbin.idx >= 16:
                self.sub_segment_num = bitbin.asint(8)  # 1 byte
                self.sub_segments_expected = bitbin.asint(8)  # 1 byte
            else:
                self.sub_segment_num = self.sub_segments_expected = 0

    def _encode_segments(self, nbin):
        nbin.add_int(self.segment_num, 8)  # 1 byte
        nbin.add_int(self.segments_expected, 8)  # 1 byte
        if self.segmentation_type_id in [0x34, 0x36, 0x38, 0x3A]:
            """
            if there are 16 more bits in bitbin, read them.
            """
            if self.sub_segment_num:
                nbin.add_int(self.sub_segment_num, 8)  # 1 byte
                nbin.add_int(self.sub_segments_expected, 8)  # 1 byte
            # else:
            #   self.sub_segment_num = self.sub_segments_expected = 0

    @staticmethod
    def _air_id(bitbin, upid_length):
        return bitbin.ashex(upid_length << 3)

    @staticmethod
    def _atsc(bitbin, upid_length):
        return {
            "TSID": bitbin.asint(16),
            "reserved": bitbin.asint(2),
            "end_of_day": bitbin.asint(5),
            "unique_for": bitbin.asint(9),
            "content_id": bitbin.asdecodedhex((upid_length - 4) << 3),
        }

    @staticmethod
    def _isan(bitbin, upid_length):
        pre = "0000-0000-"
        middle = bitbin.ashex(upid_length << 3)
        post = "-0000-Z-0000-0000-6"
        return f"{pre}{middle[2:6]}{post}"

    def _mid(self, bitbin, upid_length):
        upids = []
        b_c = upid_length << 3
        while b_c:
            upid_type = bitbin.asint(8)  # 1 byte
            b_c -= 8
            upid_length = bitbin.asint(8)
            b_c -= 8
            segmentation_upid = self._decode_segmentation_upid(
                bitbin, upid_type, upid_length
            )
            b_c -= upid_length << 3
            upids.append(segmentation_upid)
        return upids

    @staticmethod
    def _mpu(bitbin, upid_length):
        b_c = upid_length << 3
        return {
            "format identifier": bitbin.asint(32),
            "private data": bitbin.asint(b_c - 32),
        }

    @staticmethod
    def _eidr(bitbin, upid_length):
        pre = bitbin.asint(16)
        post = bitbin.ashex(80)
        return f"10.{pre}/{post[2:6]}-{post[6:10]}-{post[10:14]}-{post[14:18]}-T"

    @staticmethod
    def _umid(bitbin, upid_length):
        n_u = 8
        pre = "".join(bitbin.ashex(upid_length << 3).split("x", 1))
        return ".".join([pre[i : i + n_u] for i in range(0, len(pre), n_u)])

    @staticmethod
    def _uri(bitbin, upid_length):
        if upid_length > 0:
            return bitbin.asdecodedhex(upid_length << 3)
        return None


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
