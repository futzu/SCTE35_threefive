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

{ 'Packet': { 'pid': '0x135',
              'pts': 89730.289522},
  'SCTE35': { 'Info_Section': { 'crc': '0x10fa4d9e',
                                'cw_index': '0x0',
                                'descriptor_loop_length': 10,
                                'encrypted_packet': False,
                                'encryption_algorithm': 0,
                                'private': False,
                                'protocol_version': 0,
                                'pts_adjustment': 0.0,
                                'reserved': 3,
                                'section_length': 47,
                                'section_syntax_indicator': False,
                                'splice_command_length': 4095,
                                'splice_command_type': 5,
                                'table_id': '0xfc',
                                'tier': '0xfff'},
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
