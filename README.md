# threefive
## SCTE35 Decoder
---
* [Supported Splice Commands](#splice-commands)
* [Supported Splice Descriptors](#splice-descriptors)

* [__Fast Start Directions__](#fast-start-directions)
* [Dependencies](#dependencies)
* [__Install__](#install)

* [__Examples__](https://github.com/futzu/SCTE35-threefive/tree/master/examples)
    * [Splice Insert](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Splice_Insert.py)
    * [Time Signal Placement Opportunity Start](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Time_Signal-Placement_Opportunity_Start.py)
    * [Time Signal Placement Opportunity End](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Time_Signal-Placement_Opportunity_End.py)
    * [Time Signal Program Overlap ](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Time_Signal-Program_Overlap.py)
    * [Time Signal Program Start End](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Time_Signal-Program_Start_End.py)

* [__Easy threefive__](#easy-threefive)
  *   [The __decode__ Function](#the-decode-function)
      * [Parsing SCTE 35 messages from Mpeg Transport Streams and Binary files](#mpegts)
        * [Output for MpegTS and Binary Files and Streams](#output-for-mpegts-and-binary-files-and-streams)
      * [Parsing SCTE 35 messages encoded in Base64, Binary, or Hex](#base64-encoded-strings)
        * [Output for Base64 and Hex Strings](#output-for-base64-and-hex-strings)

* [__Advanced threefive__](#advanced-threefive)
  *   [__Splice Class__](#splice-class)
      * [Pretty Print SCTE 35 Message](#pretty-print-scte-35-message)
      * [Return SCTE 35 Message](#return-scte-35-message)
      * [Pretty Print Splice Info Section](#pretty-print-splice-info-section)
      * [Return Splice Info Section](#return-splice-info-section)
      * [Pretty Print Splice Command](#pretty-print-splice-command)
      * [Return Splice Command](#return-splice-command)
      * [Pretty Print Splice Descriptors](#pretty-print-splice-descriptors)
      * [Return Splice Descriptors](#return-splice-descriptors)  
  *   [__Stream Class__](#stream-class)
      * [Parse a Local File with a Stream Instance](#parse-a-local-file-with-a-stream-instance)
      * [Pipe a Video to Stream](#pipe-a-video-to-stream)
  *  [__StreamPlus Class__](#streamplus-class)
      * [Parse a Local File with a StreamPlus Instance](#parse-a-local-file-with-a-streamplus-instance)
      * [Pipe a Video to StreamPlus](#pipe-a-video-to-streamplus)
---  
##  ```Splice Commands``` 
  *  source [splice_commands.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/splice_commands.py)
  *  Splice Null  
  *  Splice Schedule  (lightly tested)
  *  Splice Insert 
  *  Time Signal 
  *  Bandwidth Reservation  (lightly tested)
##  ```Splice Descriptors```  
  *  source [descriptors.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py)
  *  DTMF Descriptor 
  *  Segmentation Descriptor
  *  Segmentation UPID  (partially implemented)
  *  Segmentation Types and Messages 
  *  Time Descriptor 
  *  Audio Descriptor (lightly tested)
  
  
  [🡡 top](#threefive)


## ```Fast Start Directions```

*  [__Up and Running in Less Than Seven Seconds__](https://github.com/futzu/SCTE35-threefive/blob/master/FastStart.md) 


##  ```Dependencies``` 
*  Python 3
*  [__bitn__](https://github.com/futzu/bitn)

##  ```Install``` 
```
pip install threefive
Collecting threefive
  Downloading threefive-2.0.99-py3-none-any.whl (12 kB)
Collecting bitn>=0.0.27
  Downloading bitn-0.0.27-py3-none-any.whl (3.0 kB)
Installing collected packages: bitn, threefive
Successfully installed bitn-0.0.27 threefive-2.0.99

```
 
  
[🡡 top](#threefive)


##  ```Easy threefive```  

###   ```The decode Function``` 
 *   source [decode.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/decode.py)
 * __threefive.decode__ is an all purpose function to decode SCTE 35 messages from a file or string.

 ```python
import threefive
```
####    ```MpegTS```
```python
threefive.decode('/path/to/mpegwithscte35.ts') 
```
####    ```Binary```
```python
threefive.decode('/mnt/build/file.bin')
```

####    ```Output for MpegTS and Binary Files and Streams```
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
####  ```Base64 Encoded Strings```
```python
mesg='/DBhAAAAAAAA///wBQb+qM1E7QBLAhdDVUVJSAAArX+fCAgAAAAALLLXnTUCAAIXQ1VFSUg/nwgIAAAAACyy150RAAACF0NVRUlIAAAnf58ICAAAAAAsstezEAAAihiGnw=='
threefive.decode(mesg)
```
#### ```Hex Encoded Strings```
```python
hexed='0xFC302F000000000000FFFFF014054800008F7FEFFE7369C02EFE0052CCF500000000000A0008435545490000013562DBA30A'
threefive.decode(hexed)
```

#### ```Output for Base64 and Hex Strings```

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

 [🡡 top](#threefive)
 

## ```Advanced threefive```

###  ```Splice Class```  
   *  source [splice.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/splice.py)

   *  The __threefive.Splice__ class decodes a SCTE35 binary, base64, or hex encoded string. 
   *  __threefive.Splice__ provides several methods to access the parsed data.

```python

from threefive import Splice

b64 = "/DBIAAAAAAAA///wBQb+ek2ItgAyAhdDVUVJSAAAGH+fCAgAAAAALMvDRBEAAAIXQ1VFSUgAABl/nwgIAAAAACyk26AQAACZcuND"

scte35 = Splice(b64)

````
#### ```Pretty Print SCTE 35 Message```
```python
scte35.show()
```

#### ```Return SCTE 35 Message```
```python
scte35.get()
```

#### ```Pretty Print Splice Info Section```
```python
scte35.show_info_section()
```

#### ```Return Splice Info Section```
```python
scte35.get_info_section()

```        
#### ```Pretty print Splice Command```
```python
scte35.show_command()

{ 'name': 'Time Signal',
  'pts_time': 22798.906911,
  'time_specified_flag': True}
  
```

#### ```Return Splice Command```
```python
scte35.get_command()

``` 

#### ```Pretty Print Splice Descriptors```
```python
scte35.show_descriptors()

```    
#### ```Return Splice Descriptors```
```python
scte35.get_descriptors()

```

 [🡡 top](#threefive)
 
 
---
###  ```Stream Class``` 
  * source [stream.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/stream.py)

  * The __threefive.Stream__ class parses SCTE35 messages from a file or stream.
  
```python3
  threefive.Stream(tsdata, show_null = False)
  ```
   * __tsdata__ is an open file handle or sys.stdin.buffer to read 'piped' in data.
   * __show_null__ if set to True, enables showing SCTE 35 null commands.
  
 #### ```Parse a Local File with a Stream Instance```
 
 ```python3
 
 import sys
 from threefive import Stream
 '''
 
 if __name__ =='__main__':
    with open(sys.argv[1],'rb') as tsdata:
        Stream(tsdata)

```

#### ```Pipe a Video to Stream```

```sh

curl -s https://futzu.com/xaa.ts -o -  \
  | python3 -c 'import sys;import threefive; threefive.Stream(sys.stdin.buffer)' 
```
---
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


 [🡡 top](#threefive)

---
###  ```StreamPlus Class``` 
  * source [streamplus.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/streamplus.py)
  * __threefive.StreamPlus__ is a sub class of  __threefive.Stream__

```python3
  threefive.StreamPlus(tsdata, show_null = False)
```
   * __tsdata__ is an open file handle or sys.stdin.buffer to read 'piped' in data.
   * __show_null__ if set to True, enables showing SCTE 35 null commands.
    
   * __threefive.StreamPlus__ adds the PTS timestamp for each SCTE 35 packet.

#### ```Parse a Local File with a StreamPlus Instance```
 
 ```python3
 
 import sys
 from threefive import StreamPlus
 '''
 
 if __name__ =='__main__':
    with open(sys.argv[1],'rb') as tsdata:
        StreamPlus(tsdata)

```

#### ```Pipe a Video to StreamPlus```

```sh
curl -s https://futzu.com/xaa.ts -o - \
| python3 -c 'import sys;import threefive; threefive.StreamPlus(sys.stdin.buffer)'
```
---

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
```

```js
              'Packet': { 'pid': '0x135',              <-- Pid of the SCTE 35 Packet
                          'pts': 89730.289522},        <-- PTS of the SCTE 35 Packet
```

```python3                          
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

 
  
[🡡 top](#threefive)

