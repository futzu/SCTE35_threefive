<pre>
 <h1>threefive is the SCTE-35 cli tool</h1>
</pre>
   <br>

# Using.

* [Parse](#parse) Decode SCTE-35 Strings and MPEGTS
* [Version](#version) Display threefive version
* [Show](#show)  Show MPEGTS Stream information
* [PTS](#pts) Print PTS from MPEGTS Streams
* [Packets](#packets) Print Raw SCTE-35 packets
* [Sidecar](#sidecar) Create SCTE-35 sidecar files from MPEGTS
* [Encode](#encode) JSON to SCTE-35
* [Convert](#convert) SCTE-35 Formats
* [Help](#help) Display threefive help


 ### Parse 
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
### Version

## keywords
the threefive cli uses keywords for additional functionality.

* keyword `version` - show threefive version
```lua
a@slow:~/threefive$ threefive version
2.4.35                                                                                           
a@slow:~/threefive$                                                                               
                           
```
---
### Show
* keyword `show`- display mpegts stream info

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
---
### PTS
* keyword `pts` -  display realtime program -> pts

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
---
### Packets

* keyword `packets` - show raw SCTE-35 packets
```lua
a@slow:~/threefive$ threefive packets https://futzu.com/xaa.ts

b'G@\x86\x00\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\x05\xdd\x01\x00\x00\xc0\xfc\xe7\x80\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
b'G@\x86\x01\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\x07<\xeb\x00\x00\xbf\x8b\x96\x02\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
b'G@\x86\x02\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\x08\x9c\xd5\x00\x00e\x07\x16F\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'

```
---
# Sidecar
* keyword `sidecar` - Generate a sidecar file of pts,cue pairs from a stream
```lua
  threefive sidecar https://futzu.com/xaa.ts

cat sidecar.txt
a@slow:~$ cat sidecar.txt
  
9.241178,/DAWAAAAAAAAAP/wBQb+AAy8lAAA2Olecw==
10.242178,/DAWAAAAAAAAAP/wBQb+AA4cfgAAquAlEw==
11.243178,/DAWAAAAAAAAAP/wBQb+AA98aAAAwU63WA==
12.244178,/DAWAAAAAAAAAP/wBQb+ABDcUgAAn3KLDA==
13.245178,/DAWAAAAAAAAAP/wBQb+ABI8PAAA11yRpQ==
14.246178,/DAWAAAAAAAAAP/wBQb+ABOcJgAAwqB4gg==
15.213811,/DAWAAAAAAAAAP/wBQb+ABT8EAAAIPU2sA==
16.214811,/DAWAAAAAAAAAP/wBQb+ABZb+gAATn6zuw==
17.215811,/DAWAAAAAAAAAP/wBQb+ABe75AAAjfN41Q==
18.216822,/DAWAAAAAAAAAP/wBQb+ABkb0AAAEwaiKg==
19.251189,/DAWAAAAAAAAAP/wBQb+ABp7ugAAs6FQDw==
20.218822,/DAWAAAAAAAAAP/wBQb+ABvbpAAAoT8LNA==
```
---
### Proxy

* keyword `proxy` - parse the SCTE-35 from a stream and write it to stdout (for piping to ffmpeg and such)
```lua
threefive proxy https://example.com/video.ts | ffmpeg -i - {ffmpeg commands}
```
---
### Encode
* keyword `encode` - Edit and Re-encode JSON output from threefive
* [json.out](https://github.com/futzu/SCTE35_threefive/blob/master/json.txt)
* as base64 
```lua
a@fu:~$ cat json.out | threefive encode
/DBhAAAAAAAA///wBQb+qM1E7QBLAhdDVUVJSAAArX+fCAgAAAAALLLXnTUCAAIXQ1VFSUgAACZ/nwgIAAAAACyy150RAAACF0NVRUlIAAAnf58ICAAAAAAsstezEAAAihiGnw==
```
 * as hex
```lua
a@fu:~$ cat json.out | threefive encode hex
0xfc3061000000000000fffff00506fea8cd44ed004b021743554549480000ad7f9f0808000000002cb2d79d350200021743554549480000267f9f0808000000002cb2d79d110000021743554549480000277f9f0808000000002cb2d7b31000008a18869f
```
* as an int
```lua
a@fu:~$ cat json.out | threefive encode int
6568749059128831486770192060532589909352206581290249439460423247484378938150399213176211592233234590227802036714452527295011311848713149376955134229649960769281993134835846163707258133030654884112453407592348170135352109879034827455065523871
```
* as bytes
```lua
a@fu:~$ cat json.out | threefive encode bytes
b"\xfc0a\x00\x00\x00\x00\x00\x00\xff\xff\xf0\x05\x06\xfe\xa8\xcdD\xed\x00K\x02\x17CUEIH\x00\x00\xad\x7f\x9f\x08\x08\x00\x00\x00\x00,\xb2\xd7\x9d5\x02\x00\x02\x17CUEIH\x00\x00&\x7f\x9f\x08\x08\x00\x00\x00\x00,\xb2\xd7\x9d\x11\x00\x00\x02\x17CUEIH\x00\x00'\x7f\x9f\x08\x08\x00\x00\x00\x00,\xb2\xd7\xb3\x10\x00\x00\x8a\x18\x86\x9f"
```
### Convert

* Convert Base64 SCTE-35 to Hex SCTE-35
```lua
a@fu:~$ threefive '/DBhAAAAAAAA///wBQb+qM1E7QBLAhdDVUVJSAAArX+fCAgAAAAALLLXnTUCAAIXQ1VFSUgAACZ/nwgIAAAAACyy150RAAACF0NVRUlIAAAnf58ICAAAAAAsstezEAAAihiGnw==' 2>&1 | threefive encode hex
```
```lua
0xfc3061000000000000fffff00506fea8cd44ed004b021743554549480000ad7f9f0808000000002cb2d79d350200021743554549480000267f9f0808000000002cb2d79d110000021743554549480000277f9f0808000000002cb2d7b31000008a18869f

```
### Help
--- 
*  keyword `help`

```lua
threefive help
```
---




