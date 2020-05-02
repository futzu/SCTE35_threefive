### Running The Examples.


#### Running scripts.

- [x] Splice_Insert.py

```python3
python3  Splice_Insert.py

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

- [x] Time_Signal-Placement_Opportunity_Start.py

```python3

python3 Time_Signal-Placement_Opportunity_Start.py 

{ 'SCTE35': { 'Info_Section': { 'crc': '0x9ac9d17e',
                                'cw_index': '0xff',
                                'descriptor_loop_length': 30,
                                'encrypted_packet': False,
                                'encryption_algorithm': 0,
                                'private': False,
                                'protocol_version': 0,
                                'pts_adjustment': 0.0,
                                'reserved': '0x3',
                                'section_length': 52,
                                'section_syntax_indicator': False,
                                'splice_command_length': 5,
                                'splice_command_type': 6,
                                'table_id': '0xfc',
                                'tier': '0xfff'},
              'Splice_Command': { 'name': 'Time '
                                          'Signal',
                                  'pts_time': 21388.766756,
                                  'time_specified_flag': True},
              'Splice_Descriptors': [ { 'archive_allowed_flag': True,
                                        'delivery_not_restricted_flag': False,
                                        'descriptor_length': 28,
                                        'device_restrictions': '0x3',
                                        'identifier': 'CUEI',
                                        'name': 'Segmentation '
                                                'Descriptor',
                                        'no_regional_blackout_flag': True,
                                        'program_segmentation_flag': True,
                                        'segment_num': 2,
                                        'segmentation_duration': 307.0,
                                        'segmentation_duration_flag': True,
                                        'segmentation_event_cancel_indicator': False,
                                        'segmentation_event_id': '0x4800008e',
                                        'segmentation_message': 'Provider '
                                                                'Placement '
                                                                'Opportunity '
                                                                'Start',
                                        'segmentation_type_id': 52,
                                        'segmentation_upid_length': 8,
                                        'segmentation_upid_type': 8,
                                        'segments_expected': 0,
                                        'splice_descriptor_tag': 2,
                                        'turner_identifier': '0x2ca0a18a',
                                        'web_delivery_allowed_flag': False}]}}

```

#### Using the bin files.

* Each bin file is a single SCTE 35 packet. 

- [x]  file.bin

```python3
Python 3.7.4 (default, Jul 16 2019, 07:12:58) 
[GCC 9.1.0] on linux
Type "help", "copyright", "credits" or "license" for more information.

>>> import threefive
>>> threefive.Stream('file.bin')
{ 'Info_Section': { 'crc': '0x54590000',
                    'cw_index': '0x0',
                    'descriptor_loop_length': 60,
                    'encrypted_packet': False,
                    'encryption_algorithm': 0,
                    'private': False,
                    'protocol_version': 0,
                    'pts_adjustment': 0.0,
                    'reserved': 3,
                    'section_length': 78,
                    'section_syntax_indicator': False,
                    'splice_command_length': 5,
                    'splice_command_type': 6,
                    'table_id': '0xfc',
                    'tier': '0xfff'},
  'Splice_Command': { 'name': 'Time '
                              'Signal',
                      'pts_time': 0.555556,
                      'time_specified_flag': True},
  'Splice_Descriptors': [ { 'delivery_not_restricted_flag': True,
                            'descriptor_length': 58,
                            'identifier': 'CUEI',
                            'name': 'Segmentation '
                                    'Descriptor',
                            'program_segmentation_flag': True,
                            'segment_num': 76,
                            'segmentation_duration': 0.000178,
                            'segmentation_duration_flag': True,
                            'segmentation_event_cancel_indicator': False,
                            'segmentation_event_id': '0x3',
                            'segmentation_message': 'Closing '
                                                    'Credit '
                                                    'Start',
                            'segmentation_type_id': 38,
                            'segmentation_upid_type': 12,
                            'segments_expected': 66,
                            'splice_descriptor_tag': 2}]}
<threefive.stream.Stream object at 0x7f6667031d10>
```
- [x] file2.bin
```python3
>>> threefive.Stream('file2.bin')
{ 'Info_Section': { 'crc': '0x54590000',
                    'cw_index': '0x0',
                    'descriptor_loop_length': 60,
                    'encrypted_packet': False,
                    'encryption_algorithm': 0,
                    'private': False,
                    'protocol_version': 0,
                    'pts_adjustment': 0.0,
                    'reserved': 3,
                    'section_length': 78,
                    'section_syntax_indicator': False,
                    'splice_command_length': 5,
                    'splice_command_type': 6,
                    'table_id': '0xfc',
                    'tier': '0xfff'},
  'Packet': {'pid': '0x135'},
  'Splice_Command': { 'name': 'Time '
                              'Signal',
                      'pts_time': 93221.495456,
                      'time_specified_flag': True},
  'Splice_Descriptors': [ { 'delivery_not_restricted_flag': True,
                            'descriptor_length': 58,
                            'identifier': 'CUEI',
                            'name': 'Segmentation '
                                    'Descriptor',
                            'program_segmentation_flag': True,
                            'segment_num': 76,
                            'segmentation_duration': 0.000189,
                            'segmentation_duration_flag': True,
                            'segmentation_event_cancel_indicator': False,
                            'segmentation_event_id': '0x3',
                            'segmentation_message': 'Closing '
                                                    'Credit '
                                                    'End',
                            'segmentation_type_id': 39,
                            'segmentation_upid_type': 13,
                            'segments_expected': 66,
                            'splice_descriptor_tag': 2}]}
<threefive.stream.Stream object at 0x7f6667037750>
```


