# threefive


## SCTE35 parsing. 


### The Spec
* https://www.scte.org/SCTEDocs/Standards/ANSI_SCTE%2035%202019r1.pdf


## Dependencies
* Python 3
* bitstring

## Install and Run
```python3
so# pip install threefive   
Collecting bitstring
 ...
Collecting threefive
 ...
Installing collected packages: bitstring, threefive
Successfully installed bitstring-3.1.6 threefive-1.0.93

so# python3                         
Python 3.6.8 (default, Apr 13 2019, 18:58:09) 
[GCC 4.2.1 Compatible OpenBSD Clang 7.0.1 (tags/RELEASE_701/final)] on openbsd6

>>> import threefive    
>>> mesg='/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo='
>>> splice=threefive.Splice(mesg)
>>> splice.show_descriptors()

[ Splice Descriptor  0  ]
name : Avail Descriptor
splice_descriptor_tag : 0
descriptor_length : 8
identifier : CUEI
provider_avail_id : 309

>>> 

```


#### Parse base64 encoded messages
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
#### Parse hex encoded messages
```python3
>>> import threefive
>>> mesg= '0xfc3061000000000000fffff00506fea8cd44ed004b021743554549480000ad7f9f0808000000002cb2d79d350200021743554549480000267f9f0808000000002cb2d79d110000021743554549480000277f9f0808000000002cb2d7b31000008a18869f'
>>> h_splice=threefive.Splice(mesg)
>>> h_splice.show_info_section() 

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

## Methods
#### threefive.Splice.show_info_section()
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
#### threefive.Splice.show_command()
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
#### threefive.Splice.show_descriptors()
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
segment_num : 0
segments_expected : 0

```

### threefive.Splice.show()
#### Shows all data
```python3

>>> import threefive                
>>> mesg='/DBIAAAAAAAA///wBQb+ky44CwAyAhdDVUVJSAAACn+fCAgAAAAALKCh4xgAAAIXQ1VFSUgAAAl/nwgIAAAAACygoYoRAAC0IX6w')
>>> fu=threefive.Splice(mesg)
>>> fu.show()

[ Splice Info Section ]
table_id : 0xfc
section_syntax_indicator : False
private : False
reserved : 3
section_length : 72
protocol_version : 0
encrypted_packet : False
encryption_algorithm : 0
pts_adjustment : 0
cw_index : 0xff
tier : 0xfff
splice_command_length : 5
splice_command_type : 6
descriptor_loop_length : 50

[ Splice Command ]
splice_type : 6
name : Time Signal
time_specified_flag : True
pts_time : 27436.441722

[ Splice Descriptor  0  ]
name : Segmentation Descriptor
splice_descriptor_tag : 2
descriptor_length : 23
identifier : CUEI
segmentation_event_id : 0x4800000a
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
turner_identifier : 0x000000002ca0a1e3
segmentation_type_id : 24
segment_num : 0
segments_expected : 0

[ Splice Descriptor  1  ]
name : Segmentation Descriptor
splice_descriptor_tag : 2
descriptor_length : 23
identifier : CUEI
segmentation_event_id : 0x48000009
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
turner_identifier : 0x000000002ca0a18a
segmentation_type_id : 17
segment_num : 0
segments_expected : 0

```
### Read individual values

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
