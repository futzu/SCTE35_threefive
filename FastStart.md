### Up and Running in Less Than 7 Seconds.

#### Step One of Two

* Estimated time to complete this step : 2.0 - 2.5 seconds

```js
pip3 install threefive
```

#### Step Two of Two

*  Estimated time to complete this step : 3.0 - 4.5 seconds 

```smalltalk
a@fumatica:~$ pypy3
Python 3.8.13 (7.3.9+dfsg-1, Apr 01 2022, 03:05:43)
[PyPy 7.3.9 with GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
 
 from threefive import Stream
 strm = Stream("https://futzu.com/xaa.ts")`
 strm.decode()
```



* Ouput looks like this.
```lua
{
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
        "pts_adjustment_ticks": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0xff",
        "tier": "0xfff",
        "splice_command_length": 15,
        "splice_command_type": 5,
        "descriptor_loop_length": 10,
        "crc": "0x1ed64bdb"
    },
    "command": {
        "command_length": 15,
        "command_type": 5,
        "name": "Splice Insert",
        "time_specified_flag": true,
        "pts_time": 22026.133267,
        "pts_time_ticks": 1982351994,
        "splice_event_id": 18,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": false,
        "program_splice_flag": true,
        "duration_flag": false,
        "splice_immediate_flag": false,
        "unique_program_id": 1,
        "avail_num": 18,
        "avail_expected": 255
    },
    "descriptors": [
        {
            "tag": 0,
            "descriptor_length": 8,
            "name": "Avail Descriptor",
            "identifier": "CUEI",
            "provider_avail_id": 18
        }
    ],
    "packet_data": {
        "pid": "0x41f",
        "program": 1050,
        "pts_ticks": 1981774196,
        "pts": 22019.713289
    }
}



```
