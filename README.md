#### It's not just me saying [threefive is the best SCTE-35 parser.](https://www.perplexity.ai/search/best-scte35-parser-5ugjxRn3SlidRnNE_unndA?s=u)



# __threefive__ is the  highest rated SCTE-35 parser.  Ever.



### cli tool and library for encoding and decoding SCTE-35.
<br> `Parses` __SCTE-35__ from multiple streams in `MPEGTS` and `Multiple Program Transport Streams` 
<br> `Parses` __SCTE-35__ from  Cues encoded in`Base64`, `Bytes`, `Hex`, `Integers`.
<br> `Parses` __SCTE-35__ from  `files`, `http(s)`, `Multicast`, `UDP` and even `stdin` _( you can pipe to it)_. 
<br> `Parses` __SCTE-35__ from streams converted to `bin data` ( _type 0x06_ ) by `ffmpeg`.



### You haven't seen an [online SCTE-35 Encoder](https://iodisco.com/cgi-bin/scte35encoder) before, have you? 
###  [__threefive__ online SCTE-35 parser](https://iodisco.com/cgi-bin/scte35parser)
 

## new stuff in __threefive__ 

* Latest __threefive__ release is `2`.`4`.`29`, 

* __threefive__ supports the latest SCTE-35 specification `SCTE-35 2023r1`
  
