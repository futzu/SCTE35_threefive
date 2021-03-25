### Up and Running in Less Than 7 Seconds.

#### Step One of Two

* Estimated time to complete this step : 2.0 - 2.5 seconds

```js
pip3 install threefive
```

#### Step Two of Two

*  Estimated time to complete this step : 3.0 - 4.5 seconds 

```sh
pthon3 -c 'import threefive; threefive.decode("https://futzu.com/xaa.ts")' 
```

* Ouput looks like this.
```sh
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x3",
        "sap_details": "No Sap Type",
        "section_length": 47,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x0",
        "tier": "0xfff",
        "splice_command_length": 20,
        "splice_command_type": 5,
        "descriptor_loop_length": 10
    },
    "command": {
        "command_length": 20,
        "command_type": 5,
        "name": "Splice Insert",
        "time_specified_flag": true,
        "pts_time": 89742.161689,
        "break_auto_return": false,
        "break_duration": 242.0,
        "splice_event_id": 662,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": false,
        "unique_program_id": 1,
        "avail_num": 0,
        "avail_expected": 0
    },
    "descriptors": [
        {
            "tag": 0,
            "descriptor_length": 8,
            "identifier": "CUEI",
            "name": "Avail Descriptor",
            "provider_avail_id": 0
        }
    ],
    "crc": "0x10fa4d9e",
    "pid": 309,
    "program": 1,
    "pts": 89730.289522
}


```
