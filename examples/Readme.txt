Running The Examples.


1. Running scripts.

python3 Splice_Insert.py 
     

parsing 0xFC302F000000000000FFFFF014054800008F7FEFFE7369C02EFE0052CCF500000000000A0008435545490000013562DBA30A

{ 'Info_Section': { 'crc': '0x62dba30a',
                    'cw_index': '0xff',
                    'descriptor_loop_length': 10,
                    'encrypted_packet': False,
                    'encryption_algorithm': 0,
                    'private': False,
                    'protocol_version': 0,
                    'pts_adjustment': 0.0,
                    'reserved': 3,
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
                            'splice_descriptor_tag': 0}]}

parsing /DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo=

{ 'Info_Section': { 'crc': '0x62dba30a',
                    'cw_index': '0xff',
                    'descriptor_loop_length': 10,
                    'encrypted_packet': False,
                    'encryption_algorithm': 0,
                    'private': False,
                    'protocol_version': 0,
                    'pts_adjustment': 0.0,
                    'reserved': 3,
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
                            'splice_descriptor_tag': 0}]}


2. Using the bin files.

Each bin file is a single SCTE 35 packet. 

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

