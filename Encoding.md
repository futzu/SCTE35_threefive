# Encoding ( Requires threefive 2.3.02+ )


#### threefive.**Cue()**

###### A decoded __Cue__ instance contains: 

* **cue.info_section** 1 [threefive.**SpliceInfoSection()**](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/section.py)

* **cue.command** 1 command
      
    * commands: [ threefive.**BandwidthReservation()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L32)  |    [ threefive.**PrivateCommand()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L54)  |    [ threefive.**SpliceInsert()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L139)  |    [ threefive.**SpliceNull()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L43)  |    [ threefive.**TimeSignal()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L84)

* **cue.descriptors** a list of 0 or more descriptors

    * descriptors :    [ threefive.**AudioDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L153)  | 
        [ threefive.**AvailDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L50)  | 
        [ threefive.**DtmfDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L78)  | 
        [ threefive.**SegmentationDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L201)  | 
        [threefive.**TimeDescriptor()**](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L119)

###### All instance vars can be accessed via dot notation.

### Automatic Features

* Splice Info Section of the Cue is automatically generated. 
* length vars for Cue.command and Cue.descriptors are automatically generated.  
* Descriptor loop length and crc32 are automatically calculated 

## Examples

### Edit the Splice Insert Command in a Cue 
```python3
a@fumatica:~/threefive$ pypy3
Python 3.7.10 (7.3.5+dfsg-2, Jun 03 2021, 20:39:46)
[PyPy 7.3.5 with GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>> import threefive
>>>> Base64 = "/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo="
>>>> cue = threefive.Cue(Base64)
>>>> cue.decode()
True
>>>> cue.command
{'calculated_length': 20, 'command_type': 5, 'name': 'Splice Insert', 'time_specified_flag': True, 'pts_time': 21514.559089, 'break_auto_return': True, 'break_duration': 60.293567, 'splice_event_id': 1207959695, 'splice_event_cancel_indicator': False, 'out_of_network_indicator': True, 'program_splice_flag': True, 'duration_flag': True, 'splice_immediate_flag': False, 'component_count': None, 'components': None, 'unique_program_id': 0, 'avail_num': 0, 'avail_expected': 0}


# Access vars with dot notation

>>>> cue.command.break_duration= 90.0

# re-encode

>>>> cue.encode()
'/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4Ae5igAAAAAAAKAAhDVUVJAAABNVB2fJs='
>>>> 
>>>> cue.show()
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x3",
        "sap_details": "No Sap Type",
        "section_length": 47,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0xff",
        "tier": "0xfff",
        "splice_command_length": 20,
        "splice_command_type": 5,
        "descriptor_loop_length": 10,
        "crc": "0x62dba30a"
    },
    "command": {
        "calculated_length": 20,
        "command_type": 5,
        "name": "Splice Insert",
        "time_specified_flag": true,
        "pts_time": 21514.559089,
        "break_auto_return": true,
        "break_duration": 90.0,
        "splice_event_id": 1207959695,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": false,
        "unique_program_id": 0,
        "avail_num": 0,
        "avail_expected": 0
    },
    "descriptors": [
        {
            "tag": 0,
            "descriptor_length": 8,
            "name": "Avail Descriptor",
            "identifier": "CUEI",
            "provider_avail_id": 309
        }
    ]
}
```
### Remove a Splice Descriptor in a Cue
```python3
>>>> import threefive
>>>> Base64 = "/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo="
>>>> cue = threefive.Cue(Base64)
>>>> cue.decode()
True
>>>> cue.show()
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x3",
        "sap_details": "No Sap Type",
        "section_length": 47,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0xff",
        "tier": "0xfff",
        "splice_command_length": 20,
        "splice_command_type": 5,
        "descriptor_loop_length": 10,
        "crc": "0x62dba30a"
    },
    "command": {
        "calculated_length": 20,
        "command_type": 5,
        "name": "Splice Insert",
        "time_specified_flag": true,
        "pts_time": 21514.559089,
        "break_auto_return": true,
        "break_duration": 60.293567,
        "splice_event_id": 1207959695,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": false,
        "unique_program_id": 0,
        "avail_num": 0,
        "avail_expected": 0
    },
    "descriptors": [
        {
            "tag": 0,
            "descriptor_length": 8,
            "name": "Avail Descriptor",
            "identifier": "CUEI",
            "provider_avail_id": 309
        }
    ]
}

# delete the descriptor from descriptors

>>>> del cue.descriptors[0]

# re-encode 

>>>> cue.encode()
'/DAlAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAAYinJUA=='
>>>> cue.show()
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x3",
        "sap_details": "No Sap Type",
        "section_length": 37,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0xff",
        "tier": "0xfff",
        "splice_command_length": 20,
        "splice_command_type": 5,
        "descriptor_loop_length": 0,
        "crc": "0x6229c950"
    },
    "command": {
        "calculated_length": 20,
        "command_type": 5,
        "name": "Splice Insert",
        "time_specified_flag": true,
        "pts_time": 21514.559089,
        "break_auto_return": true,
        "break_duration": 60.293567,
        "splice_event_id": 1207959695,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": false,
        "unique_program_id": 0,
        "avail_num": 0,
        "avail_expected": 0,
        "command_length": 20
    },
    "descriptors": []
}

```
### Add a Dtmf Descriptor to an existing Cue
```python3
>>>> import threefive
>>>> Base64 = "/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo="
>>>> cue = threefive.Cue(Base64)
>>>> cue.decode()
True
>>>> dscrptr = threefive.DtmfDescriptor()
>>>> dscrptr
{'tag': 1, 'descriptor_length': 0, 'identifier': None, 'bites': None, 'name': 'DTMF Descriptor', 'preroll': None, 'dtmf_count': None, 'dtmf_chars': []}

 # My data to load into the DtmfDescriptor instance

>>>> data = {'tag': 1, 'descriptor_length': 10, 'identifier': 'CUEI', 'name': 'DTMF Descriptor', 'preroll': 177, 'dtmf_count': 4, 'dtmf_chars': ['1'\
, '2', '1', '#']}

 #  All Splice Commands and Descriptors have a load method


>>>> dscrptr.load(data)

>>>> dscrptr
{'tag': 1, 'descriptor_length': 10, 'identifier': 'CUEI', 'bites': None, 'name': 'DTMF Descriptor', 'preroll': 177, 'dtmf_count': 4, 'dtmf_chars': ['1', '2', '1', '#']}


  # Append to cue.descrptors


>>>> cue.descriptors.append(dscrptr)
  # Run encode to generate new Base64 string
>>>> cue.encode()
b'/DA7AAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAWAAhDVUVJAAABNQEKQ1VFSbGfMTIxI55FecI='
```