*  <b>threefive/go</b> is now[ cuei](https://github.com/futzu/cuei) 


 <details> <summary> <b>threefive cli tool</b> now accepts <b>version</b>,  <b>show</b> and <b>pts</b> keywords. </summary>

* `version` <br>
```smalltalk

a@fu:~$ threefive version
2.4.25
```

* `show` <br>

```smalltalk

a@fu:~$ threefive show f10.ts

Program: 1
    Service:	Service01
    Provider:	FFmpeg
    Pid:	4096
    Pcr Pid:	256
    Streams:
		Pid: 256[0x100]	Type: 0x1b AVC Video
		Pid: 257[0x101]	Type: 0xf AAC Audio
		Pid: 258[0x102]	Type: 0x6 PES Packets/Private Data
		Pid: 259[0x103]	Type: 0x6 PES Packets/Private Data
		Pid: 260[0x104]	Type: 0x15 ID3 Timed Meta Data
```

* `pts`<br>

```smalltalk

a@fu:~$ threefive pts f10.ts
1-> 1.466667
1-> 1.6
1-> 1.533333
1-> 1.533333
1-> 1.533333
1-> 1.5
1-> 1.566667
1-> 1.733333
1-> 1.733333
```


</details>


<details><summary><b>threefive</b> is now <b>addressable TVnew stuff in thr compatible</summary>


  ```smalltalk
             "tag": 2,
            "descriptor_length": 31,
            "name": "Segmentation Descriptor",
            "identifier": "CUEI",
            "components": [],
            "segmentation_event_id": "0x065eff",
            "segmentation_event_cancel_indicator": false,
            "segmentation_event_id_compliance_indicator": true,
            "program_segmentation_flag": true,
            "segmentation_duration_flag": false,
            "delivery_not_restricted_flag": true,
            "segmentation_message": "Call Ad Server",   < --- Boom
            "segmentation_upid_type": 12,
            "segmentation_upid_type_name": "MPU",
            "segmentation_upid_length": 16,
            "segmentation_upid": {
                "format_identifier": "ADFR",	<--- Boom
                "private_data": "0x0133f10134b04f065e060220",
                "version": 1,                            <---- Boom
                "channel_identifier": "0x33f1",                  <---- Boom
                "date": 20230223,                         <---- Boom
                "break_code": 1630,                       <---- Boom
                "duration": "0x602"                <---- Boom
            },
            "segmentation_type_id": 2,         <----  Boom
            "segment_num": 0,
            "segments_expected": 0
        },

  ```
</details>



<details><summary><b>threefive's code is cleaner than your dishes</b> </summary>
<br>
<br>
  A cyclomatic coimplesity score under 15 is considered good.
<br>
<b> threefive's cyclomatic complexity is 1.968</b>

<br>

```lua	
250 blocks (classes, functions, methods) analyzed.
Average complexity: A (1.968)
```
```lua
a@fu:~/.local/lib/pypy3.9/site-packages$ radon cc -sa -o SCORE --md threefive/*.py
```

| Filename | Name | Type | Start:End Line | Complexity | Classification |
| -------- | ---- | ---- | -------------- | ---------- | -------------- |
| threefive/base.py | SCTE35Base.kv_clean | M | 68:84 | 3 | A |
| threefive/base.py | SCTE35Base.load | M | 92:100 | 3 | A |
| threefive/base.py | SCTE35Base._chk_var | M | 102:115 | 3 | A |
| threefive/base.py | SCTE35Base | C | 9:115 | 2 | A |
| threefive/base.py | SCTE35Base.as_hms | M | 35:46 | 2 | A |
| threefive/base.py | SCTE35Base._chk_nbin | M | 87:90 | 2 | A |
| threefive/base.py | SCTE35Base.__repr__ | M | 17:18 | 1 | A |
| threefive/base.py | SCTE35Base.as_90k | M | 21:25 | 1 | A |
| threefive/base.py | SCTE35Base.as_ticks | M | 28:32 | 1 | A |
| threefive/base.py | SCTE35Base.fix_hex | M | 49:53 | 1 | A |
| threefive/base.py | SCTE35Base.get | M | 55:59 | 1 | A |
| threefive/base.py | SCTE35Base.get_json | M | 61:66 | 1 | A |
| threefive/bitn.py | BitBin | C | 9:91 | 2 | A |
| threefive/bitn.py | BitBin.as_int | M | 30:38 | 2 | A |
| threefive/bitn.py | BitBin.as_charset | M | 48:60 | 2 | A |
| threefive/bitn.py | NBin | C | 94:188 | 2 | A |
| threefive/bitn.py | NBin.add_int | M | 128:135 | 2 | A |
| threefive/bitn.py | NBin.reserve | M | 165:174 | 2 | A |
| threefive/bitn.py | NBin.zeroed | M | 182:188 | 2 | A |
| threefive/bitn.py | BitBin.__init__ | M | 17:20 | 1 | A |
| threefive/bitn.py | BitBin.as_90k | M | 22:28 | 1 | A |
| threefive/bitn.py | BitBin.as_hex | M | 40:46 | 1 | A |
| threefive/bitn.py | BitBin.as_bytes | M | 63:70 | 1 | A |
| threefive/bitn.py | BitBin.as_flag | M | 72:76 | 1 | A |
| threefive/bitn.py | BitBin.forward | M | 78:83 | 1 | A |
| threefive/bitn.py | BitBin.negative_shift | M | 85:91 | 1 | A |
| threefive/bitn.py | NBin.__init__ | M | 102:105 | 1 | A |
| threefive/bitn.py | NBin.nbits2bites | M | 107:116 | 1 | A |
| threefive/bitn.py | NBin.add_bites | M | 118:123 | 1 | A |
| threefive/bitn.py | NBin.add_90k | M | 137:144 | 1 | A |
| threefive/bitn.py | NBin.add_hex | M | 146:154 | 1 | A |
| threefive/bitn.py | NBin.add_flag | M | 156:163 | 1 | A |
| threefive/bitn.py | NBin.forward | M | 176:180 | 1 | A |
| threefive/commands.py | TimeSignal._encode_splice_time | M | 140:153 | 6 | B |
| threefive/commands.py | SpliceInsert.decode | M | 179:193 | 4 | A |
| threefive/commands.py | SpliceInsert.encode | M | 232:245 | 4 | A |
| threefive/commands.py | SpliceInsert._encode_break | M | 257:269 | 4 | A |
| threefive/commands.py | TimeSignal | C | 95:153 | 3 | A |
| threefive/commands.py | SpliceInsert | C | 156:286 | 3 | A |
| threefive/commands.py | SpliceSchedule | C | 289:352 | 3 | A |
| threefive/commands.py | SpliceCommand | C | 8:36 | 2 | A |
| threefive/commands.py | BandwidthReservation | C | 39:50 | 2 | A |
| threefive/commands.py | PrivateCommand | C | 55:81 | 2 | A |
| threefive/commands.py | SpliceNull | C | 84:92 | 2 | A |
| threefive/commands.py | TimeSignal._splice_time | M | 126:138 | 2 | A |
| threefive/commands.py | SpliceInsert._decode_break | M | 195:204 | 2 | A |
| threefive/commands.py | SpliceSchedule.decode | M | 342:352 | 2 | A |
| threefive/commands.py | SpliceCommand.__init__ | M | 13:17 | 1 | A |
| threefive/commands.py | SpliceCommand.decode | M | 19:20 | 1 | A |
| threefive/commands.py | SpliceCommand._set_len | M | 24:29 | 1 | A |
| threefive/commands.py | SpliceCommand.encode | M | 31:36 | 1 | A |
| threefive/commands.py | BandwidthReservation.__init__ | M | 44:47 | 1 | A |
| threefive/commands.py | BandwidthReservation.decode | M | 49:50 | 1 | A |
| threefive/commands.py | PrivateCommand.__init__ | M | 60:64 | 1 | A |
| threefive/commands.py | PrivateCommand.decode | M | 66:73 | 1 | A |
| threefive/commands.py | PrivateCommand.encode | M | 75:81 | 1 | A |
| threefive/commands.py | SpliceNull.__init__ | M | 89:92 | 1 | A |
| threefive/commands.py | TimeSignal.__init__ | M | 100:106 | 1 | A |
| threefive/commands.py | TimeSignal.decode | M | 108:115 | 1 | A |
| threefive/commands.py | TimeSignal.encode | M | 117:124 | 1 | A |
| threefive/commands.py | SpliceInsert.__init__ | M | 161:177 | 1 | A |
| threefive/commands.py | SpliceInsert._decode_event | M | 206:214 | 1 | A |
| threefive/commands.py | SpliceInsert._decode_flags | M | 216:225 | 1 | A |
| threefive/commands.py | SpliceInsert._decode_unique_avail | M | 227:230 | 1 | A |
| threefive/commands.py | SpliceInsert._encode_event | M | 247:255 | 1 | A |
| threefive/commands.py | SpliceInsert._encode_flags | M | 271:281 | 1 | A |
| threefive/commands.py | SpliceInsert._encode_unique_avail | M | 283:286 | 1 | A |
| threefive/commands.py | SpliceSchedule.__init__ | M | 333:340 | 1 | A |
| threefive/crc.py | _bytecrc | F | 16:22 | 2 | A |
| threefive/crc.py | _mk_table | F | 25:28 | 2 | A |
| threefive/crc.py | crc32 | F | 31:41 | 2 | A |
| threefive/cue.py | Cue._mk_bits | M | 128:154 | 7 | B |
| threefive/cue.py | Cue.load_descriptors | M | 325:344 | 6 | B |
| threefive/cue.py | Cue.load | M | 275:293 | 5 | A |
| threefive/cue.py | Cue.load_command | M | 307:323 | 5 | A |
| threefive/cue.py | Cue.get | M | 92:106 | 4 | A |
| threefive/cue.py | Cue | C | 15:344 | 3 | A |
| threefive/cue.py | Cue._descriptor_loop | M | 78:90 | 3 | A |
| threefive/cue.py | Cue._unloop_descriptors | M | 259:273 | 3 | A |
| threefive/cue.py | Cue.__init__ | M | 45:56 | 2 | A |
| threefive/cue.py | Cue.decode | M | 63:76 | 2 | A |
| threefive/cue.py | Cue.get_descriptors | M | 108:113 | 2 | A |
| threefive/cue.py | Cue.fix_bad_b64 | M | 123:126 | 2 | A |
| threefive/cue.py | Cue._set_splice_command | M | 179:192 | 2 | A |
| threefive/cue.py | Cue.encode | M | 210:235 | 2 | A |
| threefive/cue.py | Cue.load_info_section | M | 295:305 | 2 | A |
| threefive/cue.py | Cue.__repr__ | M | 58:59 | 1 | A |
| threefive/cue.py | Cue.get_json | M | 115:120 | 1 | A |
| threefive/cue.py | Cue._mk_descriptors | M | 156:166 | 1 | A |
| threefive/cue.py | Cue.mk_info_section | M | 168:177 | 1 | A |
| threefive/cue.py | Cue.show | M | 194:198 | 1 | A |
| threefive/cue.py | Cue.to_stderr | M | 200:206 | 1 | A |
| threefive/cue.py | Cue.encode_as_int | M | 237:242 | 1 | A |
| threefive/cue.py | Cue.encode_as_hex | M | 244:249 | 1 | A |
| threefive/cue.py | Cue._encode_crc | M | 251:257 | 1 | A |
| threefive/decode.py | _read_stuff | F | 27:40 | 3 | A |
| threefive/decode.py | decode | F | 43:83 | 3 | A |
| threefive/descriptors.py | SegmentationDescriptor._encode_segmentation | M | 367:385 | 4 | A |
| threefive/descriptors.py | k_by_v | F | 10:17 | 3 | A |
| threefive/descriptors.py | SegmentationDescriptor | C | 242:401 | 3 | A |
| threefive/descriptors.py | SegmentationDescriptor._decode_segmentation | M | 299:311 | 3 | A |
| threefive/descriptors.py | SegmentationDescriptor._decode_segments | M | 313:334 | 3 | A |
| threefive/descriptors.py | SpliceDescriptor | C | 20:83 | 2 | A |
| threefive/descriptors.py | SpliceDescriptor.parse_tag_and_len | M | 39:48 | 2 | A |
| threefive/descriptors.py | SpliceDescriptor.parse_id | M | 50:59 | 2 | A |
| threefive/descriptors.py | SpliceDescriptor.encode | M | 67:75 | 2 | A |
| threefive/descriptors.py | AudioDescriptor | C | 86:144 | 2 | A |
| threefive/descriptors.py | AudioDescriptor.decode | M | 119:130 | 2 | A |
| threefive/descriptors.py | AudioDescriptor.encode | M | 132:144 | 2 | A |
| threefive/descriptors.py | AvailDescriptor | C | 147:170 | 2 | A |
| threefive/descriptors.py | DtmfDescriptor | C | 173:206 | 2 | A |
| threefive/descriptors.py | DtmfDescriptor.encode | M | 194:206 | 2 | A |
| threefive/descriptors.py | TimeDescriptor | C | 209:239 | 2 | A |
| threefive/descriptors.py | SegmentationDescriptor.decode | M | 274:285 | 2 | A |
| threefive/descriptors.py | SegmentationDescriptor._decode_flags | M | 287:297 | 2 | A |
| threefive/descriptors.py | SegmentationDescriptor.encode | M | 336:352 | 2 | A |
| threefive/descriptors.py | SegmentationDescriptor._encode_flags | M | 354:365 | 2 | A |
| threefive/descriptors.py | SegmentationDescriptor._encode_segments | M | 387:401 | 2 | A |
| threefive/descriptors.py | splice_descriptor | F | 414:423 | 1 | A |
| threefive/descriptors.py | SpliceDescriptor.__init__ | M | 27:37 | 1 | A |
| threefive/descriptors.py | SpliceDescriptor.decode | M | 61:65 | 1 | A |
| threefive/descriptors.py | SpliceDescriptor._encode_id | M | 77:83 | 1 | A |
| threefive/descriptors.py | AudioDescriptor.__init__ | M | 91:96 | 1 | A |
| threefive/descriptors.py | AudioDescriptor._decode_comp | M | 98:109 | 1 | A |
| threefive/descriptors.py | AudioDescriptor._encode_comp | M | 112:117 | 1 | A |
| threefive/descriptors.py | AvailDescriptor.__init__ | M | 152:155 | 1 | A |
| threefive/descriptors.py | AvailDescriptor.decode | M | 157:162 | 1 | A |
| threefive/descriptors.py | AvailDescriptor.encode | M | 164:170 | 1 | A |
| threefive/descriptors.py | DtmfDescriptor.__init__ | M | 178:183 | 1 | A |
| threefive/descriptors.py | DtmfDescriptor.decode | M | 185:192 | 1 | A |
| threefive/descriptors.py | TimeDescriptor.__init__ | M | 214:220 | 1 | A |
| threefive/descriptors.py | TimeDescriptor.decode | M | 222:229 | 1 | A |
| threefive/descriptors.py | TimeDescriptor.encode | M | 231:239 | 1 | A |
| threefive/descriptors.py | SegmentationDescriptor.__init__ | M | 247:272 | 1 | A |
| threefive/encode.py | mk_splice_insert | F | 50:115 | 3 | A |
| threefive/encode.py | mk_time_signal | F | 25:47 | 2 | A |
| threefive/encode.py | mk_splice_null | F | 13:22 | 1 | A |
| threefive/packetdata.py | PacketData | C | 8:47 | 3 | A |
| threefive/packetdata.py | PacketData._mk_timestamp | M | 24:27 | 2 | A |
| threefive/packetdata.py | PacketData.mk_pcr | M | 29:37 | 2 | A |
| threefive/packetdata.py | PacketData.mk_pts | M | 39:47 | 2 | A |
| threefive/packetdata.py | PacketData.__init__ | M | 15:21 | 1 | A |
| threefive/section.py | SpliceInfoSection._encode_encrypted | M | 114:124 | 3 | A |
| threefive/section.py | SpliceInfoSection._encode_pts_adjustment | M | 126:134 | 3 | A |
| threefive/section.py | SpliceInfoSection._encode_splice_command | M | 152:162 | 3 | A |
| threefive/section.py | SpliceInfoSection | C | 17:182 | 2 | A |
| threefive/section.py | SpliceInfoSection.decode | M | 43:66 | 2 | A |
| threefive/section.py | SpliceInfoSection._encode_sap | M | 89:96 | 2 | A |
| threefive/section.py | SpliceInfoSection._encode_section_length | M | 98:104 | 2 | A |
| threefive/section.py | SpliceInfoSection._encode_protocol_version | M | 106:112 | 2 | A |
| threefive/section.py | SpliceInfoSection._encode_cw_index | M | 136:142 | 2 | A |
| threefive/section.py | SpliceInfoSection._encode_tier | M | 144:150 | 2 | A |
| threefive/section.py | SpliceInfoSection.__init__ | M | 23:41 | 1 | A |
| threefive/section.py | SpliceInfoSection._encode_table_id | M | 68:73 | 1 | A |
| threefive/section.py | SpliceInfoSection._encode_section_syntax_indicator | M | 75:80 | 1 | A |
| threefive/section.py | SpliceInfoSection._encode_private_flag | M | 82:87 | 1 | A |
| threefive/section.py | SpliceInfoSection.encode | M | 164:182 | 1 | A |
| threefive/segment.py | Segment.decode | M | 119:136 | 6 | B |
| threefive/segment.py | Segment.__init__ | M | 56:73 | 4 | A |
| threefive/segment.py | Segment | C | 15:136 | 3 | A |
| threefive/segment.py | Segment.show_cue | M | 109:117 | 2 | A |
| threefive/segment.py | Segment.__repr__ | M | 75:76 | 1 | A |
| threefive/segment.py | Segment._mk_tmp | M | 78:80 | 1 | A |
| threefive/segment.py | Segment._aes_get_key | M | 82:84 | 1 | A |
| threefive/segment.py | Segment._aes_decrypt | M | 86:93 | 1 | A |
| threefive/segment.py | Segment._add_cue | M | 95:100 | 1 | A |
| threefive/segment.py | Segment.shushed | M | 102:107 | 1 | A |
| threefive/smoketest.py | smoke | F | 33:55 | 4 | A |
| threefive/smoketest.py | _decode_test | F | 24:30 | 2 | A |
| threefive/stream.py | Stream._parse_scte35 | M | 523:543 | 7 | B |
| threefive/stream.py | Stream._parse_sdt | M | 545:579 | 7 | B |
| threefive/stream.py | Stream._parse_tables | M | 460:475 | 6 | B |
| threefive/stream.py | Stream._parse_pmt | M | 602:627 | 6 | B |
| threefive/stream.py | Stream._find_start | M | 171:187 | 5 | A |
| threefive/stream.py | Stream.decode | M | 225:238 | 5 | A |
| threefive/stream.py | Stream.decode_fu | M | 246:260 | 5 | A |
| threefive/stream.py | Stream.show_pts | M | 318:334 | 5 | A |
| threefive/stream.py | Stream._parse_pts | M | 425:442 | 5 | A |
| threefive/stream.py | Stream.proxy | M | 286:298 | 4 | A |
| threefive/stream.py | Stream.show | M | 300:316 | 4 | A |
| threefive/stream.py | Stream._parse_pat | M | 581:600 | 4 | A |
| threefive/stream.py | ProgramInfo | C | 56:89 | 3 | A |
| threefive/stream.py | ProgramInfo.show | M | 70:89 | 3 | A |
| threefive/stream.py | Stream | C | 129:660 | 3 | A |
| threefive/stream.py | Stream._parse_cc | M | 415:423 | 3 | A |
| threefive/stream.py | Stream._parse | M | 487:495 | 3 | A |
| threefive/stream.py | Pids | C | 92:106 | 2 | A |
| threefive/stream.py | Maps | C | 109:126 | 2 | A |
| threefive/stream.py | Stream.__init__ | M | 144:166 | 2 | A |
| threefive/stream.py | Stream.pid2prgm | M | 189:197 | 2 | A |
| threefive/stream.py | Stream.pid2pts | M | 199:207 | 2 | A |
| threefive/stream.py | Stream.pid2pcr | M | 209:217 | 2 | A |
| threefive/stream.py | Stream._mk_pkts | M | 240:243 | 2 | A |
| threefive/stream.py | Stream.decode_start_time | M | 336:343 | 2 | A |
| threefive/stream.py | Stream._has_pts | M | 381:384 | 2 | A |
| threefive/stream.py | Stream._split_by_idx | M | 409:413 | 2 | A |
| threefive/stream.py | Stream._parse_payload | M | 450:458 | 2 | A |
| threefive/stream.py | Stream._parse_info | M | 477:485 | 2 | A |
| threefive/stream.py | Stream._chk_partial | M | 497:500 | 2 | A |
| threefive/stream.py | Stream._same_as_last | M | 502:506 | 2 | A |
| threefive/stream.py | Stream._section_incomplete | M | 508:513 | 2 | A |
| threefive/stream.py | Stream._parse_cue | M | 515:521 | 2 | A |
| threefive/stream.py | Stream._parse_program_streams | M | 629:642 | 2 | A |
| threefive/stream.py | Stream._set_scte35_pids | M | 654:660 | 2 | A |
| threefive/stream.py | no_op | F | 32:37 | 1 | A |
| threefive/stream.py | show_cue | F | 40:45 | 1 | A |
| threefive/stream.py | show_cue_stderr | F | 48:53 | 1 | A |
| threefive/stream.py | ProgramInfo.__init__ | M | 63:68 | 1 | A |
| threefive/stream.py | Pids.__init__ | M | 100:106 | 1 | A |
| threefive/stream.py | Maps.__init__ | M | 119:126 | 1 | A |
| threefive/stream.py | Stream.__repr__ | M | 168:169 | 1 | A |
| threefive/stream.py | Stream.iter_pkts | M | 219:223 | 1 | A |
| threefive/stream.py | Stream.decode_next | M | 262:267 | 1 | A |
| threefive/stream.py | Stream.decode_program | M | 269:275 | 1 | A |
| threefive/stream.py | Stream.decode_pids | M | 277:284 | 1 | A |
| threefive/stream.py | Stream._mk_packet_data | M | 345:350 | 1 | A |
| threefive/stream.py | Stream.as_90k | M | 353:357 | 1 | A |
| threefive/stream.py | Stream._pusi_flag | M | 360:361 | 1 | A |
| threefive/stream.py | Stream._afc_flag | M | 364:365 | 1 | A |
| threefive/stream.py | Stream._pcr_flag | M | 368:369 | 1 | A |
| threefive/stream.py | Stream._spi_flag | M | 372:373 | 1 | A |
| threefive/stream.py | Stream._pts_flag | M | 376:378 | 1 | A |
| threefive/stream.py | Stream._parse_length | M | 387:391 | 1 | A |
| threefive/stream.py | Stream._parse_pid | M | 394:399 | 1 | A |
| threefive/stream.py | Stream._parse_program | M | 402:406 | 1 | A |
| threefive/stream.py | Stream.pts | M | 444:448 | 1 | A |
| threefive/stream.py | Stream._parse_stream_type | M | 644:652 | 1 | A |
| threefive/stuff.py | print2 | F | 8:12 | 1 | A |
| threefive/upids.py | upid_encoder | F | 139:178 | 5 | A |
| threefive/upids.py | UpidDecoder._decode_eidr | M | 39:48 | 3 | A |
| threefive/upids.py | UpidDecoder.decode | M | 104:136 | 3 | A |
| threefive/upids.py | _encode_mid | F | 203:211 | 2 | A |
| threefive/upids.py | _encode_umid | F | 226:229 | 2 | A |
| threefive/upids.py | _encode_uri | F | 232:235 | 2 | A |
| threefive/upids.py | UpidDecoder | C | 14:136 | 2 | A |
| threefive/upids.py | UpidDecoder._decode_mid | M | 53:72 | 2 | A |
| threefive/upids.py | UpidDecoder._decode_mpu | M | 74:88 | 2 | A |
| threefive/upids.py | UpidDecoder._decode_umid | M | 90:96 | 2 | A |
| threefive/upids.py | _encode_air_id | F | 181:182 | 1 | A |
| threefive/upids.py | _encode_atsc | F | 185:190 | 1 | A |
| threefive/upids.py | _encode_eidr | F | 193:196 | 1 | A |
| threefive/upids.py | _encode_isan | F | 199:200 | 1 | A |
| threefive/upids.py | _encode_mpu | F | 215:219 | 1 | A |
| threefive/upids.py | _encode_no | F | 222:223 | 1 | A |
| threefive/upids.py | UpidDecoder.__init__ | M | 20:24 | 1 | A |
| threefive/upids.py | UpidDecoder._decode_air_id | M | 26:27 | 1 | A |
| threefive/upids.py | UpidDecoder._decode_atsc | M | 29:36 | 1 | A |
| threefive/upids.py | UpidDecoder._decode_isan | M | 50:51 | 1 | A |
| threefive/upids.py | UpidDecoder._decode_uri | M | 98:99 | 1 | A |
| threefive/upids.py | UpidDecoder._decode_no | M | 101:102 | 1 | A |





</details>


### [SCTE-35 code examples](https://github.com/futzu/SCTE35-threefive/blob/master/examples/README.md)

### __Documentation__ _(click a topic to expand)_



<details><summary>Supported Platforms</summary> 
 
* threefive is expected to work on any platform that runs python3.6 and up.
* There are no known platform specific issues. 
  
</details>

<details><summary>Requirements</summary>

* threefive requires
  * [pypy3](https://pypy.org) or python 3.6+ (pypy3 runs threefive 2-3 times faster than python 3.10)
  * [new_reader](https://github.com/futzu/new_reader)
  *  __pyaes__


* [Install threefive](#install)
   * [Fast Start](https://github.com/futzu/SCTE35-threefive/blob/master/FastStart.md)
   * [Super Cool Examples](https://github.com/futzu/SCTE35-threefive/blob/master/examples/README.md)
* [Versions and Releases](#versions-and-releases)
</details>

<details><summary>Versions and Releases</summary>

Every time I fix a bug or add a feature, I do a new release. 
I only support the latest version. Stay up with me. 
```lua
a@fu:~$ pypy3
Python 3.9.17 (7.3.12+dfsg-1, Jun 16 2023, 18:55:49)
[PyPy 7.3.12 with GCC 12.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>> import threefive
>>>> threefive.version
'2.4.9'
>>>> 

```
* __Release__ versions are  __odd__.
* __Unstable__ testing versions are __even__.
</details>

 <details><summary>Parse SCTE-35 on the command line.</summary>
 
* `Parse base64`
```js
threefive '/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo='
```
* `Parse a hex value`
```js
threefive 0xFC302F000000000000FFFFF014054800008F7FEFFE7369C02EFE0052CCF500000000000A0008435545490000013562DBA30A
```
* `Parse MPEGTS from stdin`
```js
cat video.ts | threefive
```
* `Parse MPEGTS video over https`
```js
threefive https://so.slo.me/longb.ts
```
* `Parse multicast`
```lua
threefive udp://@235.35.3.5:3535
```
* `display realtime program -> pts`
```lua
a@fu:~$ threefive pts /home/a/msnbc.ts

1-> 3164.442756
1-> 3164.409422
1-> 3164.476089
1-> 3164.476089
1-> 3164.476089
1-> 3164.642756
1-> 3164.576089
```
* `display mpegts stream info`
 ```lua
a@fu:~$ threefive show https://futzu.com/xaa.ts

Program: 1
    Service:	Service01
    Provider:	FFmpeg
    Pid:	4096
    Pcr Pid:	256
    Streams:
		Pid: 134[0x86]	Type: 0x86 SCTE35 Data
		Pid: 256[0x100]	Type: 0x1b AVC Video
		Pid: 257[0x101]	Type: 0xf AAC Audio
```


</details>

 <details><summary>Parse SCTE-35 programmatically with a few lines of code.</summary>

   <details><summary>Mpegts Multicast in three lines of code.</summary>

```python3
import threefive

strm = threefive.Stream('udp://@239.35.0.35:1234')
strm.decode()
````
  _(need an easy multicast server?_ [gumd](https://github.com/futzu/gumd) )

---
  </details>

 <details><summary>Mpegts over Https in three lines of code.</summary>

```python3
import threefive
strm = threefive.Stream('https://iodisco.com/ch1/ready.ts')
strm.decode()


       
   </details>

 <details><summary>Base64 in five lines of code.</summary>

```python3
>>> from threefive import Cue
>>> stuff = '/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g='
>>> cue=Cue(stuff)
>>> cue.decode()
True
 >>> cue.show()

```
---
   </details>

 <details><summary>Bytes in five lines of code.</summary>

```python3
>>> import threefive

>>> stuff = b'\xfc0\x11\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00O%3\x96'
>>> cue=Cue(stuff)
>>> cue.decode()
True
>>> cue.show()
```
---
   </details>

<details><summary>Hex in 4 lines of code.</summary>

```python3
import threefive

cue = threefive.Cue("0XFC301100000000000000FFFFFF0000004F253396")
cue.decode()
cue.show()
```
</details>

 </details>

<details><summary>Easy SCTE-35 encoding with threefive. </summary>

* Need SCTE-35 Packet Injection? [SuperKabuki](https://github.com/futzu/SuperKabuki), powered by threefive.


 * `Helper functions for SCTE35 Cue encoding`

```python3
Python 3.8.13 (7.3.9+dfsg-5, Oct 30 2022, 09:55:31)
[PyPy 7.3.9 with GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>> import threefive.encode
>>>> help(threefive.encode)



Help on module threefive.encode in threefive:

NAME
    threefive.encode - encode.py

DESCRIPTION
    threefive.encode has helper functions for Cue encoding.

FUNCTIONS
    mk_splice_insert(event_id, pts=None, duration=None, out=False)
        mk_cue returns a Cue with a Splice Insert.

        The args set the SpliceInsert vars.

        splice_event_id = event_id

        if pts is None (default):
            splice_immediate_flag      True
            time_specified_flag        False

        if pts:
            splice_immediate_flag      False
            time_specified_flag        True
            pts_time                   pts

        If duration is None (default)
            duration_flag              False

        if duration IS set:
            out_of_network_indicator   True
            duration_flag              True
            break_auto_return          True
            break_duration             duration
            pts_time                   pts

        if out is True:
            out_of_network_indicator   True

        if out is False (default):
            out_of_network_indicator   False

    mk_splice_null()
        mk_splice_null returns a Cue
        with a Splice Null

    mk_time_signal(pts=None)
         mk_time_signal returns a Cue
         with a Time Signal
        if pts is None:
             time_specified_flag   False

        if pts IS set:
             time_specified_flag   True
             pts_time              pts

```
</details>



 <details><summary>Cue Class</summary>

   *  src [cue.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/cue.py)
   *  The __threefive.Cue__ class decodes a SCTE35 binary, base64, or hex encoded string.

```py3

class Cue(threefive.base.SCTE35Base)
 |  Cue(data=None, packet_data=None)

```
```js
 |  __init__(self, data=None, packet_data=None)
 |      data may be packet bites or encoded string
 |      packet_data is a instance passed from a Stream instance
```
* `Cue.decode()`
```js
 |  decode(self)
 |      Cue.decode() parses for SCTE35 data
```
* After Calling cue.decode() the __instance variables can be accessed via dot notation__.
```python3

    >>>> cue.command
    {'calculated_length': 5, 'name': 'Time Signal', 'time_specified_flag': True, 'pts_time': 21695.740089}

    >>>> cue.command.pts_time
    21695.740089

    >>>> cue.info_section.table_id

    '0xfc'
```

* `Cue.get()`
```js
 |  get(self)
 |      Cue.get returns the SCTE-35 Cue
 |      data as a dict of dicts.
```
> `Cue.get() Example`
```python3
>>> from threefive import Cue
>>> cue = Cue('0XFC301100000000000000FFFFFF0000004F253396')
>>> cue.decode()
True
>>> cue
{'bites': b'\xfc0\x11\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00O%3\x96',
'info_section': {'table_id': '0xfc', 'section_syntax_indicator': False, 'private': False, 'sap_type': '0x3',
'sap_details': 'No Sap Type', 'section_length': 17, 'protocol_version': 0, 'encrypted_packet': False,
'encryption_algorithm': 0, 'pts_adjustment_ticks': 0, 'pts_adjustment': 0.0, 'cw_index': '0x0', 'tier': '0xfff',
'splice_command_length': 4095, 'splice_command_type': 0, 'descriptor_loop_length': 0, 'crc': '0x4f253396'},
'command': {'command_length': None, 'command_type': 0, 'name': 'Splice Null'},
'descriptors': [], 'packet_data': None}
```
* Cue.get() omits cue.bites and empty values
```
>>> cue.get()
{'info_section': {'table_id': '0xfc', 'section_syntax_indicator': False,'private': False, 'sap_type': '0x3',
'sap_details': 'No Sap Type', 'section_length': 17, 'protocol_version': 0, 'encrypted_packet': False,
'encryption_algorithm': 0, 'pts_adjustment_ticks': 0, 'pts_adjustment': 0.0, 'cw_index': '0x0', 'tier': '0xfff',
'splice_command_length': 4095, 'splice_command_type': 0, 'descriptor_loop_length': 0, 'crc': '0x4f253396'},
'command': {'command_type': 0, 'name': 'Splice Null'},
'descriptors': []}
```

* `Cue.get_descriptors()`

```js
 |  get_descriptors(self)
 |      Cue.get_descriptors returns a list of
 |      SCTE 35 splice descriptors as dicts.
```
* `Cue.get_json()`
```js
 |  get_json(self)
 |      Cue.get_json returns the Cue instance
 |      data in json.
```
* `Cue.show()`
```js
 |  show(self)
 |      Cue.show prints the Cue as JSON
```
* `Cue.to_stderr()`
```js
 |  to_stderr(self)
 |      Cue.to_stderr prints the Cue
```
</details>

<details><summary>Stream Class</summary>

  * src [stream.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/stream.py)
  * The threefive.__Stream__ class parses __SCTE35__ from __Mpegts__.
  * Supports:
     *  __File__ and __Http(s)__ and __Udp__ and __Multicast__ protocols.
  	 * __Multiple Programs__.
  	 * __Multi-Packet PAT, PMT, and SCTE35 tables__.

* threefive tries to include __pid__, __program__, anf  __pts__ of the SCTE-35 packet.

```js
class Stream(builtins.object)
 |  Stream(tsdata, show_null=True)
 |
 |  Stream class for parsing MPEG-TS data.
 ```
 ```py3
 |  __init__(self, tsdata, show_null=True)
 |
 |      tsdata is a file or http, https,
 |       udp or multicast url.
 |
 |      set show_null=False to exclude Splice Nulls

 ```

* `Stream.decode(func=show_cue)`
 ```py3
 |  decode(self, func=show_cue)
 |      Stream.decode reads self.tsdata to find SCTE35 packets.
 |      func can be set to a custom function that accepts
 |      a threefive.Cue instance as it's only argument.
 ```
 > `Stream.decode Example`

 ```python3
 import sys
 from threefive import Stream
 >>>> Stream('plp0.ts').decode()

```

   *   Pass in custom function

   *  __func__ should match the interface
  ``` func(cue)```

 > `Stream.decode with custom function Example`
```python3
import sys
import threefive

def display(cue):
   print(f'\033[92m{cue.packet_data}\033[00m')
   print(f'{cue.command.name}')

def do():
   sp = threefive.Stream(tsdata)
   sp.decode(func = display)

if __name__ == '__main__':
    do()
```

___

* `Stream.decode_next()`

 ```js
 |  decode_next(self)
 |      Stream.decode_next returns the next
 |      SCTE35 cue as a threefive.Cue instance.
 ```

> `Stream.decode_next Example`
```python3
import sys
import threefive

def do():
    arg = sys.argv[1]
    with open(arg,'rb',encoding="utf-8") as tsdata:
        st = threefive.Stream(tsdata)
        while True:
            cue = st.decode_next()
            if not cue:
                return False
            if cue:
                cue.show()

if __name__ == "__main__":
    do()

```

* `Stream.proxy(func = show_cue)`

  *  Writes all packets to sys.stdout.

  *  Writes scte35 data to sys.stderr.

 ```js
 |  decode(self, func=show_cue_stderr)
 |      Stream.decode_proxy writes all ts packets are written to stdout
 |      for piping into another program like mplayer.
 |      SCTE-35 cues are printed to stderr.
 ```
> `Stream.proxy Example`
```python3

import threefive
sp = threefive.Stream('https://futzu.com/xaa.ts')
sp.decode_proxy()
```

* Pipe to mplayer
```bash
$ python3 proxy.py | mplayer -
```
___

* `Stream.show()`

```js
|  show(self)
|   List programs and streams and info for MPEGTS
```
> `Stream.show() Example`
```python3
>>>> from threefive import Stream
>>>> Stream('https://slo.me/plp0.ts').show()
```

```js
    Service:    fancy ˹
    Provider:   fu-corp
    Pcr Pid:    1051[0x41b]
    Streams:
                Pid: 1051[0x41b]        Type: 0x1b AVC Video
                Pid: 1052[0x41c]        Type: 0x3 MP2 Audio
                Pid: 1054[0x41e]        Type: 0x6 PES Packets/Private Data
                Pid: 1055[0x41f]        Type: 0x86 SCTE35 Data

```
</details>


<details><summary> Need to verify your splice points? </summary> 
 

 
 
* Try [cue2vtt.py](https://github.com/futzu/scte35-threefive/blob/master/examples/stream/cue2vtt.py) in the examples.

   * cue2vtt.py creates webvtt subtitles out of SCTE-35 Cue data
 
* use it like this 

 ```rebol
 pypy3 cue2vtt.py video.ts | mplayer video.ts -sub -
```


 ![image](https://github.com/futzu/scte35-threefive/assets/52701496/5b8dbea3-1d39-48c4-8fbe-de03a53cc1dd)


---

</details> 

<details><summary>Custom charsets for UPIDS aka upids.charset</summary>

`Specify a charset for Upid data by setting threefive.upids.charset` [`issue #55`](https://github.com/futzu/scte35-threefive/issues/55)

* default charset is ascii
* python charsets info [Here](https://docs.python.org/3/library/codecs.html)
* setting charset to None will return raw bytes.


#### Example Usage:

```lua
>>> from threefive import Cue,upids
>>> i="/DBKAAAAAAAAAP/wBQb+YtC8/AA0AiZDVUVJAAAD6X/CAAD3W3ACEmJibG5kcHBobkQCAsGDpQIAAAAAAAEKQ1VFSRSAIyowMljRk9c="

>>> upids.charset
'ascii'
>>> cue=Cue(i)
>>> cue.decode()
ascii
True
>>> cue.descriptors[0].segmentation_upid
'bblndpphnD\x02\x02���\x02\x00\x00'

>>> upids.charset="utf16"
>>> cue.decode()
utf16
True
>>> cue.descriptors[0].segmentation_upid
'扢湬灤桰䑮Ȃ菁ʥ\x00'
```

</details>

<details> <summary> Parse Custom Splice Descriptors</summary>


1.   Subclass `threefive.descriptors.SpliceDescriptor`
2. Add `self.private_data` to` __init__`
3. Add a `decode` method 
4. Add it to `threefive.descriptors.descriptor_map` tag:Class  `112: MDSNDescriptor`
```py3
import threefive

class MDSNDescriptor(threefive.descriptors.SpliceDescriptor):
    """
    MDSNDescriptor
    """
    def __init__(self, bites=None):
        super().__init__(bites)
        self.name = "MDSN Descriptor"
        self.private_data=None

    def decode(self):
        self.private_data="".join(list(self.bites[: self.descriptor_length -4].decode()))


if __name__ == '__main__':
    threefive.descriptors.descriptor_map[112]=MDSNDescriptor 

    cue = threefive.Cue('/DBlAAAAAAAAAP/wBQb+GVJTDABPcAZNRFNOQzUCRUNVRUkAAKTff8MAACky4A8xdXJuOnV1aWQ6QnJlYWstQjAwMjA4NTU2ODlfMDAxMi0wNy0xMC1YMDExMjUxNjEyNDAAAPkSB7E=')
    cue.decode()
    cue.show()

```


```json
a@debian:~/clean/scte35-threefive$ pypy3 mdsn.py 
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x3",
        "sap_details": "No Sap Type",
        "section_length": 101,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment_ticks": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x0",
        "tier": "0xfff",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 79,
        "crc": "0xf91207b1"
    },
    "command": {
        "command_length": 5,
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 4720.284578,
        "pts_time_ticks": 424825612
    },
    "descriptors": [
        {
            "tag": 112,
            "descriptor_length": 6,
            "name": "MDSN Descriptor",   # <---- Custom Descriptor parsed. 
            "identifier": "MDSN",
            "private_data": "C5"
        },
        {
            "tag": 2,
            "descriptor_length": 69,
            "name": "Segmentation Descriptor",
            "identifier": "CUEI",
            "components": [],
            "segmentation_event_id": "0xa4df",
            "segmentation_event_cancel_indicator": false,
            "program_segmentation_flag": true,
            "segmentation_duration_flag": true,
            "delivery_not_restricted_flag": false,
            "web_delivery_allowed_flag": false,
            "no_regional_blackout_flag": false,
            "archive_allowed_flag": false,
            "device_restrictions": "No Restrictions",
            "segmentation_duration": 30.0,
            "segmentation_duration_ticks": 2700000,
            "segmentation_message": "Provider Advertisement Start",
            "segmentation_upid_type": 15,
            "segmentation_upid_type_name": "URI",
            "segmentation_upid_length": 49,
            "segmentation_upid": "urn:uuid:Break-B0020855689_0012-07-10-X0112516124",
            "segmentation_type_id": 48,
            "segment_num": 0,
            "segments_expected": 0
        }
    ]
}

```


</details>

 Powered by threefive
---
<br>⚡ [POIS Server](https://github.com/scunning1987/pois_reference_server) is Super Cool.
<br>⚡ [bpkio-cli](https://pypi.org/project/bpkio-cli/): A command line interface to the broadpeak.io APIs. 
<br>⚡ [x9k3](https://github.com/futzu/x9k3): SCTE-35 HLS Segmenter and Cue Inserter.
      <br>⚡ [amt-play ](https://github.com/vivoh-inc/amt-play) uses x9k3.
<br>⚡ [m3ufu](https://github.com/futzu/m3ufu): SCTE-35 m3u8 Parser.
<br>⚡ [six2scte35](https://github.com/futzu/six2scte35): ffmpeg changes SCTE-35 stream type to 0x06 bin data, six2scte35 changes it back.
<br>⚡ [SuperKabuki](https://github.com/futzu/SuperKabuki): SCTE-35 Packet Injection.
<br>⚡ [showcues](https://github.com/futzu/showcues) m3u8 SCTE-35 parser.
  
 threefive | more
---
<br>⚡ [Diagram](https://github.com/futzu/threefive/blob/master/cue.md) of a threefive SCTE-35 Cue.
<br>⚡ [ffmpeg and threefive](https://github.com/futzu/SCTE35-threefive/blob/master/threefive-ffmpeg.md) and SCTE35 and Stream Type 0x6 bin data.
<br>⚡ [Issues and Bugs and Feature Requests](https://github.com/futzu/scte35-threefive/issues) No forms man, just open an issue and tell me what you need. <br><i>(It needs to be  threefive related or a "What is the meaning of life and stuff?" type of question)</i>











### data
> this might be wild baseless speculation.
