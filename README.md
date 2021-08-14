
> threefive is a __SCTE-35 Decoder__ / Parser library in Python3.

* [Requirements](#requirements)
* [Install threefive](#install)
* [Versions and Releases](#versions-and-releases)
* [Fast Start](https://github.com/futzu/SCTE35-threefive/blob/master/FastStart.md) 
* [Super Cool Examples ](https://github.com/futzu/SCTE35-threefive/tree/master/examples#threefive-examples)  


*   [__Easy threefive__ ](#the-decode-function)
      *   [threefive.__decode()__](#the-decode-function)
       
*  [__Advanced threefive__](#cue-class)         
     *  [threefive.__Cue__](#cue-class)         
     *  [threefive.__Stream__ Class](#stream-class)
     ---
     
 
* [threefive Spotted in The Wild](https://gist.github.com/flavioribeiro/9b52c603c70cdb34c6910c1c5c4d240d)

* [__ffmpeg__ and __SCTE35__ and __Stream Type__ and __threefive__](https://github.com/futzu/SCTE35-threefive/blob/master/threefive-ffmpeg.md)

*  [Code of Conduct](https://github.com/futzu/threefive/blob/master/CODE_OF_CONDUCT.md).

* [Issues and Bugs and Feature Requests](#issues-and-bugs-and-feature-requests)



### Requirements
threefive requires python 3.6+ or [pypy3](https://pypy.org)

### Install
   
```sh
pip3 install threefive

# for pypy3
pypy3 -m pip install threefive
```

### Versions and Releases

 >  __Release__ versions are  __odd__.
  
  > __Unstable__ testing versions are __even__.

> ```threefive.version()```   returns the version as a string.

> ```threefive.version_number()``` returns an int for easy version comparisons.

---


### __Easy__ threefive

####   The __decode__ Function

 > __threefive.decode__ is an all purpose function to decode SCTE 35 Cues.
 

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

     * 'When parsing SCTE35 Cues from MPEGTS streams, 
       threefive attempts to include as many of the 
       following as possible.'   	        
* *  __pid__ of the packet  
* *  __program__ of the pid   
* *  __pts__ of the packet   
* *  __pcr__ of the packet 
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


