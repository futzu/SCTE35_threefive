
# :rocket: threefive
## threefive is a SCTE35 Parser library in Python3.
   
*   __2019a SCTE-35__ in about 900 lines of code.

*   __threefive__ is __simple__ and __easy__ to use. 
 	*  [__Up and Running in Less Than Seven Seconds__](https://github.com/futzu/SCTE35-threefive/blob/master/FastStart.md) 

  	* __SCTE-35__ can be parsed from strings or video with __one function__  [__threefive.decode()__](#the-decode-function).
  	*  threefive __automatically identifies__ and parses __Base64, Hexidecimal__, or __Binary__ .  
  	*   __Multiple programs__ and __multiple SCTE-35 streams__ are __well__ supported.
	*  __SCTE35 cues__ up to __4096 bytes__ long can be __parsed from video__ streams or __encoded__ strings. 
___

## Why __so many releases__?
 *  I generate [__a lot of releases__](https://github.com/futzu/SCTE35-threefive/releases), however the interface to classes and functions rarely [__changes__](#changes)
 *  Releases are made for __incremental improvements__. This __keeps pip and the git repo in sync__.
 *  Having several relases makes it much __easier to resolve__ [issues](https://github.com/futzu/SCTE35-threefive/issues)
 
---
#### [__Heads Up!__ Changes as of 1/1/2021](#changes)
* [ __threefive__ runs __three times faster__ with __pypy3__](https://www.pypy.org/)
* [__Requires__ Python __3.6 +__](https://www.python.org/downloads/release/python-390/)
* [ Latest __Pip__ Version]( https://pypi.org/project/threefive/)
*  [__Fast__ Start](#fast-start-directions)
      * [__Dependencies__](#dependencies)
      * [__Install__](#install)
      * [__Examples__](https://github.com/futzu/SCTE35-threefive/tree/master/examples)
* [__Easy__ threefive](#easy-threefive)
  *   [The __decode__ Function](#the-decode-function)
      * [Parsing __SCTE 35__ Cues from __Mpeg-TS Streams__](#the-decode-function)
      * [Parsing __SCTE 35__ Cue strings encoded in __Base64__, or __Hex__](#the-decode-function)
      * [Parsing __SCTE 35__ Cues directly from a file encoded in __Base64__, __Binary__,  or __Hex__](#the-decode-function)
      
*  [__Advanced threefive__](#advanced-threefive)
     *  [__Cue__ Class](#cue-class)
          * [Return __Cue__ instance as __dict__](#return-cue-instance-as-dict)   
          * [Return __Cue__ instance as __JSON__](#return-cue-instance-as-json)   
          * [Print __Cue__ instance as __JSON__](#print-cue-instance-as-json)   
     * [__Stream__ Class](#stream-class)
     	  * [Stream.__show__()](#streamshow) 
          * [Stream.__decode__(func=show_cue)](#streamdecodefuncshow_cue)                                                                
          * [Stream.__decode_next__()](#streamdecode_next)                                                                
          * [Stream.__decode_program__(the_program=None, func=show_cue)](#streamdecode_programthe_program-func--show_cue)
          * [Stream.__decode_proxy__(func=show_cue)](#streamdecode_proxyfunc--show_cue)    
 *   [__Examples__](https://github.com/futzu/SCTE35-threefive/tree/master/examples)
     * __HLS__
          * [Using threefive with __HLS Manifests__](https://github.com/futzu/SCTE35-threefive/tree/master/examples/hls)
     * __Multicast__
          * [Parsing SCTE-35 from a __Multicast__ Source](https://github.com/futzu/SCTE35-threefive/blob/master/examples/multicast/README.txt)
     * __Splice Insert__
          * [Splice __Insert__](https://github.com/futzu/SCTE35-threefive/blob/master/examples/spliceinsert/Splice_Insert.py)
          * [Splice __Insert__ Too](https://github.com/futzu/SCTE35-threefive/blob/master/examples/spliceinsert/Splice_Insert_Too.py)
     * __Splice_Null__
          * [Splice __Null__](https://github.com/futzu/SCTE35-threefive/blob/master/examples/splicenull)
     * __Time Signal__
          * [Time Signal __Blackout Override Program End__](https://github.com/futzu/SCTE35-threefive/blob/master/examples/timesignal/Time_Signal_Blackout_Override_Program_End.py)
          * [Time Signal __Placement Opportunity Start__](https://github.com/futzu/SCTE35-threefive/blob/master/examples/timesignal/Time_Signal-Placement_Opportunity_Start.py)
          * [Time Signal __Placement Opportunity End__](https://github.com/futzu/SCTE35-threefive/blob/master/examples/timesignal/Time_Signal-Placement_Opportunity_End.py)
          * [Time Signal __Program Overlap__ ](https://github.com/futzu/SCTE35-threefive/blob/master/examples/timesignal/Time_Signal-Program_Overlap.py)
          * [Time Signal __Program Start End__](https://github.com/futzu/SCTE35-threefive/blob/master/examples/timesignal/Time_Signal-Program_Start_End.py)
     * __UPID__
          * [__Upids__ with Custom Output](https://github.com/futzu/SCTE35-threefive/blob/master/examples/upid/Upid_Custom_Output.py)
          * [__Multiple__ Segmentation __Descriptors__](https://github.com/futzu/SCTE35-threefive/blob/master/examples/upid/Multi_Upid.py)
          * [Combination __Upid__ Segmentation Descriptor](https://github.com/futzu/SCTE35-threefive/blob/master/examples/upid/Upid_Combo.py)
     * __DTMF__
     	  * [DTMF __Descriptor__](https://github.com/futzu/SCTE35-threefive/blob/master/examples/dtmf)
     * __Stream__
          * [Stream.__decode_proxy()__ Example](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Proxy_Demo.py)
---

#### __Changes__
   *  Back by popular demand...   [Stream.__decode_next__()](#streamdecode_next)                                                                 

   *  As of threefive __v.2.2.39__  threefive.__Cue__ will require __Cue.decode()__ to be called to parse data.
   
 ```python3
  from threefive import Cue
  Base64 = "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g="
  cue = Cue(Base64)
  cue.decode()   # Now required
  cue.show()
```
                                    
   *   As of version __2.1.95__, __threefive.version__ returns a string for the current __version__. 
   ```python
   
     >>> import threefive
     >>> threefive.version()
    '2.2.35'
``` 
---

## Fast __Start_
*  [__Up and Running in Less Than Seven Seconds__](https://github.com/futzu/SCTE35-threefive/blob/master/FastStart.md) 
### Dependencies 
*  Python 3.6+ or pypy3
*  [__bitn__](https://github.com/futzu/bitn)
### Install 
*    __git__ 
```sh
git clone https://github.com/futzu/SCTE35-threefive.git

       cd SCTE-threefive
# you need root to install for the system
       make install

# for pypy3 
        make pypy3
```
*  __pip__

```sh
        pip3 install threefive

# for pypy3
        pypy3 -mpip install threefive

#If you don't have pip installed, try this.
        pypy3 -mensurepip install pip 

```

[🡡 top](#threefive)


## __Easy__ threefive

###   The __decode__ Function
 *   source [decode.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/decode.py)
 * __threefive.decode__ is an all purpose function to decode SCTE 35 messages from a file or string.
 *   __MpegTS__
```python
threefive.decode('/path/to/mpegwithscte35.ts') 
```
* __Base64__ 
```python
mesg='/DBUAAAAAAAA///wBQb+AAAAAAA+AjxDVUVJAAAACn+/Dy11cm46dXVpZDphYTg1YmJiNi01YzQzLTRiNmEtYmViYi1lZTNiMTNlYjc5OTkRAAB2c6LA'
threefive.decode(mesg)
```
* __Hex__
```python
hexed='0xFC302F000000000000FFFFF014054800008F7FEFFE7369C02EFE0052CCF500000000000A0008435545490000013562DBA30A'
threefive.decode(hexed)
```
 * __Directly from a file__ encoded in __Base64__, __Binary__ or  __Base64__
```sh
cat cue.dat
    /DCSAAAAAAAAAP/wBQb/RgeVUgB8AhdDVUVJbs6+VX+/CAgAAAAABy0IxzELGQIXQ1VFSW7MmIh/vwgIAAABGDayFhE3AQECHENVRUluzw0If/8AABvLoAgIAAAAAActVhIwDBkCKkNVRUluzw02f78MG1JUTE4xSAEAAAAAMTM3NjkyMDI1NDQ5NUgxAAEAAGnbuXg=
```

 *  __pass__ threefive.__decode__ the __file name__ and it will __parse__ it for __SCTE35__.

```js
from threefive import decode

decode('cue.dat')

{
  "info_section": {
    "table_id": "0xfc",
    "section_syntax_indicator": false,
    "private": false,
    "reserved": "0x3",
    
     <--Snipped for Brevity -->
     
    {
      "tag": 2,
      "identifier": "CUEI",
      "name": "Segmentation Descriptor",
      "segmentation_event_id": "0x6ecf0d36",
      "segmentation_event_cancel_indicator": false,
      "components": [],
      "program_segmentation_flag": true,
      "segmentation_duration_flag": false,
      "delivery_not_restricted_flag": true,
      "segmentation_message": "Content Identification",
      "segmentation_upid_type": 12,
      "segmentation_upid_length": 27,
      "segmentation_upid": "MPU:{'format identifier': 1381256270, 'private data': 4720207453582705227611785054965731163782383190579622144}",
      "segmentation_type_id": 1,
      "segment_num": 0,
      "segments_expected": 0,
      "descriptor_length": 42
    }
  ]
}
```
 [🡡 top](#threefive)
 
#  __Advanced__ threefive

##  __Cue__ Class
   *  source [cue.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/cue.py)
   *  The __threefive.Cue__ class decodes a SCTE35 binary, base64, or hex encoded string. 
   *  __threefive.Cue__ provides several methods to access the parsed data.

```python

from threefive import Cue

b64 = "/DBIAAAAAAAA///wBQb+ek2ItgAyAhdDVUVJSAAAGH+fCAgAAAAALMvDRBEAAAIXQ1VFSUgAABl/nwgIAAAAACyk26AQAACZcuND"

cue = Cue(B64)
cue.decode()
```
### __Return Cue__ instance as __dict__
```python
cue.get()

# Splice Info Section
cue.get_info_section()

# Splice Command
cue.get_command()

# Splice Descriptors
cue.get_descriptors()
````
### __Return Cue__ instance as __JSON__
```python
jason = cue.get_json()
```
### __Print Cue__ instance as __JSON__ 
```python
cue.show()
```    

 [🡡 top](#threefive)


##  __Stream__ Class

 ```python3
  threefive.Stream(tsdata, show_null = False)
  ```

  * source [stream.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/stream.py)

  * The threefive.__Stream__ class parses SCTE35 messages from a file or stream.

       *  __tsdata__ is an open file handle.
   
       *  __show_null__ if set to __True__, enables showing SCTE 35 __null commands__.
   
Method                              | Description
------------------------------------| -------------------------------------
[Stream.__show__()](#streamshow)                 |__Prints__ all recognized Programs and streams by pid and type. 
 [Stream.__decode__(func=show_cue)](#streamdecodefuncshow_cue)                                                                             | __Prints__ SCTE-35 __cues__ for SCTE-35 packets. Accepts an optional function, func, as arg.
[Stream.__decode_next__()](#streamdecode_next)|__Returns__ the next SCTE35 cue as a threefive.Cue instance. 
[Stream.__decode_program__(the_program=None, func=show_cue)](#streamdecode_programthe_program-func--show_cue) |Same as Stream.__decode__ except only packets where program == __the_program__
[Stream.__decode_proxy__(func=show_cue)](#streamdecode_proxyfunc--show_cue)      |Same as Stream.__decode__ except raw packets are written to stdout for piping to another program.

### ```Stream.show()```
 *  List programs and streams for a video.
```python3
# pypy3
>>>> from threefive import Stream, version
>>>> version
'2.2.09'
>>>> with open('video.ts','rb') as tsdata:
....     st = Stream(tsdata)
....     st.show()
....     

Program: 1030 (pcr pid: 1031)
	   1031: [0x1b] Video
	   1032: [0x3] ISO/IEC 11172 Audio
	   1034: [0x6] ITU-T Rec. H.222.0 | ISO/IEC 13818-1 PES packets with private data
	   1035: [0x86] SCTE 35

Program: 1100 (pcr pid: 1101)
	   1101: [0x1b] Video
	   1102: [0x3] ISO/IEC 11172 Audio
	   1104: [0x6] ITU-T Rec. H.222.0 | ISO/IEC 13818-1 PES packets with private data
	   1105: [0x86] SCTE 35

Program: 1080 (pcr pid: 1081)
	   1081: [0x1b] Video
	   1082: [0x3] ISO/IEC 11172 Audio
	   1084: [0x6] ITU-T Rec. H.222.0 | ISO/IEC 13818-1 PES packets with private data
```


### ```Stream.decode(func=show_cue)```
 
 ```python3
 
 import sys
 from threefive import Stream
 '''
 
 if __name__ =='__main__':
    with open(sys.argv[1],'rb') as tsdata:
        sp = Stream.decode_nextStream(tsdata)
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

### ```Stream.decode_next()```
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

### ```Stream.decode_program(the_program, func = show_cue)```

* Use Stream.__decode_program()__ instead of Stream.__decode()__ 
to decode SCTE-35 from packets where program == __the_program__

```python3
import threefive

with open('../35.ts','rb') as tsdata:
    threefive.Stream(tsdata).decode_program(1)
```

### ```Stream.decode_proxy(func = show_cue)```


*  Writes all packets to __sys.stdout__.

*  Writes scte35 data to __sys.stderr__.

```python3

   import threefive
      
   with open('vid.ts','rb') as tsdata:
      sp = threefive.Stream(tsdata)
      sp.proxy_decode()
```

* Pipe to __mplayer__
```
python3 proxy.py | mplayer -
```

[🡡 top](#threefive)
