"""
segmentation.py

SCTE35 Segmentation Descriptors
"""

from .descriptors import SpliceDescriptor


"""
Table 20 from page 58 of
https://www.scte.org/SCTEDocs/Standards/ANSI_SCTE%2035%202019r1.pdf
"""
table20 = {
    0x00: "Restrict Group 0",
    0x01: "Restrict Group 1",
    0x02: "Restrict Group 2",
    0x03: "No Restrictions",
}

"""
table 22 from page 62 of
https://www.scte.org/SCTEDocs/Standards/ANSI_SCTE%2035%202019r1.pdf
I am using the segmentation_type_id as a key.
Segmentation_type_id : segmentation_message
"""
table22 = {
    0x00: "Not Indicated",
    0x01: "Content Identification",
    0x10: "Program Start",
    0x11: "Program End",
    0x12: "Program Early Termination",
    0x13: "Program Breakaway",
    0x14: "Program Resumption",
    0x15: "Program Runover Planned",
    0x16: "Program RunoverUnplanned",
    0x17: "Program Overlap Start",
    0x18: "Program Blackout Override",
    0x19: "Program Start ??? In Progress",
    0x20: "Chapter Start",
    0x21: "Chapter End",
    0x22: "Break Start",
    0x23: "Break End",
    0x24: "Opening Credit Start",
    0x25: "Opening Credit End",
    0x26: "Closing Credit Start",
    0x27: "Closing Credit End",
    0x30: "Provider Advertisement Start",
    0x31: "Provider Advertisement End",
    0x32: "Distributor Advertisement Start",
    0x33: "Distributor Advertisement End",
    0x34: "Provider Placement Opportunity Start",
    0x35: "Provider Placement Opportunity End",
    0x36: "Distributor Placement Opportunity Start",
    0x37: "Distributor Placement Opportunity End",
    0x38: "Provider Overlay Placement Opportunity Start",
    0x39: "Provider Overlay Placement Opportunity End",
    0x3A: "Distributor Overlay Placement Opportunity Start",
    0x3B: "Distributor Overlay Placement Opportunity End",
    0x40: "Unscheduled Event Start",
    0x41: "Unscheduled Event End",
    0x50: "Network Start",
    0x51: "Network End",
}


class SegmentationDescriptor(SpliceDescriptor):
    """
    Table 19 - segmentation_descriptor()
    """

    def __init__(self, tag):
        super().__init__(tag)
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

    def decode(self, bitbin):
        """
        decode a segmentation descriptor
        """
        self.parse_id(bitbin)
        self.segmentation_event_id = bitbin.ashex(32)  # 4 bytes
        self.segmentation_event_cancel_indicator = bitbin.asflag(1)
        bitbin.forward(7)  # 1 byte
        if not self.segmentation_event_cancel_indicator:
            self._set_flags(bitbin)  # 1 byte
            if not self.program_segmentation_flag:
                self._set_components(bitbin)
            self._set_segmentation(bitbin)

    def _set_components(self, bitbin):
        self.component_count = c_c = bitbin.asint(8)  # 1 byte
        while c_c:  # 6 bytes each
            c_c -= 1
            comp = {}
            comp["component_tag"] = bitbin.asint(8)
            bitbin.forward(7)
            comp["pts_offset"] = bitbin.as90k(33)
            self.components.append(comp)

    def _set_flags(self, bitbin):  # 1 byte for set flags
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

    def _set_segmentation(self, bitbin):
        if self.segmentation_duration_flag:
            self.segmentation_duration = bitbin.as90k(40)  # 5 bytes
        self.segmentation_upid_type = bitbin.asint(8)  # 1 byte
        self.segmentation_upid_length = bitbin.asint(8)  # 1 byte
        self.segmentation_upid = self._set_segmentation_upid(
            bitbin, self.segmentation_upid_type, self.segmentation_upid_length
        )
        self.segmentation_type_id = bitbin.asint(8)  # 1 byte
        if self.segmentation_type_id in table22.keys():
            self.segmentation_message = table22[self.segmentation_type_id]
            self._set_segments(bitbin)
        bitbin = None

    def _set_segmentation_upid(self, bitbin, upid_type, upid_length):
        upid_map = {
            0x02: ["Deprecated", self._uri],
            0x03: ["Ad ID", self._uri],
            0x04: ["UMID", self._umid],
            0x05: ["ISAN", self._isan],
            0x06: ["ISAN", self._isan],
            0x07: ["TID", self._uri],
            0x08: ["AiringID", self._air_id],
            0x09: ["ADI", self._uri],
            0x0A: ["EIDR", self._eidr],
            0x0B: ["ATSC", self._atsc],
            0x0C: ["MPU", self._mpu],
            0x0D: ["MID", self._mid],
            0x0E: ["ADS Info", self._uri],
            0x0F: ["URI", self._uri],
        }
        upid_id = ""
        if upid_type in upid_map.keys():
            upid_id = upid_map[upid_type][1](bitbin, upid_length)
            if upid_type != 0x09:
                return f"{upid_map[upid_type][0]}:{upid_id}"
        return upid_id

    def _set_segments(self, bitbin):
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
            segmentation_upid = self._set_segmentation_upid(
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
