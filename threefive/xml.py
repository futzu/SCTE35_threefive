"""
xml.py  The Node class for converting to xml,
        The XmlParser class for parsing an xml string for SCTE-35 data.
        and several helper functions
"""


def t2s(v):
    """
    _t2s converts
    90k ticks to seconds and
    rounds to six decimal places
    """
    return round(v / 90000.0, 6)


def un_camel(k):
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


def iter_attrs(attrs):
    """
    iter_attrs normalizes xml attributes
    and adds them to the stuff dict.
    """
    conv = {un_camel(k): un_xml(v) for k, v in attrs.items()}
    pts_vars = ["pts_time", "pts_adjustment", "duration", "segmentation_duration"]
    conv = {k: (t2s(v) if k in pts_vars else v) for k, v in conv.items()}
    return conv


def val2xml(val):
    """
    val2xmlconvert val for xml
    """
    if isinstance(val, bool):
        return str(val).lower()
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val,str):
        if val.lower()[:2]=="0x":
            return str(int(val,16))
    return escape(val)


def key2xml(string):
    """
    key2xml convert name to camel case
    """
    new_string = string
    if "_" in string:
        new_string = string.title().replace("_", "")
    return new_string[0].lower() + new_string[1:]


def mk_xml_attrs(attrs):
    """
    mk_xml_attrs converts a dict into
    a dict of xml friendly keys and values
    """
    return "".join([f' {key2xml(k)}="{val2xml(v)}"' for k, v in attrs.items()])


special_char_map = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
}


def escape(val):
    """
    escape characters that are not valid in xml
    replaces characters matching special_char_map keys with corresponding value
    """
    if val is not None:
        for key, value in special_char_map.items():
            val = val.replace(key, value)
    return val


def unescape(val):
    """
    unescapes characters that are not valid in xml
    replaces characters matching special_char_map values with corresponding key
    """
    if val is not None:
        for key, value in special_char_map.items():
            val = val.replace(value, key)
    return val


class Node:
    """
    The Node class is to create an xml node.

    An instance of Node has:

        name :      <name> </name>
        attrs :     <name attrs[k]="attrs[v]">
        value  :    <name>value</name>
        children :  <name><children[0]></children[0]</name>
        depth:      tab depth for printing (automatically set)

    Use like this:

        from threefive.xml import Node

        ts = Node('TimeSignal')
        st = Node('SpliceTime',attrs={'pts_time':3442857000})
        ts.add_child(st)
        print(ts)
    """

    def __init__(self, name, value=None, attrs={}, ns=None):
        self.name = name
        if ns:
            self.name = ":".join((ns, name))
        self.value = escape(value)
        self.attrs = attrs
        self.children = []
        self.depth = 0

    def __repr__(self):
        return self.mk()

    def set_depth(self):
        """
        set_depth is used to format
        tabs in output
        """
        for child in self.children:
            child.depth = self.depth + 1

    def get_indent(self):
        """
        get_indent returns a string of spaces the required depth for a node
        """
        tab = "   "
        return tab * self.depth

    def mk(self, obj=None):
        """
        mk makes the node obj,
        and it's children into
        an xml representation.
        """
        if obj is None:
            obj = self
        obj.set_depth()
        ndent = obj.get_indent()
        if isinstance(obj, Comment):
            return obj.mk(obj)
        new_attrs = mk_xml_attrs(obj.attrs)
        rendrd = f"{ndent}<{obj.name}{new_attrs}>"
        if obj.value:
            return f"{rendrd}{obj.value}</{obj.name}>\n"
        rendrd = f"{rendrd}\n"
        for child in obj.children:
            rendrd += obj.mk(child)
        if obj.children:
            return f"{rendrd}{ndent}</{obj.name}>\n"
        return rendrd.replace(">", "/>")

    def add_child(self, child):
        """
        add_child adds a child node
        """
        self.children.append(child)

    def add_comment(self, comment):
        """
        add_comment add a Comment node
        """
        self.add_child(Comment(comment))


