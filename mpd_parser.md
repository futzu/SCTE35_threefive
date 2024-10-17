# Minimal Dash SCTE-35 mpd parser. 

```py3
#!/usr/bin/env python3

"""
mpdp.py minimal SCTE-35 mpd parser. 

"""


import sys
from new_reader import reader
from threefive.xml import XmlParser
from threefive import Cue


def mk_event(exemel, event_num):
    """
    mk_event split out Event nodes
    """
    event_num += 1
    ridx = exemel.index("</Event>")
    lidx = exemel.index("<Event ")
    event = exemel[lidx : ridx + 8]
    print(f"\n<!--Event #{event_num}-->\n{event}")
    exemel = exemel[ridx + 8 :]
    return event, exemel,event_num


def mk_scte35(event):
    """
    mk_scte35 parse xml into a dict
    """
    xp = XmlParser()
    scte35 = xp.parse(event)
    return scte35


def show_scte35(cue,event_num):
    """
    show_scte35
    """
    if cue:
        print(f"\n<!--The threefive.Cue instance #{event_num}-->\n")
        cue.show()
        print(
            f"\n<!--The threefive.Cue instance converted back to xml #{event_num}-->\n"
        )
        print(cue.xml())


def chk_scte35(scte35,event_num):
    """
    chk_scte35 check for SCTE-35 xml
    and SCTE-35 xml+bin
    """
    cue = False
    if "SpliceInfoSection" in scte35:
        cue = Cue()
        cue.load(scte35)  # <-- cue.load() is used with xml.
        cue.encode()
    if "Binary" in scte35:
        cue = Cue(
            scte35["Binary"]["binary"]
        )  # init with the data for Base64 encoded SCTE-35
        cue.decode()
    show_scte35(cue, event_num)


def parse_mpd(mpd):
    """
    parse_mpd parse an mpd
    """
    event_num =0
    exemel = reader(mpd).read().decode().replace("\n", " \n")
    while "</Event>" in exemel:
        event, exemel, event_num = mk_event(exemel, event_num)
        scte35 = mk_scte35(event)
        chk_scte35(scte35,event_num)


if __name__ == "__main__":
    args = sys.argv[1:]
    for arg in args:
        parse_mpd(arg)



```
