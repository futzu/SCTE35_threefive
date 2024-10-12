"""
SCTE35 Splice Descriptors
"""

from .bitn import BitBin
from .base import SCTE35Base
from .segmentation import table20, table22, dvb_table2
from .upids import upid_map
from .xml import Node


def k_by_v(adict, avalue):
    """
    dict key lookup by value
    """
    for kay, vee in adict.items():
        if vee == avalue:
            return kay
    return None


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
        self.private_data = None

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

    def decode(self):
        """
        decode handles Private Descriptors
        """
        self.private_data = self.bites.decode()
        if isinstance(self.private_data, bytes):
            self.private_data = self.bites.decode()

    def encode(self, nbin=None):
        """
        SpliceDescriptor.encode
        """
        nbin = self._chk_nbin(nbin)
        self._encode_id(nbin)
        if self.private_data:
            if isinstance(self.private_data, str):
                self.private_data = self.private_data.encode()
            nbin.add_bites(self.private_data)
        if self.tag in descriptor_map:
            return nbin
        return nbin.bites

    def _encode_id(self, nbin):
        """
        parse splice descriptor identifier
        """
        # self.identifier = "CUEI"
        id_int = int.from_bytes(self.identifier.encode(), byteorder="big")
        nbin.add_int(id_int, 32)


class DVBDASDescriptor(SpliceDescriptor):
    """
    Experimental DVB Descriptor Support
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.tag = 240  # 0xf0
        self.name = "DVD DAS Descriptor"
        self.identifier = "DVB_"
        self.break_num = 0
        self.breaks_expected = 0
        self.equivalent_segmentation_type = None
        self.equivalent_segmentation_message = None
        self.upid_type = 0x0F
        self.upid_type_name = None
        self.upid_length = None
        self.upid = None

    def decode(self):
        """
        Decode DVB DAS Descriptor
        """
        bitbin = BitBin(self.bites)
        self.break_num = bitbin.as_int(8)
        self.breaks_expected = bitbin.as_int(8)
        bitbin.forward(4)
        self.equivalent_segmentation_type = bitbin.as_int(4)
        if self.equivalent_segmentation_type in dvb_table2:
            self.equivalent_segmentation_message = dvb_table2[
                self.equivalent_segmentation_type
            ]
        self.upid_length = len(self.bites) - 3
        the_upid = upid_map[self.upid_type][1](bitbin, self.upid_type, self.upid_length)
        self.upid_type_name, self.upid = the_upid.decode()

    def encode(self, nbin=None):
        """
        encode DVB DAS Descriptor
        """
        nbin = super().encode(nbin)
        nbin.add_int(self.break_num, 8)
        nbin.add_int(self.breaks_expected, 8)
        nbin.forward(4)
        nbin.add_int(self.equivalent_segmentation_type, 4)
        the_upid = upid_map[self.upid_type][1](None, self.upid_type, self.upid_length)
        the_upid.encode(nbin, self.upid)
        return nbin.bites


class AvailDescriptor(SpliceDescriptor):
    """
    Table 17 -  avail_descriptor()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.name = "Avail Descriptor"
        self.tag = 0
        self.identifier = "CUEI"
        self.provider_avail_id = None

    def decode(self):
        """
        decode SCTE35 Avail Descriptor
        """
        bitbin = BitBin(self.bites)
        self.provider_avail_id = bitbin.as_int(32)

    def encode(self, nbin=None):
        """
        encode SCTE35 Avail Descriptor
        """
        nbin = super().encode(nbin)
        self._chk_var(int, nbin.add_int, "provider_avail_id", 32)
        return nbin.bites

    def xml(self):
        """
        Create a Node describing the AvailDescriptor
        """
        ad = Node("AvailDescriptor", attrs={"providerAvailId": self.provider_avail_id})
        return ad

    def from_xml(self, stuff):
        """
        Load an AvailDescriptor from XML
        """
        if "AvailDescriptor" in stuff:
            self.load(stuff["AvailDescriptor"])


