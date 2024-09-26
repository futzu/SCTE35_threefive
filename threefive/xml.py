"""
xml.py  The Node class for converting to xml
and several conversion functions for names and values.
"""

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

        ts = Node('scte35:TimeSignal')
        st = Node('scte35:SpliceTime',attrs={'pts_time':3442857000})
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
        mk makes the node obj
        and it's children into xml.
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
