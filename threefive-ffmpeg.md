## Working with ffmpeg. 

 * I don't know how to __stop ffmpeg__ from __changing__ the __SCTE35__ stream __type__ to __0x6__.

 * **It doesn't matter**.
 *  __threefive parses__ for __SCTE35__ on __streams__ of type __0x86__ and __0x6__


```sh
a@fuhq$ ffmpeg -hide_banner -i video.ts


Input #0, mpegts, from 'video.ts':                                                                                            
  Duration: 00:02:41.17, start: 38090.624111, bitrate: 7044 kb/s
  Program 51 
    Stream #0:0[0x1fe]: Video: h264 (High) ([27][0][0][0] / 0x001B), yuv420p(tv, bt709, top first), 1920x1080 [SAR 1:1 DAR 16:9], Closed Captions, 29.97 fps, 59.94 tbr, 90k tbn, 59.94 tbc
    Stream #0:1[0x1ff]: Audio: ac3 ([129][0][0][0] / 0x0081), 48000 Hz, 5.1(side), fltp, 384 kb/s
    Stream #0:2[0x200]: Audio: ac3 ([129][0][0][0] / 0x0081), 48000 Hz, stereo, fltp, 192 kb/s
    Stream #0:3[0x203]: Data: scte_35
```

* **Map and Copy Streams**

```sh

a@fuhq$ ffmpeg -copyts \
        -i video.ts -c copy -map 0 \
        -streamid 0:510  -streamid 1:511 -streamid 2:512 -streamid 3:515 -mpegts_service_id 51 \
        -y out.ts
```
* **This Warning Pops Up**
```
[mpegts @ 0x55ccc4ca5480] Stream 3, codec scte_35, is muxed as a private data stream and may not be recognized upon reading.  

```
* **Stream #0:3 Is Now Type 0x6**
```
a@fuhq$ ffmpeg -hide_banner -i out.ts
Input #0, mpegts, from 'out.ts':                                                                                              
  Duration: 00:02:41.17, start: 38092.024111, bitrate: 7065 kb/s
  Program 51 
    Stream #0:0[0x1fe]: Video: h264 (High) ([27][0][0][0] / 0x001B), yuv420p(tv, bt709, top first), 1920x1080 [SAR 1:1 DAR 16:9], Closed Captions, 29.97 fps, 59.94 tbr, 90k tbn, 59.94 tbc
    Stream #0:1[0x1ff]: Audio: ac3 ([129][0][0][0] / 0x0081), 48000 Hz, 5.1(side), fltp, 384 kb/s
    Stream #0:2[0x200]: Audio: ac3 ([129][0][0][0] / 0x0081), 48000 Hz, stereo, fltp, 192 kb/s
    Stream #0:3[0x203]: Data: bin_data ([6][0][0][0] / 0x0006)
```


* **Parse out.ts For SCTE35**
```sh
a@fuhq$ pypy3 -c 'import threefive; threefive.decode("out.ts")'

{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x3",
        "sap_details": "No Sap Type",
        "section_length": 49,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x0",
        "tier": "0xfff",
        "splice_command_length": 20,
        "splice_command_type": 5,
        "descriptor_loop_length": 12
    },
    "command": {
        "command_length": 20,
        "command_type": 5,
        "name": "Splice Insert",
        "time_specified_flag": true,
        "pts_time": 38113.135578,
        "break_auto_return": false,
        "break_duration": 90.023267,
        "splice_event_id": 93,
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
            "tag": 1,
            "descriptor_length": 10,
            "identifier": "CUEI",
            "name": "DTMF Descriptor",
            "preroll": 177,
            "dtmf_count": 4,
            "dtmf_chars": [
                "1",
                "2",
                "1",
                "*"
            ]
        }
    ],
    "crc": "0x2d87a625",
    "pid": 515,
    "program": 51,
    "pts": 38105.259644
}
```
