### A threefive SCTE-35 Cue

> __1__ ```info_section``` (__Required__)
```js
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x3",
        "sap_details": "No Sap Type",
        "section_length": 42,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment_ticks": 0,            <-- New! 
        "pts_adjustment": 0.0,
        "cw_index": "0xff",
        "tier": "0xfff",
        "splice_command_length": 15,
        "splice_command_type": 5,
        "descriptor_loop_length": 10,
        "crc": "0xd7165c79"
    },

```
> __1__ ```command``` (__Required__)
```js
    "command": {
        "command_length": 15,
        "command_type": 5,
        "name": "Splice Insert",
        "time_specified_flag": true,
        "pts_time": 23683.480033,
        "pts_ticks": 2131513203,                <-- New!
        "splice_event_id": 5690,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": false,
        "splice_immediate_flag": false,
        "unique_program_id": 0,
        "avail_num": 0,
        "avail_expected": 0
    },

```

> __0 or more__ ```descriptors``` (__Optional__)
```go
     "descriptors": [
        {
            "tag": 2,
            "descriptor_length": 23,
            "name": "Segmentation Descriptor",
            "identifier": "CUEI",
            "components": [],
            "segmentation_event_id": "0x4800000a",
            "segmentation_event_cancel_indicator": false,
            "program_segmentation_flag": true,
            "segmentation_duration_flag": false,
            "delivery_not_restricted_flag": false,
            "web_delivery_allowed_flag": true,
            "no_regional_blackout_flag": true,
            "archive_allowed_flag": true,
            "device_restrictions": "No Restrictions",
            "segmentation_message": "Program Blackout Override",
            "segmentation_upid_type": 8,
            "segmentation_upid_type_name": "AiringID",
            "segmentation_upid_length": 8,
            "segmentation_upid": "0x2ca0a1e3",
            "segmentation_type_id": 24,
            "segment_num": 0,
            "segments_expected": 0
        },
        {
            "tag": 2,
            "descriptor_length": 23,
            "name": "Segmentation Descriptor",
            "identifier": "CUEI",
            "components": [],
            "segmentation_event_id": "0x48000009",
            "segmentation_event_cancel_indicator": false,
            "program_segmentation_flag": true,
            "segmentation_duration_flag": false,
            "delivery_not_restricted_flag": false,
            "web_delivery_allowed_flag": true,
            "no_regional_blackout_flag": true,
            "archive_allowed_flag": true,
            "device_restrictions": "No Restrictions",
            "segmentation_message": "Program End",
            "segmentation_upid_type": 8,
            "segmentation_upid_type_name": "AiringID",
            "segmentation_upid_length": 8,
            "segmentation_upid": "0x2ca0a18a",
            "segmentation_type_id": 17,
            "segment_num": 0,
            "segments_expected": 0
        }
    ]

 ```
 > ```packet_data``` (__Optional__)
 ```js
    "packet_data": {
        "pid": "0x40b",
        "program": 1030,
        "pcr_ticks": 8534428819,               <-- New!
        "pcr": 94826.986878,
        "pts_ticks": 2131027203,               <-- New!
        "pts": 23678.080033
    }

``` 
