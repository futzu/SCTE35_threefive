
### threefive is a fast and accurate and non-validating SCTE-35 parser python3 lib. 

___


> Q. __How many lines of code doe it take to parse SCTE35 from Mpegts__?

> A. __Two__. 
```python3

from threefive import decode

decode("https://futzu.com/xaa.ts")

```
#### If the question is about SCTE-35 parsing threefive is probably the answer.
 
---

   * Supports All __2020 SCTE-35__
      [`Commands`](https://github.com/futzu/threefive/blob/master/threefive/commands.py) and
     [`Descriptors`](https://github.com/futzu/threefive/blob/master/threefive/descriptors.py) and
     [`Upids`](https://github.com/futzu/threefive/blob/master/threefive/upid.py).
   * [Parses`Mpegts`](#stream-class)  and [Decrypts `AES` ](https://github.com/futzu/scte35-threefive/blob/901456089d369e8cd81c0dc3c2bd6600e303562e/threefive/segment.py#L37) 
  * [`ffmpeg` and `SCTE35` and `Stream Type 0x6 bin data` and threefive](https://github.com/futzu/SCTE35-threefive/blob/master/threefive-ffmpeg.md)

* [A threefive SCTE-35 Cue](https://github.com/futzu/threefive/blob/master/cue.md).What's included.
* [`35decode`, a cli tool](https://github.com/futzu/threefive/blob/master/examples/35decode)

*  [Direct Multicast Support ](#mpegts-multicast)
* [`Heads Up`. New output format for `threefive.Stream.show()`](#streamshow) just pushed.

*  [`HLS?`   `Custom Upid Handling?`     `Frame Accurate Preroll timings?`... Yes.](https://github.com/futzu/SCTE35-threefive/tree/master/examples#threefive-examples)
* [`Encoding` too](https://github.com/futzu/scte35-threefive/blob/master/Encoding.md) with [`Examples`](https://github.com/futzu/scte35-threefive/blob/master/examples/encode)
* [`Issues` and `Bugs` and `Feature Requests`](#issues-and-bugs-and-feature-requests)
 *No forms man, just open an issue and tell me what you need.* 

* [`Heads Up`. New output format for `threefive.Stream.show()`](#streamshow) just pushed.

---

* [Requirements](#requirements)
* [__Install threefive__](#install)
* [Versions and Releases](#versions-and-releases)

* [__Fast Start__](https://github.com/futzu/SCTE35-threefive/blob/master/FastStart.md) 

*   [`Easy` threefive](#easy-threefive) 
      *   [threefive.__decode__()](#easy-threefive)      

*  [`Advanced` threefive](#advanced-threefive)     
     *  [threefive.__Cue__ Class](#cue-class)         
     *  [threefive.__Stream__ Class](#stream-class)
     
* [__Super Cool Examples__](https://github.com/futzu/SCTE35-threefive/blob/master/examples/README.md)

* [Diagram](https://github.com/futzu/threefive/blob/master/cue.md)  of a threefive SCTE-35 Cue
* [`Issues` and `Bugs` and `Feature` Requests](#issues-and-bugs-and-feature-requests)
 *No forms man, just open an issue.*  
* [threefive Spotted `in The Wild`](https://gist.github.com/flavioribeiro/9b52c603c70cdb34c6910c1c5c4d240d)


### Requirements
* threefive requires [pypy3](https://pypy.org) or python 3.6+ 
    * (pypy3 runs threefive 4x Faster than python3 but uses a lot more memory)
* threefive 2.3.02+ requires __crcmod__ for encoding and __pyaes__ for decrypting.

 

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


* [```Acme Jet Propelled Unicycle```](https://www.ebay.com/itm/124520782156?chn=ps&mkevt=1&mkcid=28)


### __Easy__ threefive

> the tsduck user's manual is longer than threefive's source code.

>
> __threefive.decode__ is a SCTE-35 decoder function
> with input type __auto-detection__. 
```Base64```, ```Binary```, 
> ```Hex Strings```,```Hex literals```, ```Integers```, ```Mpegts files``` and ```Mpegts HTTP/HTTPS Streams```
> 
> __SCTE-35__ data can be __parsed__ 
> with just __one function call__.
  
> SCTE-35 data is __printed in JSON__ format.


#### Examples:

###### Base64
```python3
import threefive 

stuff = '/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g='
threefive.decode(stuff)
```
##### Bytes
```python3
import threefive 

payload = b'\xfc0\x11\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00O%3\x96'
threefive.decode(payload)
```
##### Hex String
```python3
import threefive 

stuff = '0XFC301100000000000000FFFFFF0000004F253396'
threefive.decode(stuff)
```
##### Hex Literal
```python3
import threefive 

threefive.decode(0XFC301100000000000000FFFFFF0000004F253396)
```
##### Integer
```python3
big_int = 1439737590925997869941740173214217318917816529814
threefive.decode(big_int)
```
##### Mpegts File
```python3
import threefive 

threefive.decode('/path/to/mpegts')
```
##### Mpegts HTTP/HTTPS Streams
```python3
import threefive 

threefive.decode('https://futzu.com/xaa.ts')
````
#### Mpegts UDP streams
```python3
import threefive 

threefive.decode('udp://10.0.0.1:555')
````
#### Mpegts Multicast
```python3
import threefive 

threefive.decode('udp://@239.35.0.35:1234')
````
* [__A threefive SCTE-35 Cue__](https://github.com/futzu/threefive/blob/master/cue.md)

___

#  Advanced threefive

___

###  Cue Class


   *  src [cue.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/cue.py)
   *  The __threefive.Cue__ class decodes a SCTE35 binary, base64, or hex encoded string. 
   *  __threefive.Cue__ provides several methods to access the parsed data.
   
```python3
    >>>> import threefive
    >>>> Base64 = "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g="
    >>>> cue = threefive.Cue(Base64)
```

> cue.decode() returns True on success,or False if decoding failed
```python3
    >>>> cue.decode()
    True
```
> After Calling cue.decode() the instance variables can be accessed via dot notation.
```python3

    >>>> cue.command
    {'calculated_length': 5, 'name': 'Time Signal', 'time_specified_flag': True, 'pts_time': 21695.740089}

    >>>> cue.command.pts_time
    21695.740089

    >>>> cue.info_section.table_id

    '0xfc'
```

> When parsing SCTE35 Cues from MPEGTS streams, 
> threefive attempts to include as many of the 
> following as possible.'   	        
*   __pid__ of the packet  
*  __program__ of the pid   
*  __pts__ of the packet   
*  __pcr__ of the packet 
___


* call one or more of these methods after decode.

|Cue Method                  | Description                                    |
|----------------------------|------------------------------------------------|
| cue.**get()**              | returns **cue as a dict**                      |
| cue.**get_json()**         | returns **cue as a JSON** string               |
| cue.**show()**             | prints **cue as JSON**                         |
|                            |                                                |



___

###  __Stream__ Class


 ```python3
  threefive.Stream(tsdata, show_null = False)
  ```

  * src [stream.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/stream.py)
  * The threefive.__Stream__ class parses __SCTE35__ from __Mpegts__.
  * Supports:
     *  __File__ and __Http(s)__ and __Udp__ and __Multicast__ protocols. 
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
>>>> from threefive import Stream
>>>> Stream('https://slo.me/plp0.ts').show()
```

```js
Program: 1040
    Service:    fumatic
    Provider:   fu-labs
    Pcr Pid:    1041[0x411]
    Streams:
                Pid: 1041[0x411]        Type: 0x1b AVC Video
                Pid: 1042[0x412]        Type: 0x3 MP2 Audio
                Pid: 1044[0x414]        Type: 0x6 PES Packets/Private Data
                Pid: 1045[0x415]        Type: 0x86 SCTE35 Data

Program: 1050
    Service:    fancy ˹ 
    Provider:   fu-corp
    Pcr Pid:    1051[0x41b]
    Streams:
                Pid: 1051[0x41b]        Type: 0x1b AVC Video
                Pid: 1052[0x41c]        Type: 0x3 MP2 Audio
                Pid: 1054[0x41e]        Type: 0x6 PES Packets/Private Data
                Pid: 1055[0x41f]        Type: 0x86 SCTE35 Data

```
___


#### Stream.decode(func=show_cue)
 
 ```python3
 import sys
 from threefive import Stream
 >>>> Stream('plp0.ts').decode()

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
threefive.Stream('35.ts').decode_program(1)
```
___


#### Stream.decode_proxy(func = show_cue)

*  Writes all packets to __sys.stdout__.

*  Writes scte35 data to __sys.stderr__.

```python3

import threefive
sp = threefive.Stream('https://futzu.com/xaa.ts')
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

---


