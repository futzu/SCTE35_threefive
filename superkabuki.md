### Project Super Kabuki is SCTE35 MPEGTS Packet Injection.

_I am hesitant to release superkabuki, I fear it will be a pain for me to support._



* ffprobe in.ts

```lua
ffprobe -hide_banner  in.ts
Input #0, mpegts, from 'in.ts':
  Duration: 00:01:00.13, start: 4.202733, bitrate: 2090 kb/s
  Program 1 
    Metadata:
      service_name    : Service01
      service_provider: FFmpeg
  Stream #0:0[0x100]: Video: h264 (High) ([27][0][0][0] / 0x001B), yuv420p(tv, bt709, progressive), 1920x1080 [SAR 1:1 DAR 16:9], 29.97 fps, 29.97 tbr, 90k tbn
  Stream #0:1[0x101](und): Audio: aac (LC) ([15][0][0][0] / 0x000F), 48000 Hz, stereo, fltp, 135 kb/s
```
* Make a Time Signal Command

```smalltalk
Python 3.8.13 (7.3.9+dfsg-4, Aug 09 2022, 12:51:24)
[PyPy 7.3.9 with GCC 12.1.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>> from threefive import Cue, TimeSignal
>>>> cue = Cue()
>>>> ts = TimeSignal()
>>>> ts.pts_time=10.27554444
>>>> ts.time_specified_flag=True
>>>> cue.command =ts
>>>> cue.encode()
'/DAWAAAAAAAAAP/wBQb+AA4cfwAAqziJlA=='

>>>> cue.bites
b'\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\x0e\x1c\x7f\x00\x00\xab8\x89\x94'
```

* run superkabuki.py to add a SCTE35 stream and a SCTE35 payload

```lua
 pypy3  superkabuki.py -i in.ts -o out.ts -p 0x36 --cue b'\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\x0e\x1c\x7f\x00\x00\xab8\x89\x94'
```

```smalltalk
seclen 29
program_number 1
pcr_pid 256
New PMT b'\x02\xb0(\x00\x01\xc1\x00\x00\xe1\x00\xf0\x06\x05\x04CUEI\x1b\xe1\x00\xf0\x00\x0f\xe1\x01\xf0\x06\n\x04und\x00\x86\xe06\xf0\x00'
0xf3fa02ef
```

* ffprobe out.ts and check for the new stream
```lua
 ffprobe -hide_banner out.ts

Input #0, mpegts, from 'out.ts':
  Duration: 00:01:00.13, start: 4.202733, bitrate: 2090 kb/s
  Program 1 
    Metadata:
      service_name    : Service01
      service_provider: FFmpeg
  Stream #0:0[0x100]: Video: h264 (High) ([27][0][0][0] / 0x001B), yuv420p(tv, bt709, progressive), 1920x1080 [SAR 1:1 DAR 16:9], 29.97 fps, 29.97 tbr, 90k tbn
  Stream #0:1[0x101](und): Audio: aac (LC) ([15][0][0][0] / 0x000F), 48000 Hz, stereo, fltp, 135 kb/s
  
  Stream #0:2[0x36]: Data: scte_35                             <------- New SCTE35 Stream PID 0x36 ✓
```
* run threefive on out.ts to check for the new SCTE35 Cue

```lua

threefive out.ts

a@debian:~/scte35-threefive$ threefive out.ts
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
        "pts_adjustment_ticks": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x0",
        "tier": "0xfff",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 0,
        "crc": "0xab388994"
    },
    "command": {
        "command_length": 5,
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 10.275544,          <--------- SCTE35 PTS ✓
        "pts_time_ticks": 924799
    },
    "descriptors": [],
    "packet_data": {
        "pid": "0x36",                  <-------- PID 0x36 ✓
        "program": 1,
        "pcr_ticks": 855793,
        "pcr": 9.508811,
        "pts_ticks": 924799,
        "pts": 10.275544                <-------- Packet PTS ✓
    }

```

