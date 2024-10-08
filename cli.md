 <h1>threefive is the SCTE-35 cli tool</h1>
   <br>

* [Help](#help) Display threefive help
* [Parse](#parse) Decode SCTE-35 Strings and MPEGTS
* [Sixfix](#sixfix) sixfix converts Ffmpeg bin data streams back to SCTE-35.
* [Encode](#encode) JSON and XML as inputs for encoding to SCTE-35.
* [Xml](#xml) Xml as an output format for SCTE-35 Cues from strings and mpegts streams.
* [Version](#version) Display threefive version
* [Show](#show)  Show MPEGTS Stream information
* [PTS](#pts) Print PTS from MPEGTS Streams
* [Packets](#packets) Print Raw SCTE-35 packets
* [Sidecar](#sidecar) Create SCTE-35 sidecar files from MPEGTS


## `Help`
* Use the help man, I spent a lot of time trying to get it to make sense.

![image](https://github.com/user-attachments/assets/601f23ca-6a52-4532-908d-a680723230ee)

## `Parse` 

![image](https://github.com/user-attachments/assets/9352fd02-4697-4763-8279-c8fa94eb9ec5)

* By default, threefive will parse SCTE-35 from:
* Strings
	* Bytes
	* Base64
	* Hex
	* Integers
   
* MPEGTS 
	* Files
 	* Https
  	* Multicast
  	* UDP
  	* Stdin
___


![image](https://github.com/user-attachments/assets/de6f9ac4-2950-44f8-b65e-9a62985520d7)

the threefive cli uses keywords for additional functionality.

## `Version`

![image](https://github.com/user-attachments/assets/b58d7863-d413-4ddc-9b48-3cb52784820f)

* keyword `version` - show threefive version

---
## `Show`

![image](https://github.com/user-attachments/assets/91ffece2-8108-40b1-9231-dcbb66caea11)
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
## `PTS`
![image](https://github.com/user-attachments/assets/c4c86da7-fb20-4aba-af30-481f634116e2)
* keyword `pts` -  display realtime pts values

---
## `Sixfix`
![image](https://github.com/user-attachments/assets/1ad076c1-528f-4e94-9c60-8bb0a2a21857)
* keyword `sixfix`


* ffmpeg changes SCTE-35 streams types to 0x6 bin data. sixfix will convert the bin data back to SCTE-35.
* The new file name is prefixed with 'fixed'.


* Input file is sixed.ts

```js
  a@fu:~/build/SCTE35_threefive$ ffprobe -hide_banner sixed.ts                                    
Input #0, mpegts, from 'sixed.ts':                                                                                  
  Stream #0:0[0x100]: Video: h264 (Main) ([27][0][0][0] / 0x001B), yuv420p(tv, progressive), 640x360 [SAR 1:1 DAR 16:9], 29.97 fps, 29.97 tbr, 90k tbn
  Stream #0:1[0x101](und): Audio: aac (LC) ([15][0][0][0] / 0x000F), 48000 Hz, stereo, fltp, 64 kb/s
  Stream #0:2[0x102]: Data: bin_data ([6][0][0][0] / 0x0006) <------ Bin Data
  Stream #0:3[0x103]: Data: timed_id3 (ID3  / 0x20334449)
```
* Run  threefive sixfix
```js
a@fu:~/build/SCTE35_threefive$ ./threefive sixfix sixed.ts
```
* output file  is named fixed-sixed.ts
```js
a@fu:~/build/SCTE35_threefive$ ffprobe -hide_banner fixed-sixed.ts                            
Input #0, mpegts, from 'fixed-sixed.ts':                                                                            
  Stream #0:0[0x100]: Video: h264 (Main) ([27][0][0][0] / 0x001B), yuv420p(tv, progressive), 640x360 [SAR 1:1 DAR 16:9], 29.97 fps, 29.97 tbr, 90k tbn
  Stream #0:1[0x101](und): Audio: aac (LC) ([15][0][0][0] / 0x000F), 48000 Hz, stereo, fltp, 64 kb/s
  Stream #0:2[0x102]: Data: scte_35       <------------ fixed
  Stream #0:3[0x103]: Data: timed_id3 (ID3  / 0x20334449)
```

## `Encode`

![image](https://github.com/user-attachments/assets/27307593-eb87-448b-b9e3-d3917f40e34b)
* keyword `encode` -  JSON or XML as an input for encoding SCTE-35. 
The threefive cli tool can now encode JSON and XML to SCTE-35.  


* Change the pts_time 
    * Here I do it with sed, you can use any editor 

```js
sed -i 's/20.004344/60.0/' json.txt
```
* Re-encode as Base64
```lua
a@fu:~$ cat json.txt | threefive encode

/DAWAAAAAAAAAP/wBQb+AFJlwAAAZ1PBRA==
```

* Re-encode as Hex
```lua
a@fu:~$ cat json.txt | threefive encode hex
0xfc301600000000000000fff00506fe005265c000006753c144
```

* Re-encode as an integer
```lua
a@fu:~$ cat json.txt | threefive encode int
1583008701074197245727019716796221242034694813189400685691204
```
* Re-encode as bytes
 ```lua
a@fu:~$ cat json.txt | threefive encode bytes
b'\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00Re\xc0\x00\x00gS\xc1D'
```
* Re-encode as Xml
```lua
cat json.txt | threefive encode xml
```
* xml to Base64
```js
a@fu:~$ cat xml.xml | threefive encode
/DAWAAAAAAAAAP/wBQb+ABt4xwAAwhCGHw==
```
* xml to json
```
a@fu:~$ cat xml.xml | threefive encode json
```

## `Xml`

![image](https://github.com/user-attachments/assets/5c597b48-764b-4009-b6a3-f0ec984fa6f5)
* keyword `xml`
* Xml is also supported as an output when decoding SCTE-35.

* xml output for Base64
```js
a@fu:~$ threefive xml  '/DAWAAAAAAAAAP/wBQb+ABt4xwAAwhCGHw=='
```
```xml 
<SpliceInfoSection xmlns="https://scte.org/schemas/35" ptsAdjustment="0" protocolVersion="0" sapType="3" tier="4095">
   <TimeSignal>
      <SpliceTime ptsTime="1800391"/>
   </TimeSignal>
</SpliceInfoSection>
```
* Xml output is available when decoding mpegts streams using the xml keyword.
```js
a@fu:~$ threefive xml build/SCTE35_threefive/sixed.ts
```
---
## `Packets`

![image](https://github.com/user-attachments/assets/815b4395-dfc6-48cf-9c85-cfe25120c417)
* keyword `packets` - show raw SCTE-35 packets


```lua
a@slow:~/threefive$ threefive packets https://futzu.com/xaa.ts

b'G@\x86\x00\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\x05\xdd\x01\x00\x00\xc0\xfc\xe7\x80\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
b'G@\x86\x01\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\x07<\xeb\x00\x00\xbf\x8b\x96\x02\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
b'G@\x86\x02\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\x08\x9c\xd5\x00\x00e\x07\x16F\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'

```
---
## `Sidecar`
![image](https://github.com/user-attachments/assets/36ce3f57-99e0-4997-b235-57c2fb04731e)

* keyword `sidecar` - Generate a sidecar file of pts,cue pairs from a stream
```lua
  threefive sidecar https://futzu.com/xaa.ts
```

```lua
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
## `Proxy`
![image](https://github.com/user-attachments/assets/00ef6fa5-3c16-4499-ac96-2c526b916268)

* keyword `proxy` - parse the SCTE-35 from a stream and write it to stdout (for piping to ffmpeg and such)
```smalltalk
threefive proxy https://example.com/video.ts | ffmpeg -i - {ffmpeg commands}
```
---

