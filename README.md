# threefive

## SCTE35 Decoder
*  Parse SCTE 35 messages from Mpeg Transport Streams and Binary files. 
*  Parse SCTE 35 messages encoded in Base64, Binary, or Hex. 

### 2019 Specification ( Link is down )
[SCTE35 2019 specification](https://www.scte.org/standard/scte-35-2019/)

###  Splice Commands 
*  Splice Null  
*  Splice Schedule  (lightly tested)
*  Splice Insert 
*  Time Signal 
*  Bandwidth Reservation  (lightly tested)

###  Splice Descriptors 
*  DTMF Descriptor 
*  Segmentation Descriptor
  *  Segmentation UPID  (partially implemented)
  *  Segmentation Types and Messages 
*  Time Descriptor 
*  Audio Descriptor (lightly tested)

###  Dependencies 
* Python 3
* bitn

##  Install 
```
pip install threefive
Collecting threefive
  Downloading threefive-2.0.35-py3-none-any.whl (12 kB)
Collecting bitn>=0.0.15
  Downloading bitn-0.0.15-py3-none-any.whl (3.0 kB)
Installing collected packages: bitn, threefive
Successfully installed bitn-0.0.15 threefive-2.0.35

```

 ## Fast Start 
 
* Immediate Gratification
 
* pip
```python
pip install threefive
```
* Create a file call it cli.py, and put the following in it.
 ```sh
 #!/usr/bin/env python3

import sys
import threefive
 
def do():
    try: 
        threefive.decode(sys.argv[1])
    except: 
        # Handles piped in data
        try: threefive.decode()
        except: pass

do()   
```
* chmod cli.py
```bash
chmod +x cli.py
```
* Parse SCTE 35 and PTS data from a video over the network( requires curl )
```bash
 curl -s https://futzu.com/mpegwithscte35.ts -o - | ./cli.py 
```


##  Using threefive  
#### Call threefive.decode.

 *  mpegts files
 *  binary files
 *  base64 encoded strings
 *  hex encoded strings
 *  binary byte strings
 

 ####  Parse mpegts files 
```python
>>> import threefive
>>> threefive.decode('/path/to/mpegwithscte35.ts') 
```

####  Parse binary encoded messages from a file
```python
>>> import threefive
>>> stuff=threefive.decode('/mnt/build/file.bin')
```

####  Parse base64 encoded messages 
```python
>>> import threefive
>>> mesg='/DBhAAAAAAAA///wBQb+qM1E7QBLAhdDVUVJSAAArX+fCAgAAAAALLLXnTUCAAIXQ1VFSUg/nwgIAAAAACyy150RAAACF0NVRUlIAAAnf58ICAAAAAAsstezEAAAihiGnw=='
>>> t=threefive.decode(mesg)
```

####  Parse hex encoded messages 

```python
>>> import threefive
>>> u=threefive.decode('0xFC302F000000000000FFFFF014054800008F7FEFFE7369C02EFE0052CCF500000000000A0008435545490000013562DBA30A')
```

#### Parse binary byte string messages
```python
>>> import threefive
>>> f=open('/mnt/build/file.bin','rb').read()
>>> scte35=threefive.decode(f)
```

### Output looks like this
```python
[SCTE 35 Message]

 Splice Info Section:
table_id :0xfc  section_syntax_indicator :False  private :False  reserved :3  section_length :47  protocol_version :0  encrypted_packet :False  encryption_algorithm :0  pts_adjustment :0.000000  cw_index :0x0  tier :0xfff  splice_command_length :4095  splice_command_type :5  descriptor_loop_length :10  crc :0x10fa4d9e 

 Splice Command:
splice_type :5  name :Splice Insert  splice_event_id :662  splice_event_cancel_indicator :False  out_of_network_indicator :True  program_splice_flag :True  duration_flag :True  splice_immediate_flag :False  time_specified_flag :True  pts_time :89742.161689  break_auto_return :False  break_duration :242.000000  unique_program_id :1  avail_num :0  avail_expected :0 

 Splice Descriptor 0:
name :Avail Descriptor  splice_descriptor_tag :0  descriptor_length :8  identifier :CUEI  provider_avail_id :0 

[  SCTE 35 Stream found with Pid 0x135  ]
```
### Output for Mpegts streams and files
```js
PTS 89730.290 

[SCTE 35 Message]
Splice Info Section
{"table_id": "0xfc", "section_syntax_indicator": false, "private": false, "reserved": 3, "section_length": 47, "protocol_version": 0, "encrypted_packet": false, "encryption_algorithm": 0, "pts_adjustment": "0.000000", "cw_index": "0x0", "tier": "0xfff", "splice_command_length": 4095, "splice_command_type": 5, "descriptor_loop_length": 10, "crc": "0x10fa4d9e"}
Splice Command
{"name": "Splice Insert", "splice_event_id": 662, "splice_event_cancel_indicator": false, "out_of_network_indicator": true, "program_splice_flag": true, "duration_flag": true, "splice_immediate_flag": false, "time_specified_flag": true, "pts_time": "89742.161689", "break_auto_return": false, "break_duration": "242.000000", "unique_program_id": 1, "avail_num": 0, "avail_expected": 0}
Splice Descriptor 0
{"name": "Avail Descriptor", "splice_descriptor_tag": 0, "descriptor_length": 8, "identifier": "CUEI", "provider_avail_id": 0}

PTS 89730.290 

[SCTE 35 Message]
Splice Info Section
{"table_id": "0xfc", "section_syntax_indicator": false, "private": false, "reserved": 3, "section_length": 47, "protocol_version": 0, "encrypted_packet": false, "encryption_algorithm": 0, "pts_adjustment": "0.000000", "cw_index": "0x0", "tier": "0xfff", "splice_command_length": 4095, "splice_command_type": 5, "descriptor_loop_length": 10, "crc": "0x10fa4d9e"}
Splice Command
{"name": "Splice Insert", "splice_event_id": 662, "splice_event_cancel_indicator": false, "out_of_network_indicator": true, "program_splice_flag": true, "duration_flag": true, "splice_immediate_flag": false, "time_specified_flag": true, "pts_time": "89742.161689", "break_auto_return": false, "break_duration": "242.000000", "unique_program_id": 1, "avail_num": 0, "avail_expected": 0}
Splice Descriptor 0
{"name": "Avail Descriptor", "splice_descriptor_tag": 0, "descriptor_length": 8, "identifier": "CUEI", "provider_avail_id": 0}

PTS 89977.250 

[SCTE 35 Message]
Splice Info Section
{"table_id": "0xfc", "section_syntax_indicator": false, "private": false, "reserved": 3, "section_length": 42, "protocol_version": 0, "encrypted_packet": false, "encryption_algorithm": 0, "pts_adjustment": "0.000000", "cw_index": "0x0", "tier": "0xfff", "splice_command_length": 4095, "splice_command_type": 5, "descriptor_loop_length": 10, "crc": "0x6e33321e"}
Splice Command
{"name": "Splice Insert", "splice_event_id": 662, "splice_event_cancel_indicator": false, "out_of_network_indicator": false, "program_splice_flag": true, "duration_flag": false, "splice_immediate_flag": false, "time_specified_flag": true, "pts_time": "89984.161689", "unique_program_id": 1, "avail_num": 0, "avail_expected": 0}
Splice Descriptor 0
{"name": "Avail Descriptor", "splice_descriptor_tag": 0, "descriptor_length": 8, "identifier": "CUEI", "provider_avail_id": 0}

PTS 90042.338 

[SCTE 35 Message]
Splice Info Section
{"table_id": "0xfc", "section_syntax_indicator": false, "private": false, "reserved": 3, "section_length": 78, "protocol_version": 0, "encrypted_packet": false, "encryption_algorithm": 0, "pts_adjustment": "0.000000", "cw_index": "0x0", "tier": "0xfff", "splice_command_length": 5, "splice_command_type": 6, "descriptor_loop_length": 60, "crc": "0x54590000"}
Splice Command
{"name": "Time Signal", "time_specified_flag": true, "pts_time": "0.555556"}
Splice Descriptor 0
{"name": "Segmentation Descriptor", "splice_descriptor_tag": 2, "descriptor_length": 58, "identifier": "CUEI", "segmentation_event_id": "0x3", "segmentation_event_cancel_indicator": false, "program_segmentation_flag": true, "segmentation_duration_flag": true, "delivery_not_restricted_flag": true, "segmentation_duration": "0.000178", "segmentation_upid_type": 12, "segmentation_type_id": 38, "segmentation_message": "Closing Credit Start", "segment_num": 76, "segments_expected": 66}
```



##  Splice Methods
####  threefive.Splice.show_info_section() 
```python
>>> import threefive
>>> mesg='/DBhAAAAAAAA///wBQb+qM1E7QBLAhdDVUVJSAAArX+fCAgAAAAALLLXnTUCAAIXQ1VFSUgAACZ/nwgIAAAAACyy150RAAACF0NVRUlIAAAnf58ICAAAAAAsstezEAAAihiGnw=='
>>> splice=threefive.Splice(mesg)
>>> splice.show_info_section()

[ Splice Info Section ]
table_id : 0xfc
section_syntax_indicator : False
private : False
reserved : 3
section_length : 97
protocol_version : 0
encrypted_packet : False
encryption_algorithm : 0
pts_adjustment : 0
cw_index : 0xff
tier : 0xfff
splice_command_length : 5
splice_command_type : 6
descriptor_loop_length : 75

```
####  threefive.Splice.show_command() 
```python
>>> import threefive
>>> mesg='/DBhAAAAAAAA///wBQb+qM1E7QBLAhdDVUVJSAAArX+fCAgAAAAALLLXnTUCAAIXQ1VFSUgAACZ/nwgIAAAAACyy150RAAACF0NVRUlIAAAnf58ICAAAAAAsstezEAAAihiGnw=='
>>> splice=threefive.Splice(mesg)
>>> splice.show_command()

[ Splice Command ]
splice_type : 6
name : Time Signal
time_specified_flag : True
pts_time : 31466.942367

```

####  threefive.Splice.show_descriptors()
##### Multiple splice descriptors per splice command are supported. 
```python
>>> import threefive
>>> mesg='/DBhAAAAAAAA///wBQb+qM1E7QBLAhdDVUVJSAAArX+fCAgAAAAALLLXnTUCAAIXQ1VFSUgAACZ/nwgIAAAAACyy150RAAACF0NVRUlIAAAnf58ICAAAAAAsstezEAAAihiGnw=='
>>> stuff=threefive.Splice(mesg)
>>> stuff.show_descriptors()

[ Splice Descriptor  0  ]
name : Segmentation Descriptor
splice_descriptor_tag : 2
descriptor_length : 23
identifier : CUEI
segmentation_event_id : 0x480000ad
segmentation_event_cancel_indicator : False
program_segmentation_flag : True
segmentation_duration_flag : False
delivery_not_restricted_flag : False
web_delivery_allowed_flag : True
no_regional_blackout_flag : True
archive_allowed_flag : True
device_restrictions : 0x3
segmentation_upid_type : 8
segmentation_upid_length : 8
turner_identifier : 0x000000002cb2d79d
segmentation_type_id : 53
segmentation_type : Provider Placement Opportunity End
segment_num : 2
segments_expected : 0

[ Splice Descriptor  1  ]
name : Segmentation Descriptor
splice_descriptor_tag : 2
descriptor_length : 23
identifier : CUEI
segmentation_event_id : 0x48000026
segmentation_event_cancel_indicator : False
program_segmentation_flag : True
segmentation_duration_flag : False
delivery_not_restricted_flag : False
web_delivery_allowed_flag : True
no_regional_blackout_flag : True
archive_allowed_flag : True
device_restrictions : 0x3
segmentation_upid_type : 8
segmentation_upid_length : 8
turner_identifier : 0x000000002cb2d79d
segmentation_type_id : 17
segmentation_type : Program End
segment_num : 0
segments_expected : 0

[ Splice Descriptor  2  ]
name : Segmentation Descriptor
splice_descriptor_tag : 2
descriptor_length : 23
identifier : CUEI
segmentation_event_id : 0x48000027
segmentation_event_cancel_indicator : False
program_segmentation_flag : True
segmentation_duration_flag : False
delivery_not_restricted_flag : False
web_delivery_allowed_flag : True
no_regional_blackout_flag : True
archive_allowed_flag : True
device_restrictions : 0x3
segmentation_upid_type : 8
segmentation_upid_length : 8
turner_identifier : 0x000000002cb2d7b3
segmentation_type_id : 16
segmentation_type : Program Start
segment_num : 0
segments_expected : 0
```

###  threefive.Splice.show() 
#### Shows all data
```python
>>> import threefive                
>>> mesg='/DBIAAAAAAAA///wBQb+ky44CwAyAhdDVUVJSAAACn+fCAgAAAAALKCh4xgAAAIX
Q1VFSUgAAAl/nwgIAAAAACygoYoRAAC0IX6w')
>>> fu=threefive.Splice(mesg)
>>> fu.show()
```

###  Read individual values 
```python
>>> import threefive
>>> mesg='/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo='
>>> scte_data=threefive.Splice(mesg)
>>> scte_data.command.name    
'Splice Insert'
>>> scte_data.command.splice_immediate_flag
False
>>> scte_data.command.pts_time
'21514.559089'
>>> scte_data.command.break_duration
'60.293567'
```
