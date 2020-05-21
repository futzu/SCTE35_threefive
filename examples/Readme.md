### Running The Examples.


#### Running scripts.

```python3
python3  Splice_Insert.py
```
---
```python3
{ 'SCTE35': { 'Info_Section': { 'crc': '0x62dba30a',
                                'cw_index': '0xff',
                                'descriptor_loop_length': 10,
                                'encrypted_packet': False,
                                'encryption_algorithm': 0,
                                'private': False,
                                'protocol_version': 0,
                                'pts_adjustment': 0.0,
                                'reserved': '0x3',
                                'section_length': 47,
                                'section_syntax_indicator': False,
                                'splice_command_length': 20,
                                'splice_command_type': 5,
                                'table_id': '0xfc',
                                'tier': '0xfff'},
              'Splice_Command': { 'avail_expected': 0,
                                  'avail_num': 0,
                                  'break_auto_return': True,
                                  'break_duration': 60.293567,
                                  'duration_flag': True,
                                  'name': 'Splice '
                                          'Insert',
                                  'out_of_network_indicator': True,
                                  'program_splice_flag': True,
                                  'pts_time': 21514.559089,
                                  'splice_event_cancel_indicator': False,
                                  'splice_event_id': 1207959695,
                                  'splice_immediate_flag': False,
                                  'time_specified_flag': True,
                                  'unique_program_id': 0},
              'Splice_Descriptors': [ { 'descriptor_length': 8,
                                        'identifier': 'CUEI',
                                        'name': 'Avail '
                                                'Descriptor',
                                        'provider_avail_id': 309,
                                        'splice_descriptor_tag': 0}]}}
{ 'SCTE35': { 'Info_Section': { 'crc': '0x62dba30a',
                                'cw_index': '0xff',
                                'descriptor_loop_length': 10,
                                'encrypted_packet': False,
                                'encryption_algorithm': 0,
                                'private': False,
                                'protocol_version': 0,
                                'pts_adjustment': 0.0,
                                'reserved': '0x3',
                                'section_length': 47,
                                'section_syntax_indicator': False,
                                'splice_command_length': 20,
                                'splice_command_type': 5,
                                'table_id': '0xfc',
                                'tier': '0xfff'},
              'Splice_Command': { 'avail_expected': 0,
                                  'avail_num': 0,
                                  'break_auto_return': True,
                                  'break_duration': 60.293567,
                                  'duration_flag': True,
                                  'name': 'Splice '
                                          'Insert',
                                  'out_of_network_indicator': True,
                                  'program_splice_flag': True,
                                  'pts_time': 21514.559089,
                                  'splice_event_cancel_indicator': False,
                                  'splice_event_id': 1207959695,
                                  'splice_immediate_flag': False,
                                  'time_specified_flag': True,
                                  'unique_program_id': 0},
              'Splice_Descriptors': [ { 'descriptor_length': 8,
                                        'identifier': 'CUEI',
                                        'name': 'Avail '
                                                'Descriptor',
                                        'provider_avail_id': 309,
                                        'splice_descriptor_tag': 0}]}}
```


#### Using the bin files.

* Each bin file is a single SCTE 35 packet. 
* Parse with the __threefive.decode__ function
* Parse with a __threefive.Stream__ or __threefive.StreamPlus__ Instance


```python3
Python 3.7.4 (default, Jul 16 2019, 07:12:58) 
[GCC 9.1.0] on linux
Type "help", "copyright", "credits" or "license" for more information.

>>> import threefive
>>> threefive.decode('file.bin')
{
 "SCTE35": {
  "Info_Section": {
   "table_id": "0xfc",
   "section_syntax_indicator": false,
   "private": false,
   "reserved": "0x3",
   "section_length": 78,
   "protocol_version": 0,
   "encrypted_packet": false,
   "encryption_algorithm": 0,
   "pts_adjustment": 0.0,
   "cw_index": "0x0",
   "tier": "0xfff",
   "splice_command_length": 5,
   "splice_command_type": 6,
   "descriptor_loop_length": 60,
   "crc": "0x534500d1"
  },
  "Splice_Command": {
   "time_specified_flag": true,
   "pts_time": 0.555556,
   "name": "Time Signal",
   "splice_command_length": 5
  },
  "Splice_Descriptors": [
   {
    "tag": 2,
    "identifier": "CUEI",
    "name": "Segmentation Descriptor",
    "segmentation_event_id": "0x3",
    "segmentation_event_cancel_indicator": false,
    "program_segmentation_flag": true,
    "segmentation_duration_flag": true,
    "delivery_not_restricted_flag": true,
    "segmentation_duration": 0.000178,
    "segmentation_upid_type": 12,
    "segmentation_upid_length": 38,
    "segmentation_upid": "MPU:{'format identifier': 1279415385, 'private data': 4}",
    "segmentation_type_id": 54,
    "segmentation_message": "Distributor Placement Opportunity Start",
    "segment_num": 0,
    "segments_expected": 0,
    "sub_segment_num": 0,
    "sub_segments_expected": 0,
    "descriptor_length": 58
   }
  ]
 }
}






<threefive.stream.Stream object at 0x7f6667031d10>
```


