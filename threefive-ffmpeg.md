## threefive works very well with ffmpeg. 
* __ffmpeg changes the SCTE-35 (0x86) stream type to bin data (0x6)__
  * Changing the stream type __Breaks Every SCTE-35 parser, Except threefive__.
  * __threefive__  parses SCTE-35 (__0x86__) and bin data (__0x6__) stream types.  

### Example 1
---
* Transcode mpegts with a SCTE-35 stream and pipe it to threefive to parse SCTE-35
  * oldvid.ts looks like this:
```
  Program 1 
  Stream #0:0[0x31]: Video: h264 (High) ([27][0][0][0] / 0x001B), yuv420p(tv, bt709, progressive), 
  1280x720 [SAR 1:1 DAR 16:9], Closed Captions, 59.94 fps, 59.94 tbr, 90k tbn
  Stream #0:1[0x32]: Audio: mp2 ([4][0][0][0] / 0x0004), 48000 Hz, stereo, s16p, 256 kb/s
  Stream #0:2[0x33]: Audio: mp2 ([4][0][0][0] / 0x0004), 48000 Hz, stereo, s16p, 256 kb/s
  Stream #0:3[0x34]: Audio: mp2 ([4][0][0][0] / 0x0004), 48000 Hz, stereo, s16p, 256 kb/s
  Stream #0:4[0x35]: Audio: mp2 ([4][0][0][0] / 0x0004), 48000 Hz, stereo, s16p, 256 kb/s
  Stream #0:5[0x36]: Data: scte_35
```
* transcode
   * `-copyts`, keep timestamps 
   * `-map`  keep SCTE-35 stream 

```sh
ffmpeg  -copyts -i  oldvid.ts -vcodec libx265  -map 0  -y  newvid.ts
```

* newvid.ts looks like this
```
  Program 1 
  Stream #0:0[0x100]: Video: hevc (Main) (HEVC / 0x43564548), yuv420p(tv, bt709), 1280x720 
  [SAR 1:1 DAR 16:9], 59.94 fps, 59.94 tbr, 90k tbn
  Stream #0:1[0x101]: Audio: mp2 ([3][0][0][0] / 0x0003), 48000 Hz, stereo, fltp, 384 kb/s
  Stream #0:2[0x102]: Audio: mp2 ([3][0][0][0] / 0x0003), 48000 Hz, stereo, fltp, 384 kb/s
  Stream #0:3[0x103]: Audio: mp2 ([3][0][0][0] / 0x0003), 48000 Hz, stereo, fltp, 384 kb/s
  Stream #0:4[0x104]: Audio: mp2 ([3][0][0][0] / 0x0003), 48000 Hz, stereo, fltp, 384 kb/s
  Stream #0:5[0x105]: Data: bin_data ([6][0][0][0] / 0x0006)
```

 * Create 35.py
 
 ```smalltalk
 #!/usr/bin/env python3
"""
35.py
    parses a stream for SCTE-35,
    prints SCTE-35 messages
"""

import sys
import threefive


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    else:
        arg = sys.stdin.buffer

    strm = threefive.Stream(arg)
    strm.decode()
```
* parse newvid.ts with 35.py

```smalltalk
a@debian:~$ pypy3 35.py  newvid.ts
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x3",
        "sap_details": "No Sap Type",
        "section_length": 169,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment_ticks": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x0",
        "tier": "0xfff",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 147,
        "crc": "0x8c829e81"
    },
    "command": {
        "command_length": 5,
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 14652.879367,
        "pts_time_ticks": 1318759143
    },
    "descriptors": [
        {
            "tag": 2,
            "descriptor_length": 21,
            "name": "Segmentation Descriptor",
            "identifier": "CUEI",
            "components": [],
            "segmentation_event_id": "0x949d1b0",
            "segmentation_event_cancel_indicator": false,
            "program_segmentation_flag": true,
            "segmentation_duration_flag": false,
            "delivery_not_restricted_flag": false,
            "web_delivery_allowed_flag": true,
            "no_regional_blackout_flag": true,
            "archive_allowed_flag": true,
            "device_restrictions": "No Restrictions",
            "segmentation_message": "Provider Placement Opportunity End",
            "segmentation_upid_type": 1,
            "segmentation_upid_type_name": "Deprecated",
            "segmentation_upid_length": 6,
            "segmentation_upid": "300009",
            "segmentation_type_id": 53,
            "segment_num": 1,
            "segments_expected": 1
        },

    ],
    "packet_data": {
        "pid": "0x105",
        "program": 1,
        "pcr_ticks": 1318822943,
        "pcr": 14653.588256,
        "pts_ticks": 1318890273,
        "pts": 14654.336367
    }
}


```
* transcode with ffmpeg and pipe directly to 35.py
```sh
ffmpeg  -copyts -i  oldvid.ts -vcodec libx265  -map 0  -f mpegts - | python3 35.py

```
---
## Example 2
* use threefive to parse for SCTE-35 and pipe to ffplay
1. Create 35proxy.py
```smalltalk
#!/usr/bin/env python3
"""
35proxy.py
    parses a stream for SCTE-35,
    prints SCTE-35 messages to stderr
    and proxies the stream to stdin
"""
import sys
import threefive


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    else:
        arg = sys.stdin.buffer
    strm = threefive.Stream(arg)
    strm.decode_proxy()
```
2. Run 35proxy.py and pipe to ffplay
```smalltalk
./35proxy.py vid.ts | ffplay -
```
---
