# More on Encoding. 
A lot of people have been looking at the encoding page, and I think the encoding is a pretty good explanation 
but there is a little more encoding stuff in threefive and rather than complicated the encoding page, I wanted 
to put it here. 

# The Cue class has a lot of stuff I've never really mentioned. I wanted to wait a while and see if anything blew up. A lot of the Cue methods are for encoding.

### Cues can be encoded as base64, hex, integers, or bytes
```py3
|  encode(self)
 |      Cue.encode() converts SCTE35 data
 |      to a base64 encoded string.
 |  
 |  encode_as_hex(self)
 |      encode_as_hex returns self.bites as
 |      a hex string
 |  
 |  encode_as_int(self)
 |      encode_as_int returns self.bites as an int.
 |
```
```py3
a@slow:~/SCTE-35-HLS-Sideways$ pypy3
Python 3.9.16 (7.3.11+dfsg-2, Feb 06 2023, 16:52:03)
[PyPy 7.3.11 with GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.

>>>> from threefive import Cue,TimeSignal

>>>> cue = Cue()                                                                         

>>>> cue.command=TimeSignal()
>>>> cue.command.time_specified_flag=True
>>>> cue.command.pts_time=12345.13

>>>> cue.encode()                                                                        
'/DAWAAAAAAAAAP/wBQb+Qjl0xAAAMsxgbg=='                                                 

>>>> cue.encode_as_hex()
'0xfc301600000000000000fff00506fe423974c4000032cc606e'                                  

>>>> cue.encode_as_int()
1583008701074197245727019716796221242345910914446764125479022

## Note: it's Cue.bites, since bytes() is a builtin python function.

>>>> cue.bites
b'\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfeB9t\xc4\x00\x002\xcc`n'

>>>> 


>>>> cue.show()
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 22,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment_ticks": 0,
        "cw_index": "0x0",
        "tier": "0xfff",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 0,
        "crc": "0x32cc606e"
    },
    "command": {
        "command_length": 5,
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 12345.13,
        "pts_time_ticks": 1111061700
    },
    "descriptors": []
}
>>>> 
```
### The Cue class also has methods to load data from a dictionary or JSON for encoding

```pypy3
|  load(self, stuff)
 |      Cue.load loads SCTE35 data for encoding.
 |      stuff is a dict or json
 |      with any or all of these keys
 |      stuff = {
 |          'info_section': {dict} ,
 |          'command': {dict},
 |          'descriptors': [list of {dicts}],
 |          }
 |  
 |  load_command(self, cmd)
 |      load_command loads data for Cue.command
 |      cmd should be a dict.
 |      if 'command_type' is included,
 |      the command instance will be created.
 |  
 |  load_descriptors(self, dlist)
 |      Load_descriptors loads descriptor data.
 |      dlist is a list of dicts
 |      if 'tag' is included in each dict,
 |      a descriptor instance will be created.
 |  
 |  load_info_section(self, isec)
 |      load_info_section loads data for Cue.info_section
 |      isec should be a dict.
 |      if 'splice_command_type' is included,
 |      an empty command instance will be created for Cue.command
```
