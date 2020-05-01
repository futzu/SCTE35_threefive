# threefive
## SCTE35 Decoder
*  Parse SCTE 35 messages from Mpeg Transport Streams and Binary files. 
*  Parse SCTE 35 messages encoded in Base64, Binary, or Hex. 

### Fast Start Directions.
*  ['Up and Running in Less Than Seven Seconds'](https://github.com/futzu/SCTE35-threefive/blob/master/FastStart.md) 

###  Splice Commands 
- [x] Splice Null  
- [x] Splice Schedule  (lightly tested)
- [x] Splice Insert 
- [x] Time Signal 
- [x] Bandwidth Reservation  (lightly tested)
###  Splice Descriptors 
- [x]  DTMF Descriptor 
- [x]  Segmentation Descriptor
- [x]  Segmentation UPID  (partially implemented)
- [x]  Segmentation Types and Messages 
- [x]  Time Descriptor 
- [x]  Audio Descriptor (lightly tested)

###  Dependencies 
*  Python 3
*  bitn

##  Install 
```
pip install threefive
Collecting threefive
  Downloading threefive-2.0.69-py3-none-any.whl (12 kB)
Collecting bitn>=0.0.21
  Downloading bitn-0.0.21-py3-none-any.whl (3.0 kB)
Installing collected packages: bitn, threefive
Successfully installed bitn-0.0.21 threefive-2.0.69

```
##  Using threefive  

#### Call threefive.decode.

 ```python
import threefive
```
- [x]  mpegts files
```python
threefive.decode('/path/to/mpegwithscte35.ts') 
```
- [x]  binary files
```python
threefive.decode('/mnt/build/file.bin')
```
- [x]  base64 encoded strings
```python
mesg='/DBhAAAAAAAA///wBQb+qM1E7QBLAhdDVUVJSAAArX+fCAgAAAAALLLXnTUCAAIXQ1VFSUg/nwgIAAAAACyy150RAAACF0NVRUlIAAAnf58ICAAAAAAsstezEAAAihiGnw=='
threefive.decode(mesg)
```
- [x]  hex encoded strings
```python
hexed='0xFC302F000000000000FFFFF014054800008F7FEFFE7369C02EFE0052CCF500000000000A0008435545490000013562DBA30A'
threefive.decode(hexed)
```

### Output for Base64 and Hex Strings
*  SCTE 35 Info Section
*  SCTE 35 Command
*  SCTE 35 Descriptors

```js
{ 'Info_Section': { 'crc': '0x9972e343',
                    'cw_index': '0xff',
                    'descriptor_loop_length': 50,
                    'encrypted_packet': False,
                    'encryption_algorithm': 0,
                    'private': False,
                    'protocol_version': 0,
                    'pts_adjustment': 0.0,
                    'reserved': 3,
                    'section_length': 72,
                    'section_syntax_indicator': False,
                    'splice_command_length': 5,
                    'splice_command_type': 6,
                    'table_id': '0xfc',
                    'tier': '0xfff'},
  'Splice_Command': { 'name': 'Time '
                              'Signal',
                      'pts_time': 22798.906911,
                      'time_specified_flag': True},
  'Splice_Descriptors': [ { 'archive_allowed_flag': True,
                            'delivery_not_restricted_flag': False,
                            'descriptor_length': 23,
                            'device_restrictions': '0x3',
                            'identifier': 'CUEI',
                            'name': 'Segmentation '
                                    'Descriptor',
                            'no_regional_blackout_flag': True,
                            'program_segmentation_flag': True,
                            'segment_num': 0,
                            'segmentation_duration_flag': False,
                            'segmentation_event_cancel_indicator': False,
                            'segmentation_event_id': '0x48000018',
                            'segmentation_message': 'Program '
                                                    'End',
                            'segmentation_type_id': 17,
                            'segmentation_upid_length': 8,
                            'segmentation_upid_type': 8,
                            'segments_expected': 0,
                            'splice_descriptor_tag': 2,
                            'turner_identifier': '0x2ccbc344',
                            'web_delivery_allowed_flag': True},
                          { 'archive_allowed_flag': True,
                            'delivery_not_restricted_flag': False,
                            'descriptor_length': 23,
                            'device_restrictions': '0x3',
                            'identifier': 'CUEI',
                            'name': 'Segmentation '
                                    'Descriptor',
                            'no_regional_blackout_flag': True,
                            'program_segmentation_flag': True,
                            'segment_num': 0,
                            'segmentation_duration_flag': False,
                            'segmentation_event_cancel_indicator': False,
                            'segmentation_event_id': '0x48000019',
                            'segmentation_message': 'Program '
                                                    'Start',
                            'segmentation_type_id': 16,
                            'segmentation_upid_length': 8,
                            'segmentation_upid_type': 8,
                            'segments_expected': 0,
                            'splice_descriptor_tag': 2,
                            'turner_identifier': '0x2ca4dba0',
                            'web_delivery_allowed_flag': True}]}

```
### Output for Mpegts streams and Files
*  Packet Pid
*  Packet PTS
*  SCTE 35 Info Section
*  SCTE 35 Command
*  SCTE 35 Descriptors

```js
{ 'Info_Section': { 'crc': '0x6e33321e',
                    'cw_index': '0x0',
                    'descriptor_loop_length': 10,
                    'encrypted_packet': False,
                    'encryption_algorithm': 0,
                    'private': False,
                    'protocol_version': 0,
                    'pts_adjustment': 0.0,
                    'reserved': 3,
                    'section_length': 42,
                    'section_syntax_indicator': False,
                    'splice_command_length': 4095,
                    'splice_command_type': 5,
                    'table_id': '0xfc',
                    'tier': '0xfff'},
  'Packet': { 'pid': '0x135',
              'pts': 89977.249522},
  'Splice_Command': { 'avail_expected': 0,
                      'avail_num': 0,
                      'duration_flag': False,
                      'name': 'Splice '
                              'Insert',
                      'out_of_network_indicator': False,
                      'program_splice_flag': True,
                      'pts_time': 89984.161689,
                      'splice_event_cancel_indicator': False,
                      'splice_event_id': 662,
                      'splice_immediate_flag': False,
                      'time_specified_flag': True,
                      'unique_program_id': 1},
  'Splice_Descriptors': [ { 'descriptor_length': 8,
                            'identifier': 'CUEI',
                            'name': 'Avail '
                                    'Descriptor',
                            'provider_avail_id': 0,
                            'splice_descriptor_tag': 0}]}
```

###  Using threefive.Splice

The threefive.Splice class can be used to decode a SCTE35 message. 

threefive.Splice provides several methods to access the parsed data.

```python

from threefive import Splice

b64 = "/DBIAAAAAAAA///wBQb+ek2ItgAyAhdDVUVJSAAAGH+fCAgAAAAALMvDRBEAAAIXQ1VFSUgAABl/nwgIAAAAACyk26AQAACZcuND"

scte35 = Splice(b64)

````
- [x] Pretty print the SCTE 35 message data.
```python
scte35.show()
```
- [x] Return all message data in a dict.
```python
scte35.get()
```
- [x] Pretty print SCTE 35 splice info section.
```python
scte35.show_info_section()
```
- [x] Return SCTE 35 splice info section as a dict.
```python
scte35.get_info_section()

```        
- [x] Pretty print SCTE 35 splice command.
```python

scte35.show_command()

{ 'name': 'Time Signal',
  'pts_time': 22798.906911,
  'time_specified_flag': True}
  
```
- [x] Return the SCTE 35 splice command data as a dict.
```python
scte35.get_command()
```     
- [x] Pretty print SCTE 35 splice descriptors.
```python
scte35.show_descriptors()
```    
- [x] Return a list of SCTE 35 splice descriptors as dicts.
```python
scte35.get_descriptors()
```      