class Comment(Node):
    """
    The Comment class is to create a Node representing a xml comment.

    An instance of Comment has:

        name :      <!-- name -->
        depth:      tab depth for printing (automatically set)

    Since Comment is a Node, it also has attrs, value and children but
    these are ignored. cf etree.Comment
    Use like this:

        from threefive.xml import Comment, Node

        n = Node('root')
        c = Comment('my first comment')

        n.add_child(c)
        print(n)

    See also Node.add_comment:
    """
    def mk(self, obj=None):
        if obj is None:
            obj = self
        obj.set_depth()
        return f"{obj.get_indent()}<!-- {obj.name} -->\n"


class XmlParser:
    """
    XmlParser is for parsing
    a SCTE-35 Cue from  xml.
    """

    DESCRIPTORS = [
        "AvailDescriptor",
        "DTMFDescriptor",
        "SegmentationDescriptor",
        "TimeDescriptor",
    ]

    def __init__(self):
        self.active = None
        self.node_list = []

    def chk_node_list(self, node):
        """
        chk_node_list is used to track open xml nodes
        """
        if self.active in self.node_list:
            self.node_list.remove(self.active)
        elif node[-2] != "/":
            self.node_list.append(self.active)

    def mk_value(self, value, stuff):
        """
        mk_value, if the xml node has a value, write it to self.stuff

        <name>value</name>

        """
        if value not in [None, ""]:
            stuff[self.active][un_camel(self.active)] = unescape(value)
        return stuff

    def mk_active(self, node):
        """
        mk_active sets self.active to the current node name.
        """
        name = node[1:].split(" ", 1)[0].split(">", 1)[0].split(":")[-1]
        self.active = name.replace("/", "").replace(">", "")

    def mk_attrs(self, node):
        """
        mk_attrs parses the current node for attributes
        and stores them in self.stuff[self.active]
        """
        node= node.replace("='",'="').replace("' ",'" ')
        attrs = [x for x in node.split(" ") if "=" in x]
        parsed = {
            x.split('="')[0]: unescape(x.split('="')[1].split('"')[0])
            for x in attrs
        }
        it = iter_attrs(parsed)
        return it

    def parse(self, exemel, descriptor_parse=False):
        """
        parse parses an xml string for a SCTE-35 Cue.
        """
        stuff = {"descriptors": []}
        data = exemel.replace("\n", "").strip()
        while ">" in data:
            self.mk_active(data)
            data, stuff = self._parse_nodes(data, stuff, descriptor_parse)
        return stuff

    def _parse_nodes(self, data, stuff, descriptor_parse=False):
        if self.active in self.DESCRIPTORS and not descriptor_parse:
            data, stuff = self._parse_descriptor(data, stuff)
        else:
            data, stuff = self._parse_most(data, stuff)
        return data, stuff

    def _parse_most(self, data, stuff):
        """
        parse_most parse everything except descriptor nodes
        """
        rgator = data.index(">")
        this_node = data[: rgator + 1]
        self.chk_node_list(this_node)
        attrs = self.mk_attrs(this_node)
        if self.active not in stuff:
            stuff[self.active] = attrs
        data = data[rgator + 1 :]
        if "<" in data:
            lgator = data.index("<")
            value = data[:lgator].strip()
            stuff = self.mk_value(value, stuff)
            data = data[lgator:]
        return data, stuff

    def _parse_descriptor(self, data, stuff):
        """
        mk_descriptor slices off an entire
        descriptor xml node from data to parse.
        """
        sub_data = ""
        tag = data[1:].split(" ", 1)[0]
        try:
            sub_data = data[: data.index(f"</{tag}>") + len(tag) + 1]
        except:
            sub_data = data[: data.index("/>") + 2]
        data = data.replace(sub_data, "")
        stuff["descriptors"].append(self.parse(sub_data, descriptor_parse=True))
        return data, stuff
