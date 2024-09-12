# Dash SCTE-35 Parser Preview
### Expected in release 2.4.71
### _Everything here may or may not change._

*  Dash SCTE-35 data is coverted to threefive.Cue instances.

* `threefive.DashSCTE35` is the class
*  the method is `parse_mpd`
```py3
a@fu:~$ pypy3
Python 3.9.16 (7.3.11+dfsg-2+deb12u2, May 20 2024, 22:08:06)
[PyPy 7.3.11 with GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>> from threefive import DashSCTE35
>>>> ds = DashSCTE35()
>>>> mpd ="fu.mpd"
>>>> cues=ds.parse_mpd(mpd)
```
* Output
```js
MPD
MPD->Period
MPD->Period->BaseURL
MPD->Period->EventStream
MPD->Period->EventStream->Event
MPD->Period->EventStream->Event->Signal
MPD->Period->EventStream->Event->Signal->Binary
{
    "MPD": {
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xmlns": "urn:mpeg:dash:schema:mpd:2011",
        "xsi:schema_location": "urn:mpeg:dash:schema:mpd:2011 http://standards.iso.org/ittf/PubliclyAvailableStandards/MPEG-DASH_schema_files/DASH-MPD.xsd",
        "type": "dynamic",
        "availability_start_time": "1970-01-01T00:00:00Z",
        "publish_time": "2024-09-10T05:44:02.778129Z",
        "minimum_update_period": "PT2S",
        "time_shift_buffer_depth": "PT10M",
        "max_segment_duration": "PT3S",
        "min_buffer_time": "PT10S",
        "profiles": "urn:mpeg:dash:profile:isoff-live:2011,urn:com:dashif:dash264,urn:hbbtv:dash:profile:isoff-live:2012"
    },
    "Period": {
        "id": 1,
        "start": "PT0S"
    },
    "BaseURL": {
        "base_u_r_l": "dash/"
    },
    "EventStream": {
        "scheme_id_uri": "urn:scte:scte35:2014:xml+bin",
        "timescale": 1000
    },
    "Event": {
        "presentation_time": 1725946427520,
        "duration": 0.426667,
        "id": 14268737
    },
    "Signal": {
        "xmlns": "http://www.scte.org/schemas/35/2016"
    },
    "Binary": {
        "binary": "/DAgAAAAAAAAAP/wDwUA2blBf//+ADS8AMAAAAAAAORhJCQ="
    }
}
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
        "splice_event_id": 14268737,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": true,
        "event_id_compliance_flag": true,
        "unique_program_id": 49152,
        "avail_num": 0,
        "avail_expected": 0
    },
    "descriptors": []
}
MPD->Period->EventStream->Event
MPD->Period->EventStream->Event->Signal
MPD->Period->EventStream->Event->Signal->Binary
{
    "Event": {
        "presentation_time": 1725946548480,
        "duration": 0.426667,
        "id": 14268738
    },
    "Signal": {
        "xmlns": "http://www.scte.org/schemas/35/2016"
    },
    "Binary": {
        "binary": "/DAgAAAAAAAAAP/wDwUA2blCf//+ADS8AMAAAAAAAORhJCQ="
    }
}
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
        "splice_event_id": 14268738,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": true,
        "event_id_compliance_flag": true,
        "unique_program_id": 49152,
        "avail_num": 0,
        "avail_expected": 0
    },
    "descriptors": []
}
MPD->Period->EventStream->Event
MPD->Period->EventStream->Event->Signal
MPD->Period->EventStream->Event->Signal->Binary
{
    "Event": {
        "presentation_time": 1725946669440,
        "duration": 0.426667,
        "id": 14268739
    },
    "Signal": {
        "xmlns": "http://www.scte.org/schemas/35/2016"
    },
    "Binary": {
        "binary": "/DAgAAAAAAAAAP/wDwUA2blDf//+ADS8AMAAAAAAAORhJCQ="
    }
}
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
        "splice_event_id": 14268739,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": true,
        "event_id_compliance_flag": true,
        "unique_program_id": 49152,
        "avail_num": 0,
        "avail_expected": 0
    },
    "descriptors": []
}
MPD->Period->EventStream->Event
MPD->Period->EventStream->Event->Signal
MPD->Period->EventStream->Event->Signal->Binary
{
    "Event": {
        "presentation_time": 1725946790400,
        "duration": 0.426667,
        "id": 14268740
    },
    "Signal": {
        "xmlns": "http://www.scte.org/schemas/35/2016"
    },
    "Binary": {
        "binary": "/DAgAAAAAAAAAP/wDwUA2blEf//+ADS8AMAAAAAAAORhJCQ="
    }
}
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
        "splice_event_id": 14268740,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": true,
        "event_id_compliance_flag": true,
        "unique_program_id": 49152,
        "avail_num": 0,
        "avail_expected": 0
    },
    "descriptors": []
}
MPD->Period->EventStream->Event
MPD->Period->EventStream->Event->Signal
MPD->Period->EventStream->Event->Signal->Binary
{
    "Event": {
        "presentation_time": 1725946911360,
        "duration": 0.426667,
        "id": 14268741
    },
    "Signal": {
        "xmlns": "http://www.scte.org/schemas/35/2016"
    },
    "Binary": {
        "binary": "/DAgAAAAAAAAAP/wDwUA2blFf//+ADS8AMAAAAAAAORhJCQ="
    }
}
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
        "splice_event_id": 14268741,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": true,
        "event_id_compliance_flag": true,
        "unique_program_id": 49152,
        "avail_num": 0,
        "avail_expected": 0
    },
    "descriptors": []
}
MPD->Period->EventStream->Event
MPD->Period->EventStream->Event->Signal
MPD->Period->EventStream->Event->Signal->Binary
{
    "Event": {
        "presentation_time": 1725947032320,
        "duration": 0.426667,
        "id": 14268742
    },
    "Signal": {
        "xmlns": "http://www.scte.org/schemas/35/2016"
    },
    "Binary": {
        "binary": "/DAgAAAAAAAAAP/wDwUA2blGf//+ADS8AMAAAAAAAORhJCQ="
    }
}
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
        "splice_event_id": 14268742,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": true,
        "event_id_compliance_flag": true,
        "unique_program_id": 49152,
        "avail_num": 0,
        "avail_expected": 0
    },
    "descriptors": []
}
MPD->Period->AdaptationSet
MPD->Period->AdaptationSet->AudioChannelConfiguration
MPD->Period->AdaptationSet->Role
MPD->Period->AdaptationSet->SegmentTemplate
MPD->Period->AdaptationSet->SegmentTemplate->SegmentTimeline
MPD->Period->AdaptationSet->SegmentTemplate->SegmentTimeline->S
MPD->Period->AdaptationSet->Representation
MPD->Period->AdaptationSet
MPD->Period->AdaptationSet->Role
MPD->Period->AdaptationSet->SegmentTemplate
MPD->Period->AdaptationSet->SegmentTemplate->SegmentTimeline
MPD->Period->AdaptationSet->SegmentTemplate->SegmentTimeline->S
MPD->Period->AdaptationSet->Representation
MPD->UTCTiming
{
    "AdaptationSet": {
        "id": 2,
        "group": 2,
        "content_type": "video",
        "par": "16:9",
        "segment_alignment": true,
        "width": 1280,
        "height": 720,
        "sar": "1:1",
        "frame_rate": 25,
        "mime_type": "video/mp4",
        "codecs": "avc1.42C01F",
        "start_with_s_a_p": 1
    },
    "AudioChannelConfiguration": {
        "scheme_id_uri": "urn:mpeg:dash:23003:3:audio_channel_configuration:2011",
        "value": 1
    },
    "Role": {
        "scheme_id_uri": "urn:mpeg:dash:role:2011",
        "value": "main"
    },
    "SegmentTemplate": {
        "timescale": 600,
        "start_number": 898930439,
        "initialization": "scte35-$RepresentationID$.dash",
        "media": "scte35-$RepresentationID$-$Time$.dash"
    },
    "SegmentTimeline": {},
    "S": {
        "t": 1035567864576,
        "d": 1152,
        "r": 311
    },
    "Representation": {
        "id": "video=1000000",
        "bandwidth": 1000000,
        "scan_type": "progressive"
    },
    "UTCTiming": {
        "scheme_id_uri": "urn:mpeg:dash:utc:http-iso:2014",
        "value": "https://time.akamai.com/?iso"
    }
}
>>>> 
```
