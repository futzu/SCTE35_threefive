"""
dash.py converting dash SCTE-35 to a threefive.Cue instance.
"""
import json
import xml.parsers.expat
from .cue import Cue
from .commands import SpliceInsert, TimeSignal
from .descriptors import SegmentationDescriptor
from .segmentation import table20


def _convert_k(k):
    """
    _convert_k changes camel case xml names
    to underscore_format names.
    """
    k = "".join([f"_{i.lower()}" if i.isupper() else i for i in k])
    return (k, k[1:])[k[0] == "_"]


def _convert_v(v):
    """
    _convert xml values
    to ints, floats and booleans
    """
    if v.isdigit():
        return int(v)
    if v.replace(".", "").isdigit():
        return float(v)
    if v in ["false", "False"]:
        return False
    if v in ["true", "True"]:
        return True
    return v


def _ticks2seconds(v):
    """
    _ticks2seconds converts
    90k ticks to seconds and
    rounds to six decimal places
    """
    v /= 90000.0
    return round(v, 6)


class DashSCTE35:
    """
    DashSCTE35 parses DASH Events for SCTE-35.
    Supports xml and binary formats.
    """

    def __init__(self):
        self.active = None
        self.stuff = {}
        self.child_path =[]
        

    def _iter_attrs(self, attrs):
        """
        iter_attrs normalizes xml attributes
        and adds them to the stuff dict.
        """
        conv = {_convert_k(k): _convert_v(v) for k, v in attrs.items()}
        pts_vars = ["pts_time", "pts_adjustment", "duration", "segmentation_duration"]
        conv = {k: (_ticks2seconds(v) if k in pts_vars else v) for k, v in conv.items()}
        self.stuff[self.active].update(conv)

    def start_element(self, name, attrs):
        """
        start_element for expat
        """
        self.child_path.append(name)
        print('->'.join(self.child_path))
        self.active = name.split(":")[-1]
        self.stuff[self.active] = {}
        self._iter_attrs(attrs)

    def end_element(self,name):
        self.child_path.pop()

    def char_data(self, data):
        """
        char_data CharacterDataHandler for expat
        """
        data=data.replace(' ','').replace('\n','')
        if data:
            self.stuff[self.active][_convert_k(self.active)] = data

    def _build_info_section(self, cue):
        """
        build_info_section loads a converted
        dash info section dict into a cue.
        """
        self.stuff["SpliceInfoSection"]["tier"] = hex(
            self.stuff["SpliceInfoSection"]["tier"]
        )
        cue.info_section.load(self.stuff["SpliceInfoSection"])
        return cue

    def _build_splice_insert(self):
        """
        build_splice_insert creates a threefive.SpliceInsert instance
        loads converted dash SpliceInsert, SpliceTime, and BreakDuration
        and adds the vars that are not included in dash.
        """
        cmd = SpliceInsert()
        cmd.load(self.stuff["SpliceInsert"])
        cmd.event_id_compliance_flag = True
        cmd.program_splice_flag = False
        if "SpliceTime" in self.stuff:
            cmd.load(self.stuff["SpliceTime"])
            cmd.program_splice_flag = True
            cmd.time_specified_flag = True
        if "BreakDuration" in self.stuff:
            cmd.load(self.stuff["BreakDuration"])
            cmd.break_duration = cmd.duration
            cmd.duration_flag = True
            cmd.break_auto_return = cmd.auto_return
        cmd.avail_expected = bool(cmd.avails_expected)
        return cmd

    def _build_time_signal(self):
        """
        build_time_signal creates threefive.TimeSignal instance
        and loads converted data from Dash.
        """
        cmd = TimeSignal()
        if "SpliceTime" in self.stuff:
            cmd.load(self.stuff['SpliceTime'])
            cmd.time_specified_flag = True
        return cmd

    def _build_splice_command(self, cue):
        """
        build_splice_command determines whether to build
        a SpliceInsert or TimeSignal and builds it.
        """
        cue.command = (self._build_splice_insert, self._build_time_signal)["TimeSignal" in self.stuff]()
        return cue

    def _chk_sub_segments(self, dscptr):
        """
        chk_sub_segments sets sub_segment vars if not present
        """
        if dscptr.segmentation_type_id in [
            0x30,
            0x32,
            0x34,
            0x36,
            0x38,
            0x3A,
            0x44,
            0x46,
        ]:
            if not dscptr.sub_segment_num:
                dscptr.sub_segment_num = 0
                dscptr.sub_segments_expected = 0

    def _build_descriptor(self, cue):
        if "SegmentationDescriptor" in self.stuff:
            dscptr =SegmentationDescriptor()
            dscptr.load(self.stuff["SegmentationDescriptor"])
            dscptr.segmentation_event_id_compliance_indicator = True
            dscptr.program_segmentation_flag = True
            if hasattr(dscptr, "segmentation_duration"):
                dscptr.segmentation_duration_flag = True
            dscptr.delivery_not_restricted_flag = True
            if "DeliveryRestrictions" in self.stuff:
                dscptr.delivery_not_restricted_flag = False
            dscptr.load(self.stuff["DeliveryRestrictions"])
            dscptr.segmentation_event_id = hex(dscptr.segmentation_event_id)
            dscptr.device_restrictions = table20[dscptr.device_restrictions]
            dscptr.segmentation_upid_length = 0
            dscptr.segmentation_upid_type = 0
            if "SegmentationUpid" in self.stuff:
                dscptr.load(self.stuff["SegmentationUpid"])
            self._chk_sub_segments(dscptr)
            cue.descriptors.append(dscptr)
        return cue

    def _build_cue(self):
        """
        build_cue takes the data put into the stuff dict
        and builds a threefive.Cue instance
        """

        if "Binary" in self.stuff:
            cue = Cue(self.stuff["Binary"]["binary"])
            cue.decode()
        else:
            cue = Cue()
            cue = self._build_info_section(cue)
            cue = self._build_splice_command(cue)
            cue.info_section.splice_command_type =cue.command.command_type
            cue = self._build_descriptor(cue)
            cue.encode()
        return cue

    def parse(self, exemel):
        """
        do creates a an expat Parser
        to parse  the exemel and
        returns a threefive.Cue instance..
        """
        self.stuff = {}
        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = self.start_element
        p.EndElementHandler = self.end_element
        p.CharacterDataHandler = self.char_data
        p.Parse(exemel, 1)
        print(json.dumps(self.stuff, indent=4))
        new_cue = self._build_cue()
        #new_cue.show()
        return new_cue




def dash2cue(exemel):
    """
    dash2cue converts a dash event to a threefive.Cue instance
    and returns the cue and xml converted to json
    """
    ds = DashSCTE35()
    cue = ds.parse(exemel)
    parsed = ds.stuff
    return cue,parsed

