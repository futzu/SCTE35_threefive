# threefive
> threefive is a __SCTE-35 Decoder / Parser library in Python3__ .
> 
> threefive references the __2020 SCTE-35__ Specification.
>
>  threefive decodes __SCTE-35__ from __MPEG-TS video__ files and streams.
>
>threefive decodes __SCTE-35__ from __Base64, Hex, and Binary__ encoded strings.
>
>  threefive decodes __SCTE-35__ from streams transcoded by __ffmpeg__ as[` Data: bin_data ([6][0][0][0] / 0x0006)`](https://github.com/futzu/SCTE35-threefive/blob/master/threefive-ffmpeg.md).
>
>  threefive is now testing a [__Golang__  version too.](https://github.com/futzu/threefive/tree/master/go).
>  
___

*   [Versions and Releases](#versions-and-releases)

*   [Install threefive](#install)

*   [Quick Start](https://github.com/futzu/SCTE35-threefive/blob/master/FastStart.md) 



*   [__Easy threefive__ (Using the decode function )](#the-decode-function)

     * [Mpeg-TS Streams](#the-decode-function) 
     * [Mpeg-TS Streams over HTTPS](#the-decode-function) 
     * [Base64, or Hex encoded strings](#the-decode-function) 
     * [ Hex Values and Integers](#the-decode-function)
    ---
       
       
*  [__Advanced threefive__](#cue-class)         
     *  [__Cue__ Class](#cue-class)         
     *  [__Stream__ Class](#stream-class)
     ---
     
*  [__Examples__](https://github.com/futzu/SCTE35-threefive/tree/master/examples#threefive-examples) 
     * [Upids_with Custom Output](https://github.com/futzu/threefive/blob/master/examples/upid/upid_custom_output.py)
      
     * [SCTE-35 from MPEG-TS video over HTTPS](https://github.com/futzu/SCTE35-threefive/blob/master/examples/stream/decode_http.py)
       
     * [Multiple Segmentation Descriptors](https://github.com/futzu/threefive/blob/master/examples/upid/multi_upid.py)
      
      * [Parsing HLS Manifests with threefive](https://github.com/futzu/SCTE35-threefive/tree/master/examples/hls)
        
      * [SCTE-35 from a Multicast Stream](https://github.com/futzu/SCTE35-threefive/blob/master/examples/multicast/README.txt)
             
      * [Time Signal Program Start End](https://github.com/futzu/threefive/blob/master/examples/timesignal/time_signal_blackout_override_program_end.py)
      
      * [All Examples](https://github.com/futzu/SCTE35-threefive/tree/master/examples#threefive-examples)  
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
a@fumatica:~/threefive$ pypy3

Python 3.6.12 (7.3.3+dfsg-3, Feb 25 2021, 22:28:03)
[PyPy 7.3.3 with GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>> from threefive import version
>>>> version()
'2.2.82'
```

### Install
---

* Requires python 3.6+ or pypy3
> [threefive runs 3x Faster on pypy3  ](https://github.com/futzu/threefive/blob/master/py3vspypy3.md#threefive--python3-vs-pypy3)

*  __install from pip__ (recommended)
   
```python3
$ pip3 install threefive

# for pypy3
$ pypy3 -mpip install threefive

#If you don't have pip installed, try this.
$ pypy3 -mensurepip install pip 
```
___

*  __install from git__

```python3
$ git clone https://github.com/futzu/threefive.git

$ cd threefive
$ make install

# for pypy3 
$ make pypy3
```
___

## __Easy__ threefive

###   The __decode__ Function

 *   src [decode.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/decode.py)   
 * __threefive.decode__ is an all purpose function to decode SCTE 35 messages from a file or string.
 
 ```python3
import threefive
```
 *   __MpegTS__
 
```python3
threefive.decode('/path/to/mpegwithscte35.ts') 
```
 * __MpegTS__ over __http and https__
 
 ```python3
threefive.decode('https://futzu.com/xaa.ts') 
```
* __Base64__ 

```python3
mesg='/DA4AAAAAAAA///wBQb+AAAAAAAiAiBDVUVJAAAAA3//AAApPWwDDEFCQ0QwMTIzNDU2SBAAAGgCL9A='
threefive.decode(mesg)
```
* __Hex String__

```python3
hexed = "0xFC301100000000000000FFFFFF0000004F253396"
threefive.decode(hexed)
```
* __Hex Values( New! )__ 
```python3
raw_hex = 0XFC301100000000000000FFFFFF0000004F253396
threefive.decode(raw_hex)
```
* __Integers ( New! )__ 
```python3
big_int = 1439737590925997869941740173214217318917816529814
threefive.decode(big_int)
```
* __Read a string directly from a file__ encoded in __Base64__, __Binary__ or  __Hex__
```bash
$ cat cue.dat
   /DBIAAAAAAAA///wBQb+ek2ItgAyAhdDVUVJSAAAGH+fCAgAAAAALMvDRBEAAAIXQ1VFSUgAABl/nwgIAAAAACyk26AQAACZcuND
```
*
```python3
from threefive import decode

decode('cue.dat')

```

___

##  Advanced threefive

___

###  Cue Class
```py3
class Cue(builtins.object)
 |  The threefive.Splice class handles parsing
 |  SCTE 35 message strings.
 |  Example usage:
 |  
 |  from threefive import Cue
 |  
 |  Base64 = "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g="
 |  scte35 = Cue(Base64)
 |  scte35.decode()
 |  scte35.show()
 |  
 |  Methods defined here:
 |  
 |  __init__(self, data=None, packet_data=None)
 |      data may be packet bites or encoded string
 |      packet_data is a dict passed from a Stream instance
 |  
 |  __repr__(self)
 |  
 |  decode(self)
 |      Cue.decode() parses for SCTE35 data
 |  
 |  get(self)
 |      Cue.get returns a dict of dicts
 |      for all three parts of a SCTE 35 message.
 |  
 |  get_descriptors(self)
 |      Cue.get_descriptors returns a list of
 |      SCTE 35 splice descriptors as dicts.
 |  
 |  get_json(self)
 |      Cue.get_json returns the Cue instance
 |      data in json.
 |  
 |  mk_info_section(self, bites)
 |      Cue.mk_info_section parses the
 |      Splice Info Section
     of a SCTE35 cue.
 |  
 |  show(self)
 |      Cue.show pretty prints the SCTE 35 message
 |  
 |  to_stderr(self)
 |      Cue.to_stderr is a Wrapper
 |      for printing to sys.stderr
 |  
 |  ----------------------------------------------------------------------
```
---

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
         
          * [ threefive.**AudioDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L48)  
          * [ threefive.**AvailDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L80)  
          * [ threefive.**DtmfDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L94)  
          * [ threefive.**SegmentationDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L137)  
          * [threefive.**TimeDescriptor()**](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L115)

     *  __crc__
     
     * 'When parsing SCTE35 Cues from MPEGTS streams, 
       threefive attempts to include as many of the 
       following as possible.'   	
       *  __pid__ of the packet  
       *  __program__ of the pid 
       *  __pts__ of the packet 
       *  __pcr__ of the packet 
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
```py3
class Stream(builtins.object)
 |  Stream class for parsing MPEG-TS data.
 |  
 |  Methods defined here:
 |  
 |  __init__(self, tsdata, show_null=True)
 |      tsdata is an open file handle
 |      set show_null=False to exclude Splice Nulls
 |      
 |      Use like...
 |      
 |      from threefive import Stream
 |      
 |      with open("vid.ts",'rb') as tsdata:
 |          strm = Stream(tsdata,show_null=False)
 |          strm.decode()
 |  
 |  __repr__(self)
 |  
 |  decode(self, func=show_cue)
 |      Stream.decode reads self.tsdata to find SCTE35 packets.
 |      func can be set to a custom function that accepts
 |      a threefive.Cue instance as it's only argument.
 |  
 |  decode_fu(self, func=show_cue)
 |      Stream.decode_fu decodes
 |      1000 packets at a time.
 |  
 |  decode_next(self)
 |      Stream.decode_next returns the next
 |      SCTE35 cue as a threefive.Cue instance.
 |  
 |  decode_program(self, the_program, func=show_cue)
 |      Stream.decode_program limits SCTE35 parsing
 |      to a specific MPEGTS program.
 |  
  decode_proxy(self, ffunc=show_cue_stderr)
 |      Stream.decode_proxy writes all ts packets are written to stdout
 |      for piping into another program like mplayer.
 |      SCTE-35 cues are printed to stderr.
 |  
 |  show(self)
 |      displays streams that will be
 |      parsed for SCTE-35.
 |  
 |  ----------------------------------------------------------------------

```

---


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



> [Jimmy?](http://runjimmyrunrunyoufuckerrun.com/rc/)