## Cue with a Time Signal Command from scratch

```python3
>>>> import threefive
>>>> cue = threefive.Cue()
>>>> cue
{'info_section': {'table_id': None, 'section_syntax_indicator': None, 'private': None, 'sap_type': None, 'sap_details': None, 'section_length': None, 'protocol_version': None, 'encrypted_packet': None, 'encryption_algorithm': None, 'pts_adjustment': None, 'cw_index': None, 'tier': None, 'splice_command_length': None, 'splice_command_type': None, 'descriptor_loop_length': 0, 'crc': None}, 'command': None, 'descriptors': [], 'packet_data': None}
>>>> cmd=threefive.TimeSignal()
>>>> cmd
{'calculated_length': None, 'command_type': 6, 'name': 'Time Signal', 'bites': None, 'time_specified_flag': None, 'pts_time': None}
>>>> cmd.time_specified_flag=True
>>>> cmd.pts_time=20.004350
>>>> cue.command=cmd
>>>> cue
{'info_section': {'table_id': None, 'section_syntax_indicator': None, 'private': None, 'sap_type': None, 'sap_details': None, 'section_length': None, 'protocol_version': None, 'encrypted_packet': None, 'encryption_algorithm': None, 'pts_adjustment': None, 'cw_index': None, 'tier': None, 'splice_command_length': None, 'splice_command_type': None, 'descriptor_loop_length': 0, 'crc': None}, 'command': {'calculated_length': None, 'command_type': 6, 'name': 'Time Signal', 'bites': None, 'time_specified_flag': True, 'pts_time': 20.00435}, 'descriptors': [], 'packet_data': None}
>>>> cue.encode()
'/DAWAAAAAAAAAP/wBQb+ABt4xwAAwhCGHw=='
>>>> cue
{'info_section': {'table_id': '0xfc', 'section_syntax_indicator': False, 'private': False, 'sap_type': '0x3', 'sap_details': 'No Sap Type', 'section_length': 22, 'protocol_version': 0, 'encrypted_packet': False, 'encryption_algorithm': 0, 'pts_adjustment': 0.0, 'cw_index': '0x0', 'tier': '0xfff', 'splice_command_length': 5, 'splice_command_type': 6, 'descriptor_loop_length': 0, 'crc': '0xc210861f'}, 'command': {'calculated_length': None, 'command_type': 6, 'name': 'Time Signal', 'bites': None, 'time_specified_flag': True, 'pts_time': 20.00435, 'command_length': 5}, 'descriptors': [], 'bites': b'\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\x1bx\xc7\x00\x00\xc2\x10\x86\x1f', 'packet_data': None}
>>>> cue.show()

# Splice Info Section is Automatically calculated 

{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x3",
        "sap_details": "No Sap Type",
        "section_length": 22,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x0",
        "tier": "0xfff",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 0,
        "crc": "0xc210861f"
    },
    "command": {
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 20.00435,
        "command_length": 5
    },
    "descriptors": []
}
>>>> 


```

