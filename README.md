 
 [Install](#install) | [Fast Start](https://github.com/futzu/SCTE35-threefive/blob/master/FastStart.md)  | 
 [Cue](#cue-class)  |  [Stream](#stream-class) |
 [Examples](https://github.com/futzu/SCTE35-threefive/blob/master/examples/README.md)  |
  [ffmpeg and threefive](https://github.com/futzu/SCTE35-threefive/blob/master/threefive-ffmpeg.md) | [charsets for upids](#upidscharset) | [x9k3](https://github.com/futzu/) 

___

  # threefive is Pythonic SCTE-35. 
___
![image](https://user-images.githubusercontent.com/52701496/200188208-c94464bf-7e6a-44c1-a7fe-0fab927606aa.png)

#### threefive parses  All __2022__ SCTE35  
  - [x] [Commands](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py)
 - [x] [Descriptors](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py)
 - [x] [Upids](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/upids.py)


#### Be cool. 
* [Install threefive](#install)
* Do you have a limited attention span? 
   * [Fast Start](https://github.com/futzu/SCTE35-threefive/blob/master/FastStart.md) 
* [Versions and Releases](#versions-and-releases)

####  threefive is classy.
  *  [Cue Class](#cue-class)         
  *  [Stream Class](#stream-class)
#### help(threefive)
* [__Super Cool Examples__](https://github.com/futzu/SCTE35-threefive/blob/master/examples/README.md)
* [ffmpeg and SCTE35 and Stream Type 0x6 bin data and threefive](https://github.com/futzu/SCTE35-threefive/blob/master/threefive-ffmpeg.md)
*  2>&1 
   * I don't get any sort of notification for Discussions, please just open an issue for anything so I don't miss your post. 
   * [Issues and Bugs and Feature Requests *No forms man, just open an issue and tell me what you need.*  ](https://github.com/futzu/scte35-threefive/issues)
* [Diagram of a threefive SCTE-35 Cue. ](https://github.com/futzu/threefive/blob/master/cue.md)  
* [ __x9k3__ , SCTE35 hls segmenter powered by __threefive__](https://github.com/futzu/x9k3)
* [__m3ufu__, m3u8 parser powered by __threefive__](https://github.com/futzu/m3ufu)
* [__Project Super Kabuki__](https://github.com/futzu/threefive/blob/master/superkabuki.md) SCTE35 MPEGTS Packet Injection.



---
### `Q.` 
Is python fast enough to parse video?


###  `A.` 
Oh, yeah. 
---



### `Requirements`
* threefive requires 
  * [pypy3](https://pypy.org) or python 3.6+ 
  * [new_reader](https://github.com/futzu/new_reader)
* optional dependencies:
    *  __pyaes__  If you want AES decryption for HLS segments.

### `Install`
  
```smalltalk
python3 -mpip  install  threefive

# and / or

pypy3 -m pip install threefive

```
  `To install the optional dependencies`

```lua
python3 -mpip  install threefive[all]

# and / or

pypy3 -mpip  install  threefive[all]

```
---
### `Versions and Releases`
```lua
Python 3.10.6 (main, Aug 10 2022, 11:19:32) [GCC 12.1.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from threefive import version
>>> version()
'2.3.45'
>>> 
```
*  I do [__Rolling Releases__](https://en.wikipedia.org/wiki/Rolling_release)
* __Release__ versions are  __odd__.
* __Unstable__ testing versions are __even__.


---
### `upids.charset`
`Specify a charset for Upid data by setting threefive.upids.charset` [`issue #55`](https://github.com/futzu/scte35-threefive/issues/55)

* default charset is ascii
* python charsets info [Here](https://docs.python.org/3/library/codecs.html)
* setting charset to None will return raw bytes.

*  `threefive.upids.charset` will set a charset for the following upid types:

   * `0x01` (Deprecated)
   * `0x02` (Deprecated)
   * `0x03` (AdID)
   * `0x07` (TID)
   * `0x09` (ADI)
   * `0x10` (UUID) 
   * `0x11` (SCR) 
   * `0x0E` (ADS Info)
   * `0x0F` (URI)
   * `0xFD` (Unknown)
   * `0x0B` (ATSC) _only applied to_ `content_id`
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

> Q. Why not change the default to latin-1 instead of ascii?

> A. Because latin-1 and ascii are different.
```lua
>>>> a=b'\xfc0'
>>>> a.decode(encoding="ascii",errors='backslashreplace')
'\\xfc0'
>>>> a.decode(encoding="latin-1",errors='backslashreplace')
'ü0'
>>>> a.decode(encoding="latin-1",errors='backslashreplace').encode()
b'\xc3\xbc0'
>>>> a.decode(encoding="ascii",errors='backslashreplace').encode()
b'\\xfc0'
>>>> 
```
---
### `Easy Examples`
> threefive is a library. 
>
> A library means you dont have to write a lot of code. 
>
> Most SCTE-35 parsing can be done in a few lines.
___
##### `Mpegts Multicast`

```python3
import threefive 

strm = threefive.Stream('udp://@239.35.0.35:1234')
strm.decode()
````
#### Mpegts over Https
```python3
import threefive
strm = threefive.Stream('https://iodisco.com/ch1/ready.ts')
strm.decode()

```

##### Base64
```python3
>>> from threefive import Cue
>>> stuff = '/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g='
>>> cue=Cue(stuff)
>>> cue.decode()
True
```
##### `Bytes`
```python3
>>> import threefive 

>>> stuff = b'\xfc0\x11\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00O%3\x96'
>>> cue=Cue(stuff)
>>> cue.decode()
True
>>> cue.show()
```
##### `Hex`
```python3
import threefive 

cue = threefive.Cue("0XFC301100000000000000FFFFFF0000004F253396")
cue.decode()
cue.show()
```

___

# Documentation for classes and methods 


##  `Cue Class`

   *  src [cue.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/cue.py)
   *  The __threefive.Cue__ class decodes a SCTE35 binary, base64, or hex encoded string. 
   
```python3
    >>>> import threefive
    >>>> Base64 = "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g="
    >>>> cue = threefive.Cue(Base64)
```

*  cue.decode() returns True on success,or False if decoding failed
```python3
    >>>> cue.decode()
    True
```
* After Calling cue.decode() the instance variables can be accessed via dot notation.
```python3

    >>>> cue.command
    {'calculated_length': 5, 'name': 'Time Signal', 'time_specified_flag': True, 'pts_time': 21695.740089}

    >>>> cue.command.pts_time
    21695.740089

    >>>> cue.info_section.table_id

    '0xfc'
```

```js

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
___

##  `Stream Class`
  * src [stream.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/stream.py)
  * The threefive.__Stream__ class parses __SCTE35__ from __Mpegts__.
  * Supports:
     *  __File__ and __Http(s)__ and __Udp__ and __Multicast__ protocols. 
  	 * __Multiple Programs__.
  	 * __Multi-Packet PAT, PMT, and SCTE35 tables__. 
 
* threefive tries to include __pid__, __program__,  __pts__, and __pcr__ of the SCTE-35 packet.

  

```js
class Stream(builtins.object)
 |  Stream(tsdata, show_null=True)
 |  
 |  Stream class for parsing MPEG-TS data.
 ```
 ```js
 |  __init__(self, tsdata, show_null=True)
 |      
 |      tsdata is a file or http, https, 
 |       udp or multicast url.
 |       
 |      set show_null=False to exclude Splice Nulls
 |      
 |      Use like...
 |      
 |      from threefive import Stream
 |      strm = Stream("vid.ts",show_null=False)
 |      strm.decode()
 ```

* `Stream.decode(func=show_cue)`
 ```js
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


* `Stream.decode_program(the_program, func = show_cue)`

 ```js
 |  decode_program(self, the_program, func=show_cue)
 |      Stream.decode_program limits SCTE35 parsing
 |      to a specific MPEGTS program.
 ```
 > `Stream.decode_program Example`
```python3
import threefive
threefive.Stream('35.ts').decode_program(1)
```
___


* `Stream.decode_proxy(func = show_cue)`

  *  Writes all packets to sys.stdout.

  *  Writes scte35 data to sys.stderr.

 ```js
 |  decode_proxy(self, func=show_cue_stderr)
 |      Stream.decode_proxy writes all ts packets are written to stdout
 |      for piping into another program like mplayer.
 |      SCTE-35 cues are printed to stderr.
 ```
> `Stream.decode_proxy Example`
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

* `Stream.dump(fname)`
 ```js
 |  dump(self, fname)
 |      Stream.dump dumps all the packets to a file (fname).
 ```
 * `Stream.strip_scte35(func=show_cue_stderr)`
 
 ```js
 |  strip_scte35(self, func=show_cue_stderr)
 |      Stream.strip_scte35 works just like Stream.decode_proxy,
 |      MPEGTS packets, ( Except the SCTE-35 packets) ,
 |      are written to stdout after being parsed.
 |      SCTE-35 cues are printed to stderr.
```


___
## `UUID`
* [__RFC 4122__ aka UUID](https://tools.ietf.org/html/rfc4122.html)
> A lot of folks have been searching this repo for uuid, I'm not sure if they are looking for uuid in a upid, 
> or a randomly generated uuid for an HLS tag or something else.
> Here is what I know about it. 

```smalltalk
>>> from uuid import uuid4, UUID

# generate a random uuid
>>> uu= uuid4()
>>> uu
UUID('7ae2e37e-3018-4c4e-8a10-f69d075828b4')

# uuid as bytes
>>> uu.bytes
b'z\xe2\xe3~0\x18LN\x8a\x10\xf6\x9d\x07X(\xb4'

# bytes to uuid
>>> UUID(bytes=uu.bytes)
UUID('7ae2e37e-3018-4c4e-8a10-f69d075828b4')
>>> 

Adrian

```
[__python3 uuid__](https://docs.python.org/3/library/uuid.html#module-uuid)

   
![image](https://user-images.githubusercontent.com/52701496/189712191-a576a240-a5f1-47d1-9975-2435ef791975.png)
