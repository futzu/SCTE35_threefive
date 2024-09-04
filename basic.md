# How to Use threefive.Cue

```py3
a@fu:~$ pypy3 
Python 3.9.16 (7.3.11+dfsg-2+deb12u2, May 20 2024, 22:08:06)
[PyPy 7.3.11 with GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>> import threefive
>>>> threefive.version
'2.4.69'
```
* __threefive.Cue__ decodes from  Base64, Integer, Bytes, Hex string, or Hex literal.

```py3
>>>> data ='/DA2AAHOR/nwAAAABQb+PnGRBwAgAh5DVUVJSAAAbH/PAAE1ODcICAAAAAAt86rXNAAAAACwnuYL'
>>>> cue=threefive.Cue(data)
>>>> cue.decode()
True
```
```py3
>>>> data=183300239680257886524837670232596047318548299418173015139317649469035368522983613603709023498560369107202549510766205308206365804540761364
>>>> cue=threefive.Cue(data)
>>>> cue.decode()
True
```
```py3
>>>> data=b'\xfc06\x00\x01\xceG\xf9\xf0\x00\x00\x00\x05\x06\xfe>q\x91\x07\x00 \\x02\x1eCUEIH\x00\x00l\x7f\xcf\x00\x01587\x08\x08\x00\x00\x00\x00-\xf3\xaa\xd74\\x00\x00\x00\x00\xb0\x9e\xe6\x0b'
>>>> cue=threefive.Cue(data)
>>>> cue.decode()
True
```
```py3
>>>> data= '0xfc30360001ce47f9f00000000506fe00a98ac70020021e435545494800006c7fcf00013538370808000000002df3aad73400000000f1e09514'
>>>> cue=threefive.Cue(data)
>>>> cue.decode()
True
```
```py3
>>>> data=0xfc30360001ce47f9f00000000506fe00a98ac70020021e435545494800006c7fcf00013538370808000000002df3aad73400000000f1e09514
>>>> cue=threefive.Cue(data)
>>>> cue.decode()
True
```
* Easy conversion from Base64 to Hex.
```py3
>>>> b64 ='/DA2AAHOR/nwAAAABQb+QZYoVAAgAh5DVUVJSAAAbX/PAAEo0GwICAAAAAAt86rXNAAAAAAfqUZ6'
>>>> cue=threefive.Cue(b64)
>>>> cue.decode()
True
>>>> hexed = cue.encode_as_hex()
>>>> hexed
'0xfc30360001ce47f9f00000000506fe419628540020021e435545494800006d7fcf000128d06c0808000000002df3aad734000000001fa9467a'
>>>> 
```
* __cue.show()__ displays a decoded cue as JSON.

```smalltalk
>>>> cue.show()
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 54,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 86175.453689,
        "cw_index": "0x00",
        "tier": "0x00",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 32,
        "crc": "0xb09ee60b"
    },
    "command": {
        "command_length": 5,
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 11640.3343
    },
    "descriptors": [
        {
            "tag": 2,
            "descriptor_length": 30,
            "name": "Segmentation Descriptor",
            "identifier": "CUEI",
            "segmentation_event_id": "0x4800006c",
            "segmentation_event_cancel_indicator": false,
            "segmentation_event_id_compliance_indicator": true,
            "program_segmentation_flag": true,
            "segmentation_duration_flag": true,
            "delivery_not_restricted_flag": false,
            "web_delivery_allowed_flag": false,
            "no_regional_blackout_flag": true,
            "archive_allowed_flag": true,
            "device_restrictions": "No Restrictions",
            "segmentation_duration": 225.166833,
            "segmentation_message": "Provider Placement Opportunity Start",
            "segmentation_upid_type": 8,
            "segmentation_upid_type_name": "AiringID",
            "segmentation_upid_length": 8,
            "segmentation_upid": "0x2df3aad7",
            "segmentation_type_id": 52,
            "segment_num": 0,
            "segments_expected": 0,
            "sub_segment_num": 0,
            "sub_segments_expected": 0
        }
    ]
}
```

