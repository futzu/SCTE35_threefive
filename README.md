# `threefive`


## `SCTE35 Decoder Ring` 
* `Parse SCTE 35 messages from Mpeg-ts files.` 
* `Parse SCTE 35 messages encoded in Base64 or Hex.`

### `New Feature`
#### threefive.SHOW_SPLICE_NULL

If you want to surpress displaying Splice Null commands: 
 
* `threefive.SHOW_SPLICE_NULL=False.`

Set it before doing anything else. 
Here's an example:
```go
 python
Python 3.7.4 (default, Jul 16 2019, 07:12:58) 
[GCC 9.1.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import threefive
>>> threefive.SHOW_SPLICE_NULL=False
>>> tf=threefive.parse_tsfile('/home/a/mpegwithscte35.ts')

```

### `Specification`
* https://www.scte.org/SCTEDocs/Standards/ANSI_SCTE%2035%202019r1.pdf

### `Splice Commands`
* `Splice Null`
* `Splice Schedule` (maybe)
* `Splice Insert`
* `Time Signal`
* `Bandwidth Reservation` (maybe)

### `Splice Descriptors`
* `DTMF Descriptor`
* `Segmentation Descriptor` (mostly)
  * `segmentation upid` (some)
  * `segmentation type and messages`
* `Time Descriptor` (maybe)
* `Audio Descriptor`

### `Dependencies`
* Python 3
* bitstring

## `Install`
```go
pip install threefive

Collecting threefive
  Downloading https://files.pythonhosted.org/packages/58/74/c0340db8d85ecd442e2180dc26cb6f11961496b3151e18e80f19026ec331/threefive-1.1.27-py3-none-any.whl
Requirement already satisfied: bitstring in /usr/lib/python3.7/site-packages (from threefive) (3.1.6)
Installing collected packages: threefive
Successfully installed threefive-1.1.27


```
## `Run`

#### `Parse mpegts file`
```go
>>> import threefive
>>> threefive.parse_tsfile('/home/a/mpegwithscte35.ts')

[ Splice Info Section ]
table_id : 0xfc
section_syntax_indicator : False
private : False
section_length : 47
protocol_version : 0
encrypted_packet : False
encryption_algorithm : 0
pts_adjustment : 0.000000
cw_index : 0x0
tier : 0xfff
splice_command_length : 4095
splice_command_type : 5
descriptor_loop_length : 10
crc : 0x10fa4d9e

[ Splice Command ]
splice_type : 5
name : Splice Insert
splice_event_id : 662
splice_event_cancel_indicator : False
out_of_network_indicator : True
program_splice_flag : True
duration_flag : True
splice_immediate_flag : False
time_specified_flag : True
pts_time : 89742.161689
break_auto_return : False
break_duration : 242.000000
unique_program_id : 1
avail_num : 0
avail_expected : 0

[ Splice Descriptor  0  ]
name : Avail Descriptor
splice_descriptor_tag : 0
descriptor_length : 8
identifier : CUEI
provider_avail_id : 0

[ Splice Info Section ]
table_id : 0xfc
section_syntax_indicator : False
private : False
section_length : 42
protocol_version : 0
encrypted_packet : False
encryption_algorithm : 0
pts_adjustment : 0.000000
cw_index : 0x0
tier : 0xfff
splice_command_length : 4095
splice_command_type : 5
descriptor_loop_length : 10
crc : 0x6e33321e

[ Splice Command ]
splice_type : 5
name : Splice Insert
splice_event_id : 662
splice_event_cancel_indicator : False
out_of_network_indicator : False
program_splice_flag : True
duration_flag : False
splice_immediate_flag : False
time_specified_flag : True
pts_time : 89984.161689
unique_program_id : 1
avail_num : 0
avail_expected : 0

[ Splice Descriptor  0  ]
name : Avail Descriptor
splice_descriptor_tag : 0
descriptor_length : 8
identifier : CUEI
provider_avail_id : 0


>>>

```

#### `Parse base64 encoded messages`
```go
>>> import threefive
>>> mesg='/DBhAAAAAAAA///wBQb+qM1E7QBLAhdDVUVJSAAArX+fCAgAAAAALLLXnTUCAAIXQ1VFSUg/nwgIAAAAACyy150RAAACF0NVRUlIAAAnf58ICAAAAAAsstezEAAAihiGnw=='
>>> splice=threefive.Splice(mesg)
>>> splice.show_command()

[ Splice Command ]
splice_type : 6
name : Time Signal
time_specified_flag : True
pts_time : 31466.942367

```
#### `Parse hex encoded messages`
```go
>>> import threefive
>>> mesg= '0xfc3061000000000000fffff00506fea8cd44ed004b021743554549480000ad7f9
f0808000000002cb2d79d350200021743554549480000267f9f0808000000002cb2d79d110000021
743554549480000277f9f0808000000002cb2d7b31000008a18869f'

>>> h_splice=threefive.Splice(mesg)
>>> h_splice.show_info_section() 

[ Splice Info Section ]
table_id : 0xfc
section_syntax_indicator : False
private : False
section_length : 97
protocol_version : 0
encrypted_packet : False
encryption_algorithm : 0
pts_adjustment : 0.000000
cw_index : 0xff
tier : 0xfff
splice_command_length : 5
splice_command_type : 6
descriptor_loop_length : 75
crc : 0x8a18869f

```

## `Methods`

#### `threefive.Splice.show_info_section()`
```python3
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
#### `threefive.Splice.show_command()`
```python3
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
#### `threefive.Splice.show_descriptors()`
```python3
>> import threefive
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

### `threefive.Splice.show()`
#### Shows all data
```python3

>>> import threefive                
>>> mesg='/DBIAAAAAAAA///wBQb+ky44CwAyAhdDVUVJSAAACn+fCAgAAAAALKCh4xgAAAIX
Q1VFSUgAAAl/nwgIAAAAACygoYoRAAC0IX6w')
>>> fu=threefive.Splice(mesg)
>>> fu.show()


[ Splice Info Section ]
table_id : 0xfc
section_syntax_indicator : False
private : False
section_length : 97
protocol_version : 0
encrypted_packet : False
encryption_algorithm : 0
pts_adjustment : 0.000000
cw_index : 0xff
tier : 0xfff
splice_command_length : 5
splice_command_type : 6
descriptor_loop_length : 75
crc : 0x8a18869f

[ Splice Command ]
splice_type : 6
name : Time Signal
time_specified_flag : True
pts_time : 31466.942367

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
### `Read individual values`

```python3
import threefive
mesg='/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo='
scte_data=threefive.Splice(mesg)

>>> scte_data.command.name    
'Splice Insert'
>>> scte_data.command.splice_immediate_flag
False
>>> scte_data.command.pts_time
'21514.559089'
>>> scte_data.command.break_duration
'60.293567'





```
