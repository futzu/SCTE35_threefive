from .tables import table22


class Splice_Descriptor:
    """
    The first six bytes of all descriptors:
            splice_descriptor_tag    8 uimsbf
            descriptor_length        8 uimsbf
            identifier              32 uimsbf
    """

    def __init__(self, bitbin, tag):
        self.name = "Unknown Descriptor"
        self.splice_descriptor_tag = tag
        self.descriptor_length = bitbin.asint(8)
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


class Segmentation_Descriptor(Splice_Descriptor):
    """
    Table 19 - segmentation_descriptor()
    """

    def __init__(self, bitbin, tag):
        if not super().__init__(bitbin, tag):
            return False
        self.name = "Segmentation Descriptor"
        self.segmentation_event_id = bitbin.ashex(32)
        self.segmentation_event_cancel_indicator = bitbin.asflag(1)
        bitbin.forward(7)
        if not self.segmentation_event_cancel_indicator:
            self.program_segmentation_flag = bitbin.asflag(1)
            self.segmentation_duration_flag = bitbin.asflag(1)
            self.delivery_not_restricted_flag = bitbin.asflag(1)
            if not self.delivery_not_restricted_flag:
                self.web_delivery_allowed_flag = bitbin.asflag(1)
                self.no_regional_blackout_flag = bitbin.asflag(1)
                self.archive_allowed_flag = bitbin.asflag(1)
                self.device_restrictions = bitbin.ashex(2)
            else:
                bitbin.forward(5)
            if not self.program_segmentation_flag:
                self.component_count = bitbin.asint(8)
                self.components = []
                for i in range(0, self.component_count):
                    comp = {}
                    comp["component_tag"] = bitbin.asint(8)
                    bitbin.forward(7)
                    comp["pts_offset"] = bitbin.as90k(33)
                    self.components.append(comp)
            if self.segmentation_duration_flag:
                self.segmentation_duration = bitbin.as90k(40)
            self.segmentation_upid_type = bitbin.asint(8)
            if self.segmentation_upid_type == 8:
                self.segmentation_upid_length = bitbin.asint(8)
                self.turner_identifier = bitbin.ashex(64)
            self.segmentation_type_id = bitbin.asint(8)
            if self.segmentation_type_id in table22.keys():
                self.segmentation_message = table22[self.segmentation_type_id][0]
            if self.segmentation_type_id == 0:
                self.segment_num = 0
                self.segments_expected = 0
            else:
                self.segment_num = bitbin.asint(8)
                self.segments_expected = bitbin.asint(8)
            if self.segmentation_type_id in [0x34, 0x36]:
                self.sub_segment_num = bitbin.asint(8)
                self.sub_segments_expected = bitbin.asint(8)


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
