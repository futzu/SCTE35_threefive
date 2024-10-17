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
### Usage:
```sh
pypy3 mpdp.py https://demo.unified-streaming.com/k8s/live/stable/scte35-no-splicing.isml/.mpd

```
### Output:

```js

<!--Event #1-->
<Event 
        presentationTime="1729124893440" 
        duration="38400" 
        id="14295014"> 
        <Signal 
          xmlns="http://www.scte.org/schemas/35/2016"> 
          <Binary>/DAgAAAAAAAAAP/wDwUA2h/mf//+ADS8AMAAAAAAAORhJCQ=</Binary> 
        </Signal> 
      </Event>

<!--The threefive.Cue instance #1 -->

{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 32,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x00",
        "tier": "0x0fff",
        "splice_command_length": 15,
        "splice_command_type": 5,
        "descriptor_loop_length": 0,
        "crc": "0xe4612424"
    },
    "command": {
        "command_length": 15,
        "command_type": 5,
        "name": "Splice Insert",
        "break_auto_return": true,
        "break_duration": 38.4,
        "splice_event_id": 14295014,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": true,
        "event_id_compliance_flag": true,
        "unique_program_id": 49152,
        "avail_num": 0,
        "avails_expected": 0
    },
    "descriptors": []
}

<!-- The threefive.Cue instance converted back to xml #1 -->

<SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <SpliceInsert spliceEventId="14295014" spliceEventCancelIndicator="false" spliceImmediateFlag="true" eventIdComplianceFlag="true" availNum="0" availsExpected="0" outOfNetworkIndicator="true" uniqueProgramId="49152">
      <BreakDuration autoReturn="true" duration="3456000"/>
   </SpliceInsert>
</SpliceInfoSection>


<!--Event #2-->
<Event 
        presentationTime="1729125014400" 
        duration="38400" 
        id="14295015"> 
        <Signal 
          xmlns="http://www.scte.org/schemas/35/2016"> 
          <Binary>/DAgAAAAAAAAAP/wDwUA2h/nf//+ADS8AMAAAAAAAORhJCQ=</Binary> 
        </Signal> 
      </Event>

<!--The threefive.Cue instance #2 -->

{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 32,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x00",
        "tier": "0x0fff",
        "splice_command_length": 15,
        "splice_command_type": 5,
        "descriptor_loop_length": 0,
        "crc": "0xe4612424"
    },
    "command": {
        "command_length": 15,
        "command_type": 5,
        "name": "Splice Insert",
        "break_auto_return": true,
        "break_duration": 38.4,
        "splice_event_id": 14295015,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": true,
        "event_id_compliance_flag": true,
        "unique_program_id": 49152,
        "avail_num": 0,
        "avails_expected": 0
    },
    "descriptors": []
}

<!-- The threefive.Cue instance converted back to xml #2 -->

<SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <SpliceInsert spliceEventId="14295015" spliceEventCancelIndicator="false" spliceImmediateFlag="true" eventIdComplianceFlag="true" availNum="0" availsExpected="0" outOfNetworkIndicator="true" uniqueProgramId="49152">
      <BreakDuration autoReturn="true" duration="3456000"/>
   </SpliceInsert>
</SpliceInfoSection>

...

```