* Access the Cue instance as a whole or by part.
```awk
>>>> cue
```
```js
{'bites': b'\xfc06\x00\x01\xceG\xf9\xf0\x00\x00\x00\x05\x06\xfe>q\x91\x07\x00 \x02\x1eCUEIH\x00\x00l\x7f
\xcf\x00\x01587\x08\x08\x00\x00\x00\x00-\xf3\xaa\xd74\x00\x00\x00\x00\xb0\x9e\xe6\x0b',
 'info_section': {'table_id': '0xfc',
'section_syntax_indicator': False, 'private': False, 'sap_type': '0x03', 'sap_details': 'No Sap Type',
'section_length': 54, 'protocol_version': 0, 'encrypted_packet': False, 'encryption_algorithm': 0,
'pts_adjustment': 86175.453689, 'cw_index': '0x00', 'tier': '0x00', 'splice_command_length': 5,
'splice_command_type': 6, 'descriptor_loop_length': 32, 'crc': '0xb09ee60b'},
'command': {'command_length': 5, 'command_type': 6, 'name': 'Time Signal',
'time_specified_flag': True, 'pts_time': 11640.3343},
'descriptors': [{'tag': 2, 'descriptor_length': 30, 'name': 'Segmentation Descriptor', 'identifier': 'CUEI',
'private_data': None, 'segmentation_event_id': '0x4800006c', 'segmentation_event_cancel_indicator': False,
 'segmentation_event_id_compliance_indicator': True, 'program_segmentation_flag': True,
'segmentation_duration_flag': True, 'delivery_not_restricted_flag': False, 'web_delivery_allowed_flag': False,
 'no_regional_blackout_flag': True, 'archive_allowed_flag': True, 'device_restrictions': 'No Restrictions',
 'segmentation_duration': 225.166833, 'segmentation_message': 'Provider Placement Opportunity Start',
  'segmentation_upid_type': 8, 'segmentation_upid_type_name': 'AiringID', 'segmentation_upid_length': 8,
 'segmentation_upid': '0x2df3aad7', 'segmentation_type_id': 52, 'segment_num': 0, 'segments_expected': 0,
 'sub_segment_num': 0, 'sub_segments_expected': 0}], 'packet_data': None}
```
```py3
>>>> cue.info_section
```
```js
{'table_id': '0xfc', 'section_syntax_indicator': False, 'private': False, 'sap_type': '0x03',
'sap_details': 'No Sap Type', 'section_length': 54, 'protocol_version': 0, 'encrypted_packet': False,
'encryption_algorithm': 0, 'pts_adjustment': 86175.453689, 'cw_index': '0x00', 'tier': '0x00',
'splice_command_length': 5, 'splice_command_type': 6, 'descriptor_loop_length': 32, 'crc': '0xb09ee60b'}
```
```py3
>>>> cue.command
```
```js
{'command_length': 5, 'command_type': 6, 'name': 'Time Signal', 'time_specified_flag': True, 'pts_time': 11640.3343}
```
```
>>>> cue.descriptors[0]
```
```js
{'tag': 2, 'descriptor_length': 30, 'name': 'Segmentation Descriptor', 'identifier': 'CUEI', 'private_data': None,
 'segmentation_event_id': '0x4800006c', 'segmentation_event_cancel_indicator': False,
'segmentation_event_id_compliance_indicator': True, 'program_segmentation_flag': True, 'segmentation_duration_flag': True,
 'delivery_not_restricted_flag': False, 'web_delivery_allowed_flag': True, 'no_regional_blackout_flag': True,
'archive_allowed_flag': True, 'device_restrictions': 'No Restrictions', 'segmentation_duration': 225.166833,
 'segmentation_message': 'Provider Placement Opportunity Start', 'segmentation_upid_type': 8,
 'segmentation_upid_type_name': 'AiringID', 'segmentation_upid_length': 8, 'segmentation_upid': '0x2df3aad7',
 'segmentation_type_id': 52, 'segment_num': 0, 'segments_expected': 0, 'sub_segment_num': 0, 'sub_segments_expected': 0}
```

* Dot notation works as you expect.
```py3
>>>> cue.info_section.pts_adjustment

86175.453689

>>>> cue.info_section.pts_adjustment=5.123

>>>> cue.info_section.pts_adjustmen

5.123

```
```py3
>>>> cue.command.pts_time

11640.3343

>>>> cue.command.pts_time = 123.456789
```
```py3
>>> cue.descriptors[0].segmentation_event_id='0x4800006d'

>>>> cue.descriptors[0].segmentation_event_id

'0x4800006d'
```

* threefive objects have the __has()__ method.
```py3
>>>> cue.has('info_section')
True
```
```py3
>>>> cue.has("fu")
False
```
```py3
>>>> cue.info_section.has('table_id')
True
```
```py3
>>>> cue.command.has('time_specified_flag')
True
```
```py3
>>>> cue.descriptors[0].has("sub_segment_num")
True
```
* A Cue instance can be encoded to Base64, Hex, or Integer.
```py3
>>>> cue.encode()
'/DA2AAHOR/nwAAAABQb+AKmKxwAgAh5DVUVJSAAAbH/PAAE1ODcICAAAAAAt86rXNAAAAADx4JUU'
```
```py3
>>>> cue.encode_as_hex()
'0xfc30360001ce47f9f00000000506fe00a98ac70020021e435545494800006c7fcf00013538370808000000002df3aad73400000000f1e09514'
```
```py3
>>>> cue.encode_as_int()
183300239680257886524837670232596047318548299418173015139317649469035368522983613603709023498560369107202549510766205308206365804540761364
```
* threefive.Cue.bites is the raw bytes of the Cue.
```py3
>>>> cue.bites
b'\xfc06\x00\x01\xceG\xf9\xf0\x00\x00\x00\x05\x06\xfe\x00\xa9\x8a\xc7\x00 \x02\x1eCUEIH\x00\x00l\x7f\xcf\x00\x01587\x08\x08\x00\x00\x00\x00-\xf3\xaa\xd74\x00\x00\x00\x00\xf1\xe0\x95\x14'
```
