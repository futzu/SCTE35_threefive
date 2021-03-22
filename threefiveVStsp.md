# threefive VS. tsduck 
___

__The Video__

```js
-rw-r--r-- 1 root root 3.7G May 21  2020 plp0.ts
```
  * Size: __3.7GB__
  * Duration: __21 mins__
  * Overall Bitrate: __24.9 Mb/s__
  * Programs: __10__ 
  * Streams: __30__
  * SCTE35
      * Streams: __5__
      * Cues: __18__

___



### tsp
```sh
tsp -I file plp0.ts  -P tables --pid 0x03F7 --pid 0x040B --pid 0x0415 --pid 0x041F --pid 0x0451 --text -  -O drop
```
#### `time: 9.845 seconds` 
___


### threefive 
* `pypy3 `
```sh
pypy3 -c "from threefive import decode; decode('plp0.ts')"

```
####  `time: 10.399 seconds`
___

* `python3.7`
```sh
python3 -c "from threefive import decode; decode('plp0.ts')"

```
####  `time: 22.241 seconds`
___



#### Cue Data


* __tsp__ 
```sh
 SCTE 35 Splice Information, TID 252 (0xFC), PID 1055 (0x041F)
  Short section, total size: 50 bytes
  - Section 0:
    Protocol version: 0x00 (0)
    Encryption: none
    PTS adjustment: 0x000000000 (0)
    CW index: 0xFF (255), tier: 0xFFF (4095)
    Command type: 0x05 (SpliceInsert), size: 20 bytes
    Splice event id: 0x00000012, cancel: 0
    Out of network: yes, program splice: yes, duration set: yes, immediate: no
    Time PTS: 0x075C14B4A
    Duration PTS: 0x00066FF30 (6750000), auto return: no
    Unique program id: 0x0001 (1), avail: 0x12 (18), avails expected: 255
    - Descriptor 0: SCTE 35 Avail (0x00, 0), 8 bytes
      Identifier: 0x43554549 ("CUEI")
      Provider id: 0x00000012
    CRC32: 0xEAA8473F (OK)
```
___


* __threefive__ 
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
        "cw_index": "0xff",
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
        "pts_time": 21951.133267,
        "break_auto_return": false,
        "break_duration": 75.0,
        "splice_event_id": 18,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": false,
        "unique_program_id": 1,
        "avail_num": 18,
        "avail_expected": 255
    },
    "descriptors": [
        {
            "tag": 0,
            "descriptor_length": 8,
            "identifier": "CUEI",
            "name": "Avail Descriptor",
            "provider_avail_id": 18
        }
    ],
    "crc": "0xeaa8473f",
    "pid": 1055,
    "program": 1050,
    "pts": 21940.713289
}

```
___
