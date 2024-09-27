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
    return round(v/90000.0, 6)


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
    if v.isdigit(): return int(v)
    if v.replace(".", "").isdigit():    return float(v)
    if v in ["false", "False"]: return False
    if v in ["true", "True"]:   return True
    return v


def iter_xml_attrs(attrs):
    """
    iter_attrs normalizes xml attributes
    and adds them to the stuff dict.
    """
    conv = {camel(k): un_xml(v) for k, v in attrs.items()}
    pts_vars = ["pts_time", "pts_adjustment", "duration", "segmentation_duration"]
    conv = {k: (t2s(v) if k in pts_vars else v) for k, v in conv.items()}
    return conv


def val2xml(val):
    """
    val2xmlconvert val for xml
    """
    if isinstance(val, bool):   return str(val).lower()
    if isinstance(val, (int, float)):   return str(val)
    return val


def key2xml(string):
    """
    key2xml convert name to camel case
    """
    new_string = string
    if "_" in string:   new_string = string.title().replace("_", "")
    return new_string[0].lower() + new_string[1:]


def mk_xml_attrs(attrs):
    """
    mk_attrs converts a dict into
    a dict of xml friendly keys and values
    """
    return "".join([f' {key2xml(k)}="{val2xml(v)}"' for k, v in attrs.items()])


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

    def __init__(self, name, value=None, attrs={}):
        self.name = name
        self.value = value
        self.attrs = attrs
        self.children = []
        self.depth = None

    def __repr__(self):
        return self.mk()

    def set_depth(self):
        """
        set_depth is used to format
        tabs in output
        """
        if not self.depth:  self.depth = 0
        for child in self.children: child.depth = self.depth + 1

    def mk(self, obj=None):
        """
        mk makes the node obj,
        and it's children into
        an xml representation.
        """
        if obj is None: obj=self
        obj.set_depth()
        ndent = "   " * obj.depth
        new_attrs = mk_xml_attrs(obj.attrs)
        rendrd = f"{ndent}<{obj.name}{new_attrs}>"
        if obj.value:   return f"{rendrd}{obj.value}</{obj.name}>\n"
        rendrd = f"{rendrd}\n"
        for child in obj.children:  rendrd += obj.mk(child)
        if obj.children:    return f"{rendrd}{ndent}</{obj.name}>\n"
        return rendrd.replace(">", "/>")

    def add_child(self, child):
        """
        add_child adds a child node
        """
        self.children.append(child)



class XmlParser:
    """
    XmlParser is for parsing
    a SCTE-35 Cue from  xml.
    """
    def __init__(self):
        self.active=None
        self.stuff={}
        self.node_list=[]


    def chk_node_list(self,node):
        """
        chk_node_list is used to track open xml nodes
        """
        if self.active in self.node_list:
            self.node_list.remove(self.active)
        elif node[-2]!='/':
            self.node_list.append(self.active)

    def mk_value(self,value):
        """
        mk_value, if the xml node has a value, write it to self.stuff

        <name>value</name>

        """
        if value not in [None,'']:
            self.stuff[self.active][camel(self.active)]=value

    def mk_active(self,node):
        """
        mk_active sets self.active to the current node name.
        """
        name =node[1:].split(' ',1)[0].split(':')[-1]
        self.active=name.replace('/','').replace('>','')

    def mk_attrs(self,node):
        """
        mk_attrs parses the current node for attributes
        and stores them in self.stuff[self.active]
        """
        if '<!--' not in node:
            attrs = [x for x in node.split(' ') if '=' in x]
            parsed ={x.split('="')[0]:x.split('="')[1].split('"')[0] for x in attrs}
            fixed=  iter_xml_attrs(parsed)
            if self.active not in self.stuff: self.stuff[self.active]=fixed


    def parse(self,exemel):
        """
        parse parses an xml string for a SCTE-35 Cue.
        """
        data = exemel.replace('\n','')
        while '>' in  data:
            if '>' in data:
                rgator=data.index('>')
                this_node=data[:rgator+1]
                self.mk_active(this_node)
                self.chk_node_list(this_node)
                self.mk_attrs(this_node)
                data = data[rgator+1:]
            if '<' in data:
                lgator = data.index('<')
                value= data[:lgator].strip()
                self.mk_value(value)
                data=data[lgator:]
        return self.stuff
