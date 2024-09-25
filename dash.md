# Dash SCTE-35 Parser Preview
### Expected in release v2.4.71
### Everything here may or may not change.
# From Xml
  * expat xml parsing
  *  Dash SCTE-35 data is coverted to threefive.Cue instances.
---
### Usage:

* <s>`threefive.DashSCTE35` is the class </s>
*  <s> the method is `parse_mpd` </s>

* Use a __Cue__ instance and pass in the Xml via the  __load__ method.
```py3
  from threefive import Cue
  cue=Cue()           # Create a Cue instance
  cue.load(dash_xml)  # load xml
```
---

### Example #1     
* `"u23rn:scte:scte35:2013:xml"`
* Text Xml of SCTE-35 SpliceInfosection converted to a Cue instance.

<details><summary> Xml </summary>


```xml
some_xml = """<Event duration="5310000">
            <scte35:SpliceInfoSection protocolVersion="0" ptsAdjustment="183003" tier="4095">
            <scte35:TimeSignal>
                <scte35:SpliceTime ptsTime="3442857000"/>
            </scte35:TimeSignal>
            <scte35:SegmentationDescriptor segmentationEventId="1414668"
                segmentationEventCancelIndicator="false" segmentationDuration="8100000"
                segmentationTypeId="52" segmentNum="0" segmentsExpected="0">
            <scte35:DeliveryRestrictions webDeliveryAllowedFlag="false"
                noRegionalBlackoutFlag="false" archiveAllowedFlag="false"
                deviceRestrictions="3"/>
            <scte35:SegmentationUpid segmentationUpidType="8"
                segmentationUpidLength="8">0x2df3aad7</scte35:SegmentationUpid>
            </scte35:SegmentationDescriptor>
            </scte35:SpliceInfoSection>
        </Event>
        """
```

</details>






 
<details><summary>Code</summary>

```py3
from threefive import Cue

cue = Cue()
cue.load(some_xml)
```


</details>




<details><summary>The Cue after calling load()</summary>


```json
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 54,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 2.033367,
        "cw_index": "0x0",
        "tier": "0xfff",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 32,
        "crc": "0x8926251d"
    },
    "command": {
        "command_length": 5,
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 38253.966667
    },
    "descriptors": [
        {
            "tag": 2,
            "descriptor_length": 30,
            "name": "Segmentation Descriptor",
            "identifier": "CUEI",
            "segmentation_event_id": "0x15960c",
            "segmentation_event_cancel_indicator": false,
            "segmentation_event_id_compliance_indicator": true,
            "program_segmentation_flag": true,
            "segmentation_duration_flag": true,
            "delivery_not_restricted_flag": false,
            "web_delivery_allowed_flag": false,
            "no_regional_blackout_flag": false,
            "archive_allowed_flag": false,
            "device_restrictions": "No Restrictions",
            "segmentation_duration": 90.0,
            "segmentation_upid_type": 8,
            "segmentation_upid_length": 8,
            "segmentation_upid": "0x2df3aad7",
            "segmentation_type_id": 52,
            "segment_num": 0,
            "segments_expected": 0,
            "sub_segment_num": 0,
            "sub_segments_expected": 0
        }
    ]
}
a@fu:~$ 
```

</details>


---


### Example #2 
* `"urn:scte:scte35:2014:xml+bin"`
* SCTE-35 Base64 in Xml converted to a threefive.Cue instance.


<details><summary> Xml </summary>


```xml
some_xml = """<Event
        presentationTime="1725944855040"
        duration="38400"
        id="14268724">
        <Signal
          xmlns="http://www.scte.org/schemas/35/2016">
          <Binary>/DAgAAAAAAAAAP/wDwUA2bk0f//+ADS8AMAAAAAAAORhJCQ=</Binary>
        </Signal>
      </Event>"""

```

</details>






 
<details><summary>Code</summary>

```py3
from threefive import Cue

cue = Cue()
cue.load(some_xml)
```


</details>




<details><summary>The Cue after calling load()</summary>


```json
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
        "splice_event_id": 14268724,
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

```

</details>

---
# To Xml

### Usage:
```py3

from threefive import Cue

cue=Cue(data) # Data can be Base64, Bytes, Hex, Integer
#OR
cue=Cue.load(data             # JSON, a dict, or xml can be loaded

cue.decode()
x = cue.xml() # returns a threefive.Node instance
x.show()   # displays xml
```

### Example 3
* `"u23rn:scte:scte35:2013:xml"`
* Converting a Cue instance to xml for Dash
<details><summary> Base64 </summary>


```js
/DA2AAHOR/nwAAAABQb+PnGRBwAgAh5DVUVJSAAAbH/PAAE1ODcICAAAAAAt86rXNAAAAACwnuYL
```

</details>


 
<details><summary>Code</summary>

```py3
from threefive import Cue
cue=Cue('/DA2AAHOR/nwAAAABQb+PnGRBwAgAh5DVUVJSAAAbH/PAAE1ODcICAAAAAAt86rXNAAAAACwnuYL')
cue.decode()
x = cue.xml() # returns a threefive.Node instance
x.show()   # displays xml
```

</details>


<details><summary>xml Output</summary>


```xml
<scte35:SpliceInfoSection ptsAdjustment="0" protocolVersion="None" sapType="None" sapDetails="None" tier="None">
        <scte35:TimeSignal>
                <scte35:SpliceTime ptsTime="11640.3343"/>
        </scte35:TimeSignal>
        <scte35:SegmentationDescriptor segmentationEventId="0x4800006c" segmentationEventCancelIndicator="false" segmentationEventIdComplianceIndicator="true" segmentationDuration="225.166833" segmentNum="0" segmentsExpected="0" self.SubSegmentNum="0" subSegmentsExpected="0">
                <DeliveryRestrictions webDeliveryAllowedFlag="true" noRegionalBlackoutFlag="true" archiveAllowedFlag="true" deviceRestrictions="No Restrictions"/>
                <segmentation_upid segmentationUpidType="8" segmentationUpidTypeName="AiringID" segmentationUpid="0x2df3aad7"/>
        </scte35:SegmentationDescriptor>
</scte35:SpliceInfoSection>

```

</details>

---