class DtmfDescriptor(SpliceDescriptor):
    """
    Table 18 -  DTMF_descriptor()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.name = "DTMF Descriptor"
        self.tag = 1
        self.identifier = "CUEI"
        self.preroll = None
        self.dtmf_count = 0
        self.dtmf_chars = None

    def decode(self):
        """
        decode SCTE35 Dtmf Descriptor
        """
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

    def xml(self):
        """
        Create a Node describing a DTMFDescriptor
        """
        dd = Node(
            "DTMFDescriptor",
            attrs={
                "preroll": self.preroll,
                "chars": "".join(self.dtmf_chars),
            },
        )
        return dd

    def from_xml(self, stuff):
        """
        Load an DTMFDescriptor from XML
        """
        if "DTMFDescriptor" in stuff:
            stuff["DTMFDescriptor"]["dtmf_chars"] = stuff["DTMFDescriptor"].pop("chars")
            self.load(stuff["DTMFDescriptor"])
            self.dtmf_count = len(self.dtmf_chars)


class TimeDescriptor(SpliceDescriptor):
    """
    Table 25 - time_descriptor()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.tag = 3
        self.name = "Time Descriptor"
        self.identifier = "CUEI"
        self.tai_seconds = 0
        self.tai_ns = 0
        self.utc_offset = 0

    def decode(self):
        """
        decode SCTE35 Time Descriptor
        """
        bitbin = BitBin(self.bites)
        self.tai_seconds = bitbin.as_int(48)
        self.tai_ns = bitbin.as_int(32)
        self.utc_offset = bitbin.as_int(16)

    def encode(self, nbin=None):
        """
        encode SCTE35 Time Descriptor
        """
        nbin = super().encode(nbin)
        self._chk_var(int, nbin.add_int, "tai_seconds", 48)
        self._chk_var(int, nbin.add_int, "tai_ns", 32)
        self._chk_var(int, nbin.add_int, "utc_offset", 16)
        return nbin.bites

    def xml(self):
        """
        create a Node describing a TimeDescriptor
        """
        td = Node(
            "TimeDescriptor",
            attrs={
                "tai_seconds": self.tai_seconds,
                "tai_ns": self.tai_ns,
                "utc_offset": self.utc_offset,
            },
        )
        return td

    def from_xml(self, stuff):
        """
        load a TimeDescriptor from XML
        """
        if "TimeDescriptor" in stuff:
            self.load(stuff["TimeDescriptor"])


