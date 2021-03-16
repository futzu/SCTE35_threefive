

# :rocket: threefive		

#### threefive is a SCTE35 Decoder,Editor, Encoder, and Parser library in Python3.

* References the __2020 SCTE35__ Specification.

* Decode __SCTE35__ from __MPEG-TS video__ files and streams, __Base64, Hex, and Binary__ encoded strings.
  
* __threefive__ now  [ __Encodes__ ](https://github.com/futzu/SCTE35-threefive/blob/master/Encoding.md) SCTE35 Cues.

* threefive [__Cyclomatic Complexity__](https://github.com/futzu/SCTE35-threefive/blob/master/cyclomatic_complexity.md)

* Performance [__Tuning__](https://github.com/futzu/SCTE35-threefive/blob/master/stream_tune.md#tuning-pat-and-pmt-packet-parsing-in-threefivestream) threefive.Stream


---
### Install threefive 
* [Dependencies and Installation](#install)
---   
### Fast Start 
*   [Up and Running in Less Than Seven Seconds](https://github.com/futzu/SCTE35-threefive/blob/master/FastStart.md) 
---
###  Easy threefive
   * [Parsing __SCTE 35__ Cues from __Mpeg-TS Streams__](#the-decode-function)
   * [Parsing __SCTE 35__ Cues from __Mpeg-TS Streams__ over __HTTPS__](#the-decode-function)
   * [Parsing __SCTE 35__ Cue strings encoded in __Base64__, or __Hex__](#the-decode-function)
   * [Parsing __SCTE 35__ Cues directly from a file encoded in __Base64__, __Binary__,  or __Hex__](#the-decode-function)
---      
###  Advanced threefive     
  *  [__Cue__ Class](#cue-class)       
  *  [__Stream__ Class](#stream-class)
---     
### Examples
  *  [Splice __Insert__](https://github.com/futzu/SCTE35-threefive/blob/master/examples/spliceinsert/Splice_Insert.py) 
  *  [DTMF __Descriptor__](https://github.com/futzu/SCTE35-threefive/blob/master/examples/dtmf) 
  * [__Time Signal__ Program Start End](https://github.com/futzu/SCTE35-threefive/blob/master/examples/timesignal/Time_Signal-Program_Start_End.py)
  *  [Combination __Upid__ Segmentation Descriptor](https://github.com/futzu/SCTE35-threefive/blob/master/examples/upid/Upid_Combo.py)
  
*   [Parsing __HLS Manifests__ with threefive](https://github.com/futzu/SCTE35-threefive/tree/master/examples/hls)

*  [__SCTE35__ from a __Multicast__ Stream](https://github.com/futzu/SCTE35-threefive/blob/master/examples/multicast/README.txt)
      
*  [__SCTE35__ from __MPEG-TS__ video over __HTTPS__](https://github.com/futzu/SCTE35-threefive/blob/master/examples/stream/Decode_Over_Http.py) 


  * [__All Examples__](https://github.com/futzu/SCTE35-threefive/tree/master/examples#threefive-examples)
   

---
### Cool Stuff

* [__threefive__ Spotted in __The Wild__](https://gist.github.com/flavioribeiro/9b52c603c70cdb34c6910c1c5c4d240d)


* [__ffmpeg__ and __SCTE35__ and __Stream Type__ and __threefive__](https://github.com/futzu/SCTE35-threefive/blob/master/threefive-ffmpeg.md)


   
---

### Install

* __dependencies__
   *  Python 3.6+ or pypy3 (__pypy3 runs threefive three times faster than python3__)
   *  [__bitn__](https://github.com/futzu/bitn)
   *  [__crcmod__](https://github.com/gsutil-mirrors/crcmod)
   *  [__urllib3__](https://github.com/urllib3/urllib3)


*  __install from git__

```bash
$ git clone https://github.com/futzu/SCTE35-threefive.git

$ cd SCTE-threefive
# you need root to install for the system
$ make install

# for pypy3 
$ make pypy3
```
*  __install from pip__

```bash
$ pip3 install threefive

# for pypy3
$ pypy3 -mpip install threefive

#If you don't have pip installed, try this.
$ pypy3 -mensurepip install pip 
```


[🡡 top](#rocket-threefive)


## __Easy__ threefive

###   The __decode__ Function


 *   src [decode.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/decode.py)   
 * __threefive.decode__ is an all purpose function to decode SCTE 35 messages from a file or string.
 
 *   __MpegTS__
 
```python3
import threefive
threefive.decode('/path/to/mpegwithscte35.ts') 

```
 *  New in __v.2.2.69__ threefive.decode can parse __MpegTS__ over __http and https__
 
 ```python3
import threefive
threefive.decode('https://futzu.com/xaa.ts') 

```

* __Base64__ 

```python3
mesg='/DA4AAAAAAAA///wBQb+AAAAAAAiAiBDVUVJAAAAA3//AAApPWwDDEFCQ0QwMTIzNDU2SBAAAGgCL9A='
threefive.decode(mesg)
```

* __Hex__

```python3
hexed='0xFC302F000000000000FFFFF014054800008F7FEFFE7369C02EFE0052CCF500000000000A0008435545490000013562DBA30A'
threefive.decode(hexed)
```

* __Read a string directly from a file__ encoded in __Base64__, __Binary__ or  __Base64__

```bash
$ cat cue.dat
    /DCSAAAAAAAAAP/wBQb/RgeVUgB8AhdDVUVJbs6+VX+/CAgAAAAABy0IxzELGQIXQ1VFSW7MmIh/vwgIAAABGDayFhE3AQECHENVRUluzw0If/8AABvLoAgIAAAAAActVhIwDBkCKkNVRUluzw02f78MG1JUTE4xSAEAAAAAMTM3NjkyMDI1NDQ5NUgxAAEAAGnbuXg=
```
*
```python3
from threefive import decode

decode('cue.dat')


```
 [🡡 top](#rocket-threefive)
 
#  __Advanced__ threefive

##  __Cue__ Class

   *  src [cue.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/cue.py)
   *  The __threefive.Cue__ class decodes a SCTE35 binary, base64, or hex encoded string. 
   *  __threefive.Cue__ provides several methods to access the parsed data.

```python3
from threefive import Cue

b64 = "/DBIAAAAAAAA///wBQb+ek2ItgAyAhdDVUVJSAAAGH+fCAgAAAAALMvDRBEAAAIXQ1VFSUgAABl/nwgIAAAAACyk26AQAACZcuND"

cue = Cue(b64)
cue.decode()
```

* A decoded __Cue__ instance contains: 

     * **cue.info_section** 
       * 1 [threefive.**SpliceInfoSection()**](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/section.py)

     * **cue.command** 	 
       * 1 of these commands:
       
         *  [ threefive.**BandwidthReservation()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L32)    
         *  [ threefive.**PrivateCommand()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L54 )
         *  [ threefive.**SpliceInsert()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L139)
         * [ threefive.**SpliceNull()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L43) 
         *  [ threefive.**TimeSignal()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L84)


     * **cue.descriptors**  
        * a list of 0 or more of these descriptors :   
         
          * [ threefive.**AudioDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L153)  
          * [ threefive.**AvailDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L50)  
          * [ threefive.**DtmfDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L78)  
          * [ threefive.**SegmentationDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L201)  
          * [threefive.**TimeDescriptor()**](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L119)

     *  __crc__
     
     * 'When parsing SCTE35 Cues from MPEGTS streams, 
       threefive attempts to include as many of the 
       following as possible.'   	
       *  __pid__ of the packet  
       *  __program__ of the pid 
       *  __pts__ of the packet 



* All instance vars can be accessed via dot notation.

```python3
>>>> from threefive import Cue
>>>> cue = Cue(b64)
>>>> cue.decode()
True
>>>> cue.command
{'command_length': 5, 'command_type': 6, 'name': 'Time Signal', 'time_specified_flag': True, 'pts_time': 22798.906911}
>>>> cue.command.pts_time
22798.906911
>>>> 
```

* call one or more of these methods after decode.

|Cue Method                  | Description                                    |
|----------------------------|------------------------------------------------|
| cue.**get()**              | returns **cue as a dict**                      |
| cue.**get_info_section()** | returns **cue.info_section as a dict**         |
| cue.**get_command()**      | returns **cue.command as a dict**              |
| cue.**get_descriptors()**  | returns **cue.descriptors as a list of dicts**.|
| cue.**get_json()**         | returns **cue as a JSON** string               |
| cue.**show()**             | prints **cue as JSON**                         |
|                            |                                                |

* Full Example 
```python3
>>>> from threefive import Cue

>>>> b64 = "/DBIAAAAAAAA///wBQb+ek2ItgAyAhdDVUVJSAAAGH+fCAgAAAAALMvDRBEAAAIXQ1VFSUgAABl/nwgIAAAAACyk26AQAACZcuND"

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
        "section_length": 72,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0xff",
        "tier": "0xfff",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 50
    },
    "command": {
        "command_length": 5,
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 22798.906911
    },
    "descriptors": [
        {
            "tag": 2,
            "descriptor_length": 23,
            "identifier": "CUEI",
            "name": "Segmentation Descriptor",
            "segmentation_event_id": "0x48000018",
            "segmentation_event_cancel_indicator": false,
            "components": [],
            "program_segmentation_flag": true,
            "segmentation_duration_flag": false,
            "delivery_not_restricted_flag": false,
            "web_delivery_allowed_flag": true,
            "no_regional_blackout_flag": true,
            "archive_allowed_flag": true,
            "device_restrictions": "No Restrictions",
            "segmentation_message": "Program End",
            "segmentation_upid_type": 8,
            "segmentation_upid_length": 8,
            "segmentation_upid": "0x2ccbc344",
            "segmentation_type_id": 17,
            "segment_num": 0,
            "segments_expected": 0
        },
        {
            "tag": 2,
            "descriptor_length": 23,
            "identifier": "CUEI",
            "name": "Segmentation Descriptor",
            "segmentation_event_id": "0x48000019",
            "segmentation_event_cancel_indicator": false,
            "components": [],
            "program_segmentation_flag": true,
            "segmentation_duration_flag": false,
            "delivery_not_restricted_flag": false,
            "web_delivery_allowed_flag": true,
            "no_regional_blackout_flag": true,
            "archive_allowed_flag": true,
            "device_restrictions": "No Restrictions",
            "segmentation_message": "Program Start",
            "segmentation_upid_type": 8,
            "segmentation_upid_length": 8,
            "segmentation_upid": "0x2ca4dba0",
            "segmentation_type_id": 16,
            "segment_num": 0,
            "segments_expected": 0
        }
    ],
    "crc": "0x9972e343"
}



```

[🡡 top](#rocket-threefive)

___

##  __Stream__ Class

 ```python3
  threefive.Stream(tsdata, show_null = False)
  ```

  * src [stream.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/stream.py)
  * The threefive.__Stream__ class parses SCTE35 messages from a file or stream.
  * Supports 
  	* __Multiple Programs__.
  	* __Multiple SCTE35 Streams__.
  	* __Multi-Packet PAT,PMT, and SCTE35 data__. 

  *  __tsdata__ is an open file handle. 
  *  __show_null__ if set to __True__, enables showing SCTE 35 __null commands__.
   
Method                              | Description
------------------------------------| -------------------------------------
[Stream.__show__()](#streamshow)                 |__Prints__ all recognized Programs and streams by pid and type. 
 [Stream.__decode__(func=show_cue)](#streamdecodefuncshow_cue)                                                                             | __Prints__ SCTE-35 __cues__ for SCTE-35 packets. Accepts an optional function, func, as arg.
[Stream.__decode_next__()](#streamdecode_next)|__Returns__ the next SCTE35 cue as a threefive.Cue instance. 
[Stream.__decode_program__(the_program=None, func=show_cue)](#streamdecode_programthe_program-func--show_cue) |Same as Stream.__decode__ except only packets where program == __the_program__
[Stream.__decode_proxy__(func=show_cue)](#streamdecode_proxyfunc--show_cue)      |Same as Stream.__decode__ except raw packets are written to stdout for piping to another program.

#### Stream.show()

 *  List programs and streams for a video.

```python3
>>>> from threefive import Stream, version
>>>> version()
'2.2.69'
>>>> with open('video.ts','rb') as tsdata:
....     strm = Stream(tsdata)
....     strm.show()
....     


Program 1030

        PMT pid: 1030
        PCR pid: 1031
        Descriptor: tag: 5 length: 4 data: b'CUEI'
        1031: [0x1b] Video
        1032: [0x3] ISO/IEC 11172 Audio
        1034: [0x6] SO/IEC 13818-1 PES packets- private data
        1035: [0x86] SCTE 35

Program 1100

        PMT pid: 1100
        PCR pid: 1101
        Descriptor: tag: 5 length: 4 data: b'CUEI'
        1101: [0x1b] Video
        1102: [0x3] ISO/IEC 11172 Audio
        1104: [0x6] SO/IEC 13818-1 PES packets- private data
        1105: [0x86] SCTE 35

Program 1080

        PMT pid: 1080
        PCR pid: 1081
        1081: [0x1b] Video
        1082: [0x3] ISO/IEC 11172 Audio
        1084: [0x6] SO/IEC 13818-1 PES packets- private data

Program 1010

        PMT pid: 1010
        PCR pid: 1011
        Descriptor: tag: 5 length: 4 data: b'CUEI'
        1011: [0x1b] Video
        1012: [0x3] ISO/IEC 11172 Audio
        1014: [0x6] SO/IEC 13818-1 PES packets- private data
        1015: [0x86] SCTE 35
	
Program 1050

        PMT pid: 1050
        PCR pid: 1051
        Descriptor: tag: 5 length: 4 data: b'CUEI'
        1051: [0x1b] Video
        1052: [0x3] ISO/IEC 11172 Audio
        1054: [0x6] SO/IEC 13818-1 PES packets- private data
        1055: [0x86] SCTE 35


```


#### Stream.decode(func=show_cue)
 
 ```python3
 import sys
 from threefive import Stream
 
 if __name__ =='__main__':
    with open(sys.argv[1],'rb') as tsdata:
        sp = Stream(tsdata)
        sp.decode()

```

  *   Pass in custom function 

  *  __func__ should match the interface 
  ``` func(cue)```
 
 
```python3
import sys
import threefive

def display(cue):
   print(f'\033[92m{cue.packet_data}\033[00m')
   print(f'{cue.command.name}')

def do():
   with open(sys.argv[1],'rb') as tsdata:
    sp = threefive.Stream(tsdata)
    sp.decode(func = display)       

if __name__ == '__main__':
    do()
```

#### Stream.decode_next()

* Stream.decode_next returns the next SCTE35 cue as a threefive.Cue instance.

```python3
import sys
import threefive

def do():
    arg = sys.argv[1]
    with open(arg,'rb') as tsdata:
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

#### Stream.decode_program(the_program, func = show_cue)

* Use Stream.__decode_program()__ instead of Stream.__decode()__ 
to decode SCTE-35 from packets where program == __the_program__

```python3
import threefive

with open('../35.ts','rb') as tsdata:
    threefive.Stream(tsdata).decode_program(1)
```

#### Stream.decode_proxy(func = show_cue)

*  Writes all packets to __sys.stdout__.

*  Writes scte35 data to __sys.stderr__.

```python3

import threefive

with open('vid.ts','rb') as tsdata:
    sp = threefive.Stream(tsdata)
    sp.proxy_decode()
```

* Pipe to __mplayer__
```bash
$ python3 proxy.py | mplayer -
```

![Happy threefive users](https://github.com/futzu/SCTE35-threefive/blob/master/threefiveishappy.jpg)


[🡡 top](#rocket-threefive)
