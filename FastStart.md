### Up and Running in Less Than 7 Seconds.

* Requires curl, pip3, and python3.


#### Step One of Two

* Estimated time to complete this step : 2.0 - 2.5 seconds

```go
pip install threefive


```



#### Step Two of Two
*  Estimated time to complete this step : 3.0 - 4.5 seconds 
```js
 curl -s https://futzu.com/xaa.ts -o - | python3 -c 'import threefive; threefive.decode()' 
```






* Ouput looks like this.
```js

 Reading from stdin
Start @ 89668.801522
SCTE 35 Packet @ 89730.289522
Splice Info Section
{'table_id': '0xfc', 'section_syntax_indicator': False, 'private': False, 'reserved': 3, 'section_length': 47, 'protocol_version': 0, 'encrypted_packet': False, 'encryption_algorithm': 0, 'pts_adjustment': '0.000000', 'cw_index': '0x0', 'tier': '0xfff', 'splice_command_length': 4095, 'splice_command_type': 5, 'descriptor_loop_length': 10, 'crc': '0x10fa4d9e'}
Splice Command
{'splice_event_id': 662, 'splice_event_cancel_indicator': False, 'out_of_network_indicator': True, 'program_splice_flag': True, 'duration_flag': True, 'splice_immediate_flag': False, 'component_count': None, 'components': [], 'unique_program_id': 1, 'avail_num': 0, 'avail_expected': 0, 'break_auto_return': False, 'break_duration': '242.000000', 'time_specified_flag': True, 'pts_time': '89742.161689', 'name': 'Splice Insert'}
Splice Descriptor 0
{'name': 'Avail Descriptor', 'splice_descriptor_tag': 0, 'descriptor_length': 8, 'identifier': 'CUEI', 'provider_avail_id': 0}

```
