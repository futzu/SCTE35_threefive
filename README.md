# threefive
## SCTE35 Decoder
* [ Latest Pip Version]( https://pypi.org/project/threefive/)
---
* [Supported Splice Commands](#splice-commands)
* [Supported Splice Descriptors](#splice-descriptors)

* [__Fast Start Directions__](#fast-start-directions)
* [Dependencies](#dependencies)
* [__Install__](#install)

* [__Examples__](https://github.com/futzu/SCTE35-threefive/tree/master/examples)
    * [Splice Insert](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Splice_Insert.py)
    * [Splice Insert Too](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Splice_Insert_Too.py)
    * [Splice Null](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Splice_Null.py)
    * [Time Signal Blackout Override Program End](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Time_Signal_Blackout_Override_Program_End.py)
    * [Time Signal Placement Opportunity Start](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Time_Signal-Placement_Opportunity_Start.py)
    * [Time Signal Placement Opportunity End](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Time_Signal-Placement_Opportunity_End.py)
    * [Time Signal Program Overlap ](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Time_Signal-Program_Overlap.py)
    * [Time Signal Program Start End](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Time_Signal-Program_Start_End.py)
    * [Sub Class Example](https://github.com/futzu/SCTE35-threefive/blob/master/examples/streamstats.py)

* [__Easy threefive__](#easy-threefive)
  *   [The __decode__ Function](#the-decode-function)
      * [Parsing SCTE 35 messages from Mpeg Transport Streams and Binary files](#mpegts)
        * [Output for MpegTS and Binary Files and Streams](#json-output-for-mpegts-and-binary-files-and-streams)
      * [Parsing SCTE 35 messages encoded in Base64, Binary, or Hex](#base64-encoded-strings)
        * [Output for Base64 and Hex Strings](#json-output-for-base64-and-hex-strings)

* [__Advanced threefive__](#advanced-threefive)
  *   [__Splice Class__](#splice-class)
      * [JSON Pretty Print SCTE 35 Message](#json-pretty-print-scte-35-message)
      * [Return SCTE 35 Message](#return-scte-35-message)
      * [JSON Pretty Print Splice Info Section](#json-pretty-print-splice-info-section)
      * [Return Splice Info Section](#return-splice-info-section)
      * [JSON Pretty Print Splice Command](#json-pretty-print-splice-command)
      * [Return Splice Command](#return-splice-command)
      * [JSON Pretty Print Splice Descriptors](#json-pretty-print-splice-descriptors)
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
  *  Segmentation Descriptor (all segmentation_upids) 
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
#####  git  
```sh
git clone https://github.com/futzu/SCTE35-threefive.git

cd SCTE-threefive

# you need root to install for the system
make install
```
---
```
...
Processing threefive-2.1.39-py3.8.egg
Copying threefive-2.1.39-py3.8.egg to /usr/local/lib/python3.8/dist-packages
Adding threefive 2.1.39 to easy-install.pth file

Installed /usr/local/lib/python3.8/dist-packages/threefive-2.1.39-py3.8.egg
Processing dependencies for threefive==2.1.39
Searching for bitn==0.0.27
Best match: bitn 0.0.27
Processing bitn-0.0.27-py3.8.egg
bitn 0.0.27 is already the active version in easy-install.pth

Using /usr/local/lib/python3.8/dist-packages/bitn-0.0.27-py3.8.egg
Finished processing dependencies for threefive==2.1.39

```

##### pip3
```sh
pip3 install threefive
```
---

```
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

####    ```JSON Output for MpegTS and Binary Files and Streams```
```python3
{
        "SCTE35": {
                "Info_Section": {
                        "table_id": "0xfc",
                        "section_syntax_indicator": false,
                        "private": false,
                        "reserved": "0x3",
                        "section_length": 47,
                        "protocol_version": 0,
                        "encrypted_packet": false,
                        "encryption_algorithm": 0,
                        "pts_adjustment": 0.0,
                        "cw_index": "0x0",
                        "tier": "0xfff",
                        "splice_command_length": 20,
                        "splice_command_type": 5,
                        "descriptor_loop_length": 10,
                        "crc": "0x10fa4d9e"
                },
                "Splice_Command": {
                        "name": "Splice Insert",
                        "splice_event_id": 662,
                        "splice_event_cancel_indicator": false,
                        "out_of_network_indicator": true,
                        "program_splice_flag": true,
                        "duration_flag": true,
                        "splice_immediate_flag": false,
                        "time_specified_flag": true,
                        "pts_time": 89742.161689,
                        "break_auto_return": false,
                        "break_duration": 242.0,
                        "unique_program_id": 1,
                        "avail_num": 0,
                        "avail_expected": 0,
                        "splice_command_length": 20
                },
                "Splice_Descriptors": [
                        {
                                "tag": 0,
                                "identifier": "CUEI",
                                "name": "Avail Descriptor",
                                "provider_avail_id": 0,
                                "descriptor_length": 8
                        }
                ]
        }
}


{
        "SCTE35": {
                "Info_Section": {
                        "table_id": "0xfc",
                        "section_syntax_indicator": false,
                        "private": false,
                        "reserved": "0x3",
                        "section_length": 42,
                        "protocol_version": 0,
                        "encrypted_packet": false,
                        "encryption_algorithm": 0,
                        "pts_adjustment": 0.0,
                        "cw_index": "0x0",
                        "tier": "0xfff",
                        "splice_command_length": 15,
                        "splice_command_type": 5,
                        "descriptor_loop_length": 10,
                        "crc": "0x6e33321e"
                },
                "Splice_Command": {
                        "name": "Splice Insert",
                        "splice_event_id": 662,
                        "splice_event_cancel_indicator": false,
                        "out_of_network_indicator": false,
                        "program_splice_flag": true,
                        "duration_flag": false,
                        "splice_immediate_flag": false,
                        "time_specified_flag": true,
                        "pts_time": 89984.161689,
                        "unique_program_id": 1,
                        "avail_num": 0,
                        "avail_expected": 0,
                        "splice_command_length": 15
                },
                "Splice_Descriptors": [
                        {
                                "tag": 0,
                                "identifier": "CUEI",
                                "name": "Avail Descriptor",
                                "provider_avail_id": 0,
                                "descriptor_length": 8
                        }
                ]
        }
}

```
####  ```Base64 Encoded Strings```
```python
mesg='/DBUAAAAAAAA///wBQb+AAAAAAA+AjxDVUVJAAAACn+/Dy11cm46dXVpZDphYTg1YmJiNi01YzQzLTRiNmEtYmViYi1lZTNiMTNlYjc5OTkRAAB2c6LA'
threefive.decode(mesg)
```
#### ```Hex Encoded Strings```
```python
hexed='0xFC302F000000000000FFFFF014054800008F7FEFFE7369C02EFE0052CCF500000000000A0008435545490000013562DBA30A'
threefive.decode(hexed)
```

#### ```JSON Output for Base64 and Hex Strings```

```python3

{
    "SCTE35": {
        "Info_Section": {
            "table_id": "0xfc",
            "section_syntax_indicator": false,
            "private": false,
            "reserved": "0x3",
            "section_length": 84,
            "protocol_version": 0,
            "encrypted_packet": false,
            "encryption_algorithm": 0,
            "pts_adjustment": 0.0,
            "cw_index": "0xff",
            "tier": "0xfff",
            "splice_command_length": 5,
            "splice_command_type": 6,
            "descriptor_loop_length": 62,
            "crc": "0x7673a2c0"
        },
        "Splice_Command": {
            "name": "Time Signal",
            "time_specified_flag": true,
            "pts_time": 0.0
        },
        "Splice_Descriptors": [
            {
                "tag": 2,
                "identifier": "CUEI",
                "name": "Segmentation Descriptor",
                "segmentation_event_id": "0xa",
                "segmentation_event_cancel_indicator": false,
                "program_segmentation_flag": true,
                "segmentation_duration_flag": false,
                "delivery_not_restricted_flag": true,
                "segmentation_upid_type": 15,
                "segmentation_upid_length": 45,
                "segmentation_upid": "URI:urn:uuid:aa85bbb6-5c43-4b6a-bebb-ee3b13eb7999",
                "segmentation_type_id": 17,
                "segmentation_message": "Program End",
                "segment_num": 0,
                "segments_expected": 0,
                "descriptor_length": 60
            }
        ]
    }
}

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
#### ```JSON Pretty Print SCTE 35 Message```
```python
scte35.show()
```

#### ```Return SCTE 35 Message```
```python
scte35.get()
```

#### ```JSON Pretty Print Splice Info Section```
```python
scte35.show_info_section()
```

#### ```Return Splice Info Section```
```python
scte35.get_info_section()

```        
#### ```JSON Pretty Print Splice Command```
```python
scte35.show_command()

```

#### ```Return Splice Command```
```python
scte35.get_command()

``` 

#### ```JSON Pretty Print Splice Descriptors```
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
{
        "SCTE35": {
                "Info_Section": {
                        "table_id": "0xfc",
                        "section_syntax_indicator": false,
                        "private": false,
                        "reserved": "0x3",
                        "section_length": 47,
                        "protocol_version": 0,
                        "encrypted_packet": false,
                        "encryption_algorithm": 0,
                        "pts_adjustment": 0.0,
                        "cw_index": "0x0",
                        "tier": "0xfff",
                        "splice_command_length": 20,
                        "splice_command_type": 5,
                        "descriptor_loop_length": 10,
                        "crc": "0x10fa4d9e"
                },
                "Splice_Command": {
                        "name": "Splice Insert",
                        "splice_event_id": 662,
                        "splice_event_cancel_indicator": false,
                        "out_of_network_indicator": true,
                        "program_splice_flag": true,
                        "duration_flag": true,
                        "splice_immediate_flag": false,
                        "time_specified_flag": true,
                        "pts_time": 89742.161689,
                        "break_auto_return": false,
                        "break_duration": 242.0,
                        "unique_program_id": 1,
                        "avail_num": 0,
                        "avail_expected": 0,
                        "splice_command_length": 20
                },
                "Splice_Descriptors": [
                        {
                                "tag": 0,
                                "identifier": "CUEI",
                                "name": "Avail Descriptor",
                                "provider_avail_id": 0,
                                "descriptor_length": 8
                        }
                ]
        }
}

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
    
   * __threefive.StreamPlus__ adds the PID and PTS timestamp for each SCTE 35 packet.

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
 
{
        "SCTE35": {
                "Info_Section": {
                        "table_id": "0xfc",
                        "section_syntax_indicator": false,
                        "private": false,
                        "reserved": "0x3",
                        "section_length": 47,
                        "protocol_version": 0,
                        "encrypted_packet": false,
                        "encryption_algorithm": 0,
                        "pts_adjustment": 0.0,
                        "cw_index": "0x0",
                        "tier": "0xfff",
                        "splice_command_length": 20,
                        "splice_command_type": 5,
                        "descriptor_loop_length": 10,
                        "crc": "0x10fa4d9e"
                },
                "Splice_Command": {
                        "name": "Splice Insert",
                        "splice_event_id": 662,
                        "splice_event_cancel_indicator": false,
                        "out_of_network_indicator": true,
                        "program_splice_flag": true,
                        "duration_flag": true,
                        "splice_immediate_flag": false,
                        "time_specified_flag": true,
                        "pts_time": 89742.161689,
                        "break_auto_return": false,
                        "break_duration": 242.0,
                        "unique_program_id": 1,
                        "avail_num": 0,
                        "avail_expected": 0,
                        "splice_command_length": 20
                },
                "Splice_Descriptors": [
                        {
                                "tag": 0,
                                "identifier": "CUEI",
                                "name": "Avail Descriptor",
                                "provider_avail_id": 0,
                                "descriptor_length": 8
                        }
                ],
                "Packet_Data": {
                        "pid": "0x135",       <--- Packet PID
                        "pts": 89730.289522   <---- Packet PTS
                }
        }
}


```
[🡡 top](#threefive)

