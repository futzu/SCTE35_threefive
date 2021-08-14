# threefive
> threefive is a __SCTE-35 Decoder / Parser library in Python3__ .
> 
> threefive references the __2020 SCTE-35__ Specification.

> threefive is [__Easy__ to use.](https://github.com/futzu/SCTE35-threefive/blob/master/FastStart.md) Check out these [ __Examples__](https://github.com/futzu/SCTE35-threefive/tree/master/examples#threefive-examples)  

___

* [ Little Help? ](#i-could-use-some-help)

*   [Versions and Releases](#versions-and-releases)

*   [Install threefive](#install)

*   [Fast Start](https://github.com/futzu/SCTE35-threefive/blob/master/FastStart.md) 


*   [__Easy threefive__ (Using the decode function )](#the-decode-function)
       
*  [__Advanced threefive__](#cue-class)         
     *  [__Cue__ Class](#cue-class)         
     *  [__Stream__ Class](#stream-class)
     ---
     
*  [__Examples__](https://github.com/futzu/SCTE35-threefive/tree/master/examples#threefive-examples) 
    
    * [ Parsing SCTE35 from MPEGTS over HTTPS](https://github.com/futzu/threefive/blob/master/examples/stream/cool_decode_http.py) (__New and Improved!__)
    
    * [Parsing HLS Manifests with threefive](https://github.com/futzu/SCTE35-threefive/tree/master/examples/hls) (__New Code!__) 

     * [Stream.__decode_proxy()__ Example](https://github.com/futzu/SCTE35-threefive/blob/master/examples/stream/decode_proxy.py)
     
     * [Show preroll](https://github.com/futzu/threefive/blob/master/examples/stream/preroll.py)

     * [Upids_with Custom Output](https://github.com/futzu/threefive/blob/master/examples/upid/upid_custom_output.py)
                        
      * [Multicast Stream Server and Client for SCTE-35](https://github.com/futzu/SCTE35-threefive/blob/master/examples/multicast/README.txt)
                   
     ---
 
* [threefive Spotted in The Wild](https://gist.github.com/flavioribeiro/9b52c603c70cdb34c6910c1c5c4d240d)

* [__ffmpeg__ and __SCTE35__ and __Stream Type__ and __threefive__](https://github.com/futzu/SCTE35-threefive/blob/master/threefive-ffmpeg.md)

*  [Code of Conduct](https://github.com/futzu/threefive/blob/master/CODE_OF_CONDUCT.md).

* [Issues and Bugs and Feature Requests](#issues-and-bugs-and-feature-requests)

---


## Versions and Releases
---

> __Odd__ numbered __Versions__ are __Releases__.
> 
> __Even__ numbered __Versions__ are __Testing Builds__ and may be __Unstable__.
> 
```python3
>>>> from threefive import version
>>>> version()
'2.2.98'

# the version_number function returns an int for easy version comparisons

version_number()
2298
```

### Install
---

* Requires python 3.6+ or pypy3
> [threefive runs 3x Faster on pypy3  ](https://github.com/futzu/threefive/blob/master/py3vspypy3.md#threefive--python3-vs-pypy3)

*  Pip Install
   
```python3
$ pip3 install threefive

# for pypy3
$ pypy3 -mpip install threefive
```

*  Git Install

```python3
$ git clone https://github.com/futzu/threefive.git

$ cd threefive
$ make install

# for pypy3 
$ make pypy3
```
___

# __Easy__ threefive

>  "Give the people what they want"  ~ __Ray Davies__ 
>
##   The __decode__ Function

 > __threefive.decode__ is an all purpose function to decode SCTE 35 Cues.
 
|     Input Type    | Function Call                                             |
|-------------------|-----------------------------------------------------------|
|  __MpegTS__       |  ```  decode('/path/to/mpegwithscte35.ts')  ```           |
| __Http/Https__    |  ```decode('https://futzu.com/xaa.ts')  ```               |
| __Base64 Encoded__|  ```decode('/DA4AAAAAAAA///wBQb+AAAAAAAiAiBDVUVJAAAAA3//AAApPWwDDEFCQ0QwMTIzNDU2SBAAAGgCL9A=')```                               |
| __Hex String__    | ```decode("0xFC301100000000000000FFFFFF0000004F253396")```|
|                   |                                                           |
|                   |                                                           |
|                   |                                                           |
|                   |                                                           |



######  threefive.decode Supports:


* ```Mpeg-TS Video```       
     
* * From Files  
* * Over HTTP/HTTPS  
* * Piped to  STDIN
     
* ```Base64, Hex Strings, and Bytes```

* * As Strings
* * from Files
* * Piped to STDIN
     
* ```Hex and Integer Values```
* * As Numerical Values
* * From Files,
* * Piped to STDIN 

> ```py3
> 
> from threefive import decode
>   
> ```


 >  MpegTS
 
```python3

decode('/path/to/mpegwithscte35.ts') 

```
 > Http / Https
 
 ```python3 
 decode('https://futzu.com/xaa.ts') 
 ```
 
 
> Base64 

```python3

mesg='/DA4AAAAAAAA///wBQb+AAAAAAAiAiBDVUVJAAAAA3//AAApPWwDDEFCQ0QwMTIzNDU2SBAAAGgCL9A='

decode(mesg)

```
* Hex String

```python3

hexed = "0xFC301100000000000000FFFFFF0000004F253396"

decode(hexed)

```
* Hex Values
 
```python3

raw_hex = 0XFC301100000000000000FFFFFF0000004F253396

decode(raw_hex)

```
* Integers
```python3

big_int = 1439737590925997869941740173214217318917816529814

decode(big_int)

```
* Read a string directly from a file [cue.txt](https://github.com/futzu/threefive/files/6986120/cue.txt)

```python3

decode('cue.txt')

```

___

#  Advanced threefive

___

###  Cue Class


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
       
         *  [ threefive.**BandwidthReservation()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L35)    
         *  [ threefive.**PrivateCommand()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L47 )
         *  [ threefive.**SpliceInsert()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L105)
         * [ threefive.**SpliceNull()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L63) 
         *  [ threefive.**TimeSignal()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L76)


     * **cue.descriptors**  
        * a list of 0 or more of these descriptors :   
         
        [ threefive.**AudioDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L48) |  [ threefive.**AvailDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L80)  |  [ threefive.**DtmfDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L94)  | [ threefive.**SegmentationDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L137)  |  [threefive.**TimeDescriptor()**](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L115)

     *  __crc__
     
     * 'When parsing SCTE35 Cues from MPEGTS streams, 
       threefive attempts to include as many of the 
       following as possible.'   	         __pid__ of the packet  *  __program__ of the pid   *  __pts__ of the packet   *  __pcr__ of the packet 
___


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
| cue.**get_json()**         | returns **cue as a JSON** string               |
| cue.**show()**             | prints **cue as JSON**                         |
|                            |                                                |

___


* Full Example 
```python3

from threefive import Cue
b64 = "/DBIAAAAAAAA///wBQb+ek2ItgAyAhdDVUVJSAAAGH+fCAgAAAAALMvDRBEAAAIXQ1VFSUgAABl/nwgIAAAAACyk26AQAACZcuND"
cue.decode(b64)
cue_data = cue.get()

```
___

###  __Stream__ Class


 ```python3
  threefive.Stream(tsdata, show_null = False)
  ```

  * src [stream.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/stream.py)
  * The threefive.__Stream__ class parses SCTE35 messages from a file or stream.
  * Supports 
  	* __Multiple Programs__.
  	* __Multiple SCTE35 Streams__.
  	* __Multi-Packet PAT, PMT, and SCTE35 tables__. 
  	* __Constant Data Parsing__.
  	     * threefive.Stream is designed to __run continuously__ 
  	     
Method                              | Description
------------------------------------| -------------------------------------
[Stream.__show__()](#streamshow)                 |__Prints__ Streams that will be checked for SCTE35 
 [Stream.__decode__(func=show_cue)](#streamdecodefuncshow_cue)                                                                             | __Prints__ SCTE-35 __cues__ for SCTE-35 packets. Accepts an optional function, func, as arg.
[Stream.__decode_next__()](#streamdecode_next)|__Returns__ the next SCTE35 cue as a threefive.Cue instance. 
[Stream.__decode_program__(the_program=None, func=show_cue)](#streamdecode_programthe_program-func--show_cue) |Same as Stream.__decode__ except only packets where program == __the_program__
[Stream.__decode_proxy__(func=show_cue)](#streamdecode_proxyfunc--show_cue)      |Same as Stream.__decode__ except raw packets are written to stdout for piping to another program.


#### Stream.show()

 *  List programs and streams that will be checked for SCTE35 data.

```python3
>>>> from threefive import Stream, version
>>>> version()
'2.2.69'
>>>> with open('video.ts','rb') as tsdata:
....     strm = Stream(tsdata)
....     strm.show()
....     

Program:1030
        PID: 1034(0x40a) Type: 0x6
        PID: 1035(0x40b) Type: 0x86 SCTE35

Program:1100
        PID: 1104(0x450) Type: 0x6
        PID: 1105(0x451) Type: 0x86 SCTE35

Program:1080
        PID: 1084(0x43c) Type: 0x6

```
___


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
___


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
___


#### Stream.decode_program(the_program, func = show_cue)

* Use Stream.__decode_program()__ instead of Stream.__decode()__ 
to decode SCTE-35 from packets where program == __the_program__

```python3
import threefive

with open('../35.ts','rb') as tsdata:
    threefive.Stream(tsdata).decode_program(1)
```
___


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
___




## Issues and Bugs and Feature Requests
---
> __Speak up. I want to hear what you have to say__. 
>   
> __If threefive__ doesn't work as expected, 
> 
> __or__ if you find a bug , 
> 
> __or__ if you have feature request, 
> 
> __please open an issue__. 

> If you want help resolving a video parsing issue, __a sample of the video is required__ .

---

# I could use some help.....

1. Someone with some DASH skills, threefive needs some DASH examples. 
---
2. Anybody want to write some tests for threefive?
---
3. Docker folks. I have some really cool stuff, I want to deploy. 
---   

> [Jimmy?](http://runjimmyrunrunyoufuckerrun.com/rc/)