class SegmentationDescriptor(SpliceDescriptor):
    """
    Table 19 - segmentation_descriptor()
    """

    SUB_SEG_TYPES = [
        0x30,
        0x32,
        0x34,
        0x36,
        0x38,
        0x3A,
        0x44,
        0x46,
    ]

    def __init__(self, bites=None):
        super().__init__(bites)
        self.tag = 2
        self.name = "Segmentation Descriptor"
        self.identifier = "CUEI"
        self.segmentation_event_id = None
        self.segmentation_event_cancel_indicator = None
        self.segmentation_event_id_compliance_indicator = None
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
        self.segmentation_event_id = bitbin.as_hex(32)
        self.segmentation_event_cancel_indicator = bitbin.as_flag(1)
        self.segmentation_event_id_compliance_indicator = bitbin.as_flag(1)
        bitbin.forward(6)
        if not self.segmentation_event_cancel_indicator:
            self._decode_flags(bitbin)
            self._decode_segmentation(bitbin)

    def _decode_flags(self, bitbin):
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
            segmentation_duration_ticks = bitbin.as_int(40)
            self.segmentation_duration = self.as_90k(segmentation_duration_ticks)
        self.segmentation_upid_type = bitbin.as_int(8)
        self.segmentation_upid_length = bitbin.as_int(8)
        the_upid = self.mk_the_upid(bitbin)
        self.segmentation_upid_type_name, self.segmentation_upid = the_upid.decode()
        self.segmentation_type_id = bitbin.as_int(8)
        self._decode_segments(bitbin)

    def _chk_sub_segments(self):
        """
        chk_sub_segments sets sub_segment vars if not present
        """
        if self.segmentation_type_id in self.SUB_SEG_TYPES:
            if not self.sub_segment_num:
                self.sub_segment_num = 0
                self.sub_segments_expected = 0

    def _decode_segments(self, bitbin):
        self.segment_num = bitbin.as_int(8)
        self.segments_expected = bitbin.as_int(8)
        if self.segmentation_type_id in self.SUB_SEG_TYPES:
            # if sub_segment_num and sub_segments_expected
            # are not available set both of them to zero
            try:
                self.sub_segment_num = bitbin.as_int(8)
                self.sub_segments_expected = bitbin.as_int(8)
            finally:
                self._chk_sub_segments()

    def encode(self, nbin=None):
        """
        encode a segmentation descriptor
        """
        nbin = super().encode(nbin)
        self._chk_var(str, nbin.add_hex, "segmentation_event_id", 32)
        self._chk_var(bool, nbin.add_flag, "segmentation_event_cancel_indicator", 1)
        self._chk_var(
            bool, nbin.add_flag, "segmentation_event_id_compliance_indicator", 1
        )
        nbin.forward(6)
        if not self.segmentation_event_cancel_indicator:
            self._encode_flags(nbin)

            self._encode_segmentation(nbin)
        return nbin.bites

    def _encode_flags(self, nbin):
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

    def mk_the_upid(self, bitbin=None):
        """
        mk_the_upid create a upid instance
        and return it. the bitbin arg is only
        used in decode()
        """
        upid_type = self.segmentation_upid_type
        if upid_type not in upid_map:
            upid_type = 0xFD
        the_upid = upid_map[upid_type][1](
            bitbin, upid_type, self.segmentation_upid_length
        )
        return the_upid

    def _encode_segmentation(self, nbin):
        if self.segmentation_duration_flag:
            nbin.add_int(self.as_ticks(self.segmentation_duration), 40)
        self._chk_var(int, nbin.add_int, "segmentation_upid_type", 8)
        self._chk_var(int, nbin.add_int, "segmentation_upid_length", 8)
        upid_type = self.segmentation_upid_type
        if upid_type not in upid_map:
            upid_type = 0xFD
        the_upid = upid_map[upid_type][1](
            None, upid_type, self.segmentation_upid_length
        )
        the_upid.encode(nbin, self.segmentation_upid)
        self._chk_var(int, nbin.add_int, "segmentation_type_id", 8)
        self._encode_segments(nbin)

    def _encode_segments(self, nbin):
        self._chk_var(int, nbin.add_int, "segment_num", 8)
        self._chk_var(int, nbin.add_int, "segments_expected", 8)
        if self.segmentation_type_id in [
            0x30,
            0x32,
            0x34,
            0x36,
            0x38,
            0x3A,
            0x44,
            0x46,
        ]:
            try:
                self._chk_var(int, nbin.add_int, "sub_segment_num", 8)
                self._chk_var(int, nbin.add_int, "sub_segments_expected", 8)
            except:
                nbin.add_int(0, 8)
                nbin.add_int(0, 8)

    def xml(self):
        """
        Create a Node describing a SegmentationDescriptor
        """
        sd_attrs = {
            "segmentation_event_id": int(self.segmentation_event_id, 0),
            "segmentation_event_cancel_indicator": self.segmentation_event_cancel_indicator,
            "segmentation_event_id_compliance_indicator": self.segmentation_event_id_compliance_indicator,
            "segmentation_type_id": self.segmentation_type_id,
            "segment_num": self.segment_num,
            "segments_expected": self.segments_expected,
        }
        if self.segmentation_type_id in self.SUB_SEG_TYPES:
            sd_attrs["sub_segment_num"] = self.sub_segment_num
            sd_attrs["sub_segments_expected"] = self.sub_segments_expected
        if self.segmentation_duration_flag:
            sd_attrs["segmentation_duration"] = self.as_ticks(
                self.segmentation_duration
            )
        sd = Node("SegmentationDescriptor", attrs=sd_attrs)
        the_upid = self.mk_the_upid()
        the_upid.upid_value = self.segmentation_upid
        upid_node = the_upid.xml()
        if not self.delivery_not_restricted_flag:
            dr_attrs = {
                "web_delivery_allowed_flag": self.web_delivery_allowed_flag,
                "no_regional_blackout_flag": self.no_regional_blackout_flag,
                "archive_allowed_flag": self.archive_allowed_flag,
                "device_restrictions": k_by_v(table20, self.device_restrictions),
            }
            dr = Node("DeliveryRestrictions", attrs=dr_attrs)
            sd.add_child(dr)
        sd.add_comment(f"UPID: {upid_map[self.segmentation_upid_type][0]}")
        if isinstance(upid_node, list):
            for node in upid_node:
                sd.add_child(node)
        else:
            sd.add_child(upid_node)
        return sd

    def _upid_from_xml(self, stuff):
        if "SegmentationUpid" in stuff:
            self.load(stuff["SegmentationUpid"])
            upid_length = upid_map[self.segmentation_upid_type][2]
            self.segmentation_upid_type_name = upid_map[self.segmentation_upid_type][0]
            if upid_length:
                self.segmentation_upid_length = upid_length
                return True
            if self.segmentation_upid:
                self.segmentation_upid_length = len(
                    self.segmentation_upid.lower().replace("0x", "")
                )
                return True
            self.segmentation_upid = ""
            self.segmentation_upid_length = 0
        return False

    def from_xml(self, stuff):
        """
        Load a SegmentationDescriptor from XML
        """
        self.load(stuff["SegmentationDescriptor"])
        self.segmentation_event_id_compliance_indicator = True
        self.program_segmentation_flag = True
        self.segmentation_duration_flag = False
        if "segmentationDuration" in stuff["SegmentationDescriptor"]:
            self.segmentation_duration_flag = True
        self.delivery_not_restricted_flag = True
        if "DeliveryRestrictions" in stuff:
            self.delivery_not_restricted_flag = False
            self.load(stuff["DeliveryRestrictions"])
            self.device_restrictions = table20[self.device_restrictions]
        self.segmentation_event_id = hex(self.segmentation_event_id)
        if self.segmentation_type_id in table22:
            self.segmentation_message = table22[self.segmentation_type_id]
        self._upid_from_xml(stuff)
        self._chk_sub_segments()


# map of known descriptors and associated classes
descriptor_map = {
    0: AvailDescriptor,
    1: DtmfDescriptor,
    2: SegmentationDescriptor,
    3: TimeDescriptor,
    240: DVBDASDescriptor,
}


def splice_descriptor(bites):
    """
    replaced splice_descriptor
    """
    spliced = None
    tag = bites[0]
    if tag in descriptor_map:
        spliced = descriptor_map[tag](bites)
    else:
        spliced = SpliceDescriptor(bites)
    spliced.decode()
    return spliced
