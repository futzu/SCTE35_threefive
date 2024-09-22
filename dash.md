# Dash SCTE-35 Parser Preview
### Expected in release v2.4.71
### Everything here may or may not change.

* expat xml parsing
*  Dash SCTE-35 data is coverted to threefive.Cue instances.
* [source](https://github.com/futzu/SCTE35_threefive/blob/master/threefive/dash.py)
---
### Usage:
* <s>`threefive.DashSCTE35` is the class </s>
*  <s> the method is `parse_mpd` </s>

* Use a __Cue__ instance and call the __load__ method
    * ( Cue.load loads xml,json, and python dicts)
 
* Code

```py3
from threefive import Cue

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

cue = Cue()
cue.load(some_xml)
```

* Run

```js
a@fu:~$ pypy3 dashtest2.py
```
* <i> debug output</i>
```rebol
Event
Event->scte35:SpliceInfoSection
Event->scte35:SpliceInfoSection->scte35:TimeSignal
Event->scte35:SpliceInfoSection->scte35:TimeSignal->scte35:SpliceTime
Event->scte35:SpliceInfoSection->scte35:SegmentationDescriptor
Event->scte35:SpliceInfoSection->scte35:SegmentationDescriptor->scte35:DeliveryRestrictions
Event->scte35:SpliceInfoSection->scte35:SegmentationDescriptor->scte35:SegmentationUpid
```
* <i> more debug output</i>
```smalltalk
{
    "Event": {
        "duration": 59.0
    },
    "SpliceInfoSection": {
        "protocol_version": 0,
        "pts_adjustment": 2.033367,
        "tier": 4095
    },
    "TimeSignal": {},
    "SpliceTime": {
        "pts_time": 38253.966667
    },
    "SegmentationDescriptor": {
        "segmentation_event_id": 1414668,
        "segmentation_event_cancel_indicator": false,
        "segmentation_duration": 90.0,
        "segmentation_type_id": 52,
        "segment_num": 0,
        "segments_expected": 0
    },
    "DeliveryRestrictions": {
        "web_delivery_allowed_flag": false,
        "no_regional_blackout_flag": false,
        "archive_allowed_flag": false,
        "device_restrictions": 3
    },
    "SegmentationUpid": {
        "segmentation_upid_type": 8,
        "segmentation_upid_length": 8,
        "segmentation_upid": "0x2df3aad7"
    }
}
{}
```
* The Cue
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
