"""
dash.py converting dash SCTE-35 to a threefive.Cue instance.
"""
import json
import xml.parsers.expat
from new_reader import reader
from .stuff import print2

def t2s(v):
    """
    _t2s converts
    90k ticks to seconds and
    rounds to six decimal places
    """
    v = (un_xml(v) / 90000.0)
    return round(v, 6)


def camel(k):
    """
    camel changes camel case xml names
    to underscore_format names.
    """
    k = "".join([f"_{i.lower()}" if i.isupper() else i for i in k])
    return (k, k[1:])[k[0] == "_"]


def un_xml(v):
    """
    un_xml converts an xml value
    to ints, floats and booleans.
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


class DashSCTE35:
    """
    DashSCTE35 parses DASH Events for SCTE-35.
    Supports xml and binary formats.
    """

    def __init__(self):
        self.active = None
        self.stuff = {}
        self.child_path =[]
        self.cue_data = []

    def _iter_attrs(self, attrs):
        """
        iter_attrs normalizes xml attributes
        and adds them to the stuff dict.
        """
        pts_vars = ["pts_time", "pts_adjustment", "duration", "segmentation_duration"]
        conv = {camel(k): (t2s(v) if k in pts_vars else un_xml(v) )for k, v in attrs.items()}
        self.stuff[self.active].update(conv)

    def start_element(self, name, attrs):
        """
        start_element for expat
        """
        self.child_path.append(name)
        print2('->'.join(self.child_path))
        self.active = name.split(":")[-1]
        self.stuff[self.active] = {}
        self._iter_attrs(attrs)

    def end_element(self,name):
        """
        end-element for expat
        """
        if name in ["Binary" , "scte35:SpliceInfoSection"] :
            stuff = self.stuff
            print(json.dumps(stuff, indent=4))
            self.cue_data.append(stuff)
            self.stuff = {}
        self.child_path.pop()

    def char_data(self, data):
        """
        char_data CharacterDataHandler for expat
        """
        data=data.replace(' ','').replace('\n','')
        if data:
            self.stuff[self.active][camel(self.active)] = data


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
        print2(json.dumps(self.stuff, indent=4))
        return self.cue_data

    def parse_mpd(self,mpd):
        """
        parse_mpd parses an mpd file
        """
        with reader(mpd) as mpd_fd:
            return self.parse(mpd_fd.read().decode())

def dash2cues(exemel):
    """
    dash2cues converts a dash events to threefive.Cue instances
    and returns the cues.
    """
    ds = DashSCTE35()
    cues = ds.parse(exemel)
    return cues
