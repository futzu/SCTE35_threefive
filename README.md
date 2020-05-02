# threefive
## SCTE35 Decoder
* [Supported Splice Commands](#splice-commands)
* [Supported Splice Descriptors](#splice-descriptors)
* [Fast Start Directions](#fast-start-directions)
* [Dependencies](#dependencies)
* [Install](#install)
* [Parsing SCTE 35 messages from Mpeg Transport Streams and Binary files](#mpegts-files)
* [Parsing SCTE 35 messages encoded in Base64, Binary, or Hex](#base64-encoded-strings)
* [Using threefive](#using-threefive)
  * [The decode Function](#the-decode-function)
    * [MpegTS Files](#mpegts-files)
    * [Binary Files](#binary-files)
    * [Output for MpegTS and Binary Files and Streams](#output-for-mpegts-and-binary-files-and-streams)
    * [Base64 Encoded Strings](#base64-encoded-strings)
    * [Hex Encoded Strings](#hex-encoded-strings)
    * [Output for Base64 and Hex Strings](#output-for-base64-and-hex-strings)
  * [Using The Splice Class](#using-the-splice-class)
    * [Pretty Print SCTE 35 Message](#pretty-print-scte-35-message)
    * [Return SCTE 35 Message](#return-scte-35-message)
    * [Pretty Print Splice Info Section](#pretty-print-splice-info-section)
    * [Return Splice Info Section](#return-splice-info-section)
    * [Pretty Print Splice Command](#pretty-print-splice-command)
    * [Return Splice Command](#return-splice-command)
    * [Pretty Print Splice Descriptors](#pretty-print-splice-descriptors)
    * [Return Splice Descriptors](#return-splice-descriptors)  
  * [Using The Stream Class](#using-the-stream-class)
  
  
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



### Fast Start Directions.
*  ['Up and Running in Less Than Seven Seconds'](https://github.com/futzu/SCTE35-threefive/blob/master/FastStart.md) 


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

### The decode Function

 ```python
import threefive
```
#### MpegTS Files
```python
threefive.decode('/path/to/mpegwithscte35.ts') 
```
#### Binary Files
```python
threefive.decode('/mnt/build/file.bin')
```
#### Output for MpegTS and Binary Files and Streams
```python3
{ 'SCTE35': { 'Info_Section': { 'crc': '0x10fa4d9e',
                                'cw_index': '0x0',
                                'descriptor_loop_length': 10,
                                'encrypted_packet': False,
                                'encryption_algorithm': 0,
                                'private': False,
                                'protocol_version': 0,
                                'pts_adjustment': 0.0,
                                'reserved': '0x3',
                                'section_length': 47,
                                'section_syntax_indicator': False,
                                'splice_command_length': 4095,
                                'splice_command_type': 5,
                                'table_id': '0xfc',
                                'tier': '0xfff'},
              'Packet': { 'pid': '0x135'},
              'Splice_Command': { 'avail_expected': 0,
                                  'avail_num': 0,
                                  'break_auto_return': False,
                                  'break_duration': 242.0,
                                  'duration_flag': True,
                                  'name': 'Splice '
                                          'Insert',
                                  'out_of_network_indicator': True,
                                  'program_splice_flag': True,
                                  'pts_time': 89742.161689,
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
                                        'splice_descriptor_tag': 0}]}}
```
####  Base64 Encoded Strings
```python
mesg='/DBhAAAAAAAA///wBQb+qM1E7QBLAhdDVUVJSAAArX+fCAgAAAAALLLXnTUCAAIXQ1VFSUg/nwgIAAAAACyy150RAAACF0NVRUlIAAAnf58ICAAAAAAsstezEAAAihiGnw=='
threefive.decode(mesg)
```
#### Hex Encoded Strings
```python
hexed='0xFC302F000000000000FFFFF014054800008F7FEFFE7369C02EFE0052CCF500000000000A0008435545490000013562DBA30A'
threefive.decode(hexed)
```

#### Output for Base64 and Hex Strings

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



```


##  Using The Splice Class

The threefive.Splice class can be used to decode a SCTE35 message. 

threefive.Splice provides several methods to access the parsed data.

```python

from threefive import Splice

b64 = "/DBIAAAAAAAA///wBQb+ek2ItgAyAhdDVUVJSAAAGH+fCAgAAAAALMvDRBEAAAIXQ1VFSUgAABl/nwgIAAAAACyk26AQAACZcuND"

scte35 = Splice(b64)

````
#### Pretty Print SCTE 35 Message
```python
scte35.show()
```

#### Return SCTE 35 Message
```python
scte35.get()
```

#### Pretty Print Splice Info Section
```python
scte35.show_info_section()
```

#### Return Splice Info Section
```python
scte35.get_info_section()

```        
#### Pretty print Splice Command.
```python
scte35.show_command()

{ 'name': 'Time Signal',
  'pts_time': 22798.906911,
  'time_specified_flag': True}
  
```

#### Return Splice Command
```python
scte35.get_command()

``` 

#### Pretty Print Splice Descriptors
```python
scte35.show_descriptors()

```    
#### Return Splice Descriptors
```python
scte35.get_descriptors()

```      
##  Using The Stream Class
* threefive.Stream can be called with three args.
  * threefive.Stream(tsfile = None, tsstream = None, show_null = False)
     * Either tsstream or tsfile must be set.
     * tsfile is for mpegts and binary files
     * tsstream, when used, is usually sys.stdin.buffer, to enable piping in streams.
     * show_null if set to True, enables showing SCTE 35 Null Commands.
     
     
