
### 35 decode, command line SCTE35 decoder.

>type 'make cli' or 'make pypy3-cli' as root to install to /usr/local/bin

#### use like:
```fortran
cat myvideo.ts | 35decode
```
```fortran
35decode https://futzu.com/xaa.ts
```
```fortran
35decode ~/myvideo.ts https://futzu.com/xaa.ts someothervideo.ts 
```
```fortran
35decode mpegts_dir/*.ts
```
 ```fortran
35decode '/DBZAAAAAAAA///wBQb+AAAAAABDAkFDVUVJAAAACn//AAApMuAPLXVybjp1dWlkOmFhODViYmI2LTVjNDMtNGI2YS1iZWJiLWVlM2IxM2ViNzk5ORAAAFz7UQA='
 ```
#### Output:
```fortran
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x3",
        "sap_details": "No Sap Type",
        "section_length": 171,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment_ticks": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x0",
        "tier": "0xfff",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 149,
        "crc": "0x8202d03b"
    },
    "command": {
        "command_length": 5,
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 17144.101244,
        "pts_ticks": 1542969112
    },
    "descriptors": [
        {
            "tag": 2,
            "descriptor_length": 49,
            "name": "Segmentation Descriptor",
            "identifier": "CUEI",
            "components": [],
            "segmentation_event_id": "0x970d471",
            "segmentation_event_cancel_indicator": false,
            "program_segmentation_flag": true,
            "segmentation_duration_flag": false,
            "delivery_not_restricted_flag": false,
            "web_delivery_allowed_flag": true,
            "no_regional_blackout_flag": true,
            "archive_allowed_flag": true,
            "device_restrictions": "No Restrictions",
            "segmentation_message": "Chapter End",
            "segmentation_upid_type": 1,
            "segmentation_upid_type_name": "Deprecated",
            "segmentation_upid_length": 34,
            "segmentation_upid": "fumatic",
            "segmentation_type_id": 33,
            "segment_num": 1,
            "segments_expected": 1
        },
        {
            "tag": 2,
            "descriptor_length": 49,
            "name": "Segmentation Descriptor",
            "identifier": "CUEI",
            "components": [],
            "segmentation_event_id": "0x970d470",
            "segmentation_event_cancel_indicator": false,
            "program_segmentation_flag": true,
            "segmentation_duration_flag": false,
            "delivery_not_restricted_flag": false,
            "web_delivery_allowed_flag": true,
            "no_regional_blackout_flag": true,
            "archive_allowed_flag": true,
            "device_restrictions": "No Restrictions",
            "segmentation_message": "Program End",
            "segmentation_upid_type": 1,
            "segmentation_upid_type_name": "Deprecated",
            "segmentation_upid_length": 34,
            "segmentation_upid": "fumatic",
            "segmentation_type_id": 17,
            "segment_num": 1,
            "segments_expected": 1
        },
        {
            "tag": 2,
            "descriptor_length": 19,
            "name": "Segmentation Descriptor",
            "identifier": "CUEI",
            "components": [],
            "segmentation_event_id": "0x9710f17",
            "segmentation_event_cancel_indicator": false,
            "program_segmentation_flag": true,
            "segmentation_duration_flag": false,
            "delivery_not_restricted_flag": false,
            "web_delivery_allowed_flag": true,
            "no_regional_blackout_flag": true,
            "archive_allowed_flag": true,
            "device_restrictions": "No Restrictions",
            "segmentation_message": "Program Start",
            "segmentation_upid_type": 1,
            "segmentation_upid_type_name": "Deprecated",
            "segmentation_upid_length": 4,
            "segmentation_upid": "fumatic",
            "segmentation_type_id": 16,
            "segment_num": 1,
            "segments_expected": 1
        },
        {
            "tag": 2,
            "descriptor_length": 24,
            "name": "Segmentation Descriptor",
            "identifier": "CUEI",
            "components": [],
            "segmentation_event_id": "0x9710f18",
            "segmentation_event_cancel_indicator": false,
            "program_segmentation_flag": true,
            "segmentation_duration_flag": true,
            "delivery_not_restricted_flag": false,
            "web_delivery_allowed_flag": true,
            "no_regional_blackout_flag": true,
            "archive_allowed_flag": true,
            "device_restrictions": "No Restrictions",
            "segmentation_duration": 1343.0,
            "segmentation_duration_ticks": 120870000,
            "segmentation_message": "Chapter Start",
            "segmentation_upid_type": 1,
            "segmentation_upid_type_name": "Deprecated",
            "segmentation_upid_length": 4,
            "segmentation_upid": "fumatic",
            "segmentation_type_id": 32,
            "segment_num": 1,
            "segments_expected": 1
        }
    ],
    "packet_data": {
        "pid": "0x36",
        "program": 1,
        "pcr_ticks": 1542841778,
        "pcr": 17142.686422,
        "pts_ticks": 1542877610,
        "pts": 17143.084556
    }
    
}
```



>I am water. Pour me in a cup, I become the cup.
