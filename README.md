#### [__x9k3__](https://github.com/futzu/x9k3) is an __HLS segmenter__ with __SCTE-35__ support powered by __threefive__. 


# threefive is a  SCTE-35 parser lib in python3.


   * Supports All __2020 SCTE-35__
     [Commands](https://github.com/futzu/threefive/blob/master/threefive/commands.py) and
     [Descriptors](https://github.com/futzu/threefive/blob/master/threefive/descriptors.py) and
     [Upids](https://github.com/futzu/threefive/blob/master/threefive/upid.py).
* [Parses SCTE-35 from MPEGTS Streams with Direct Multicast Support ](#mpegts-multicast).
* [`HLS?`   `Custom Upid Handling?`     `Frame Accurate Preroll timings?`... Yes.](https://github.com/futzu/SCTE35-threefive/tree/master/examples#threefive-examples)
https://github.com/futzu/x9k3_


* [A threefive SCTE-35 Cue](https://github.com/futzu/threefive/blob/master/cue.md).What's included.

* [`ffmpeg` and `SCTE35` and `Stream Type 0x6 bin data` and threefive](https://github.com/futzu/SCTE35-threefive/blob/master/threefive-ffmpeg.md)
---

* [`Encoding` too](https://github.com/futzu/scte35-threefive/blob/master/Encoding.md) with [`Examples`](https://github.com/futzu/scte35-threefive/blob/master/examples/encode)
* [`Issues` and `Bugs` and `Feature Requests`](https://github.com/futzu/scte35-threefive/issues)
 *No forms man, just open an issue and tell me what you need.* 

---
* [__Install threefive__](#install)
* [Versions and Releases](#versions-and-releases)

* [__Fast Start__](https://github.com/futzu/SCTE35-threefive/blob/master/FastStart.md) 
    
*  [threefive.__Cue__ Class](#cue-class)         
*  [threefive.__Stream__ Class](#stream-class)
     
* [__Super Cool Examples__](https://github.com/futzu/SCTE35-threefive/blob/master/examples/README.md)

* [Diagram](https://github.com/futzu/threefive/blob/master/cue.md)  of a threefive SCTE-35 Cue
* [`Issues` and `Bugs` and `Feature` Requests](#issues-and-bugs-and-feature-requests)
 *No forms man, just open an issue.*  


### Requirements
* threefive requires [pypy3](https://pypy.org) or python 3.6+ 
* __optional dependencies:__
    *  __pyaes__  If you want AES decryption for HLS segments.

### Install
   
```smalltalk
python3 -mpip  install  threefive

# and / or

pypy3 -m pip install threefive

```
* To install the optional dependencies.
* 
```lua
python3 -mpip  install threefive[all]

# and / or

pypy3 -mpip  install  threefive[all]

```

### Versions and Releases

 >  __Release__ versions are  __odd__.
  > __Unstable__ testing versions are __even__.

> ```threefive.version()```   returns the version as a string.

---

#### Easy Examples

###### Base64
```python3
>>> from threefive import Cue
>>> stuff = '/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g='
>>> cue=Cue(stuff)
>>> cue.decode()
True
```
##### Bytes
```python3
>>> import threefive 

>>> stuff = b'\xfc0\x11\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00O%3\x96'
>>> cue=Cue(stuff)
>>> cue.decode()
True
>>> cue.show()
```
##### Hex
```python3
import threefive 

cue = threefive.Cue("0XFC301100000000000000FFFFFF0000004F253396")
cue.decode()
cue.show()
```
#### Mpegts Multicast
```python3
import threefive 

strm = threefive.Stream('udp://@239.35.0.35:1234')
strm.decode()
````

___
* [Why Plan9 Matters](http://9p.io/sources/contrib/uriel/mirror/9book.pdf)
___


###  Cue Class

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

* When parsing Cues from MPEGTS, threefive tries to include,  	        
   *   __pid__ of the packet  
   *  __program__ of the pid   
   *  __pts__ of the packet   
   *  __pcr__ of the packet 
___
```js

class Cue(threefive.base.SCTE35Base)
 |  Cue(data=None, packet_data=None)
 
```
```js 
 |  __init__(self, data=None, packet_data=None)
 |      data may be packet bites or encoded string
 |      packet_data is a instance passed from a Stream instance
```
#### Cue.decode()
```js
 |  decode(self)
 |      Cue.decode() parses for SCTE35 data
```
#### Cue.get()
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

### Cue.get() omits cue.bites and empty values

>>> cue.get()
{'info_section': {'table_id': '0xfc', 'section_syntax_indicator': False,'private': False, 'sap_type': '0x3', 
'sap_details': 'No Sap Type', 'section_length': 17, 'protocol_version': 0, 'encrypted_packet': False,
'encryption_algorithm': 0, 'pts_adjustment_ticks': 0, 'pts_adjustment': 0.0, 'cw_index': '0x0', 'tier': '0xfff',
'splice_command_length': 4095, 'splice_command_type': 0, 'descriptor_loop_length': 0, 'crc': '0x4f253396'},
'command': {'command_type': 0, 'name': 'Splice Null'},
'descriptors': []}
```

```
#### Cue.get_descriptors()
```js
 |  get_descriptors(self)
 |      Cue.get_descriptors returns a list of
 |      SCTE 35 splice descriptors as dicts.
```
#### Cue.get_json()
```js 
 |  get_json(self)
 |      Cue.get_json returns the Cue instance
 |      data in json.
```
#### Cue.show()
```js  
 |  show(self)
 |      Cue.show prints the Cue as JSON
```
#### Cue.to_stderr()
```js 
 |  to_stderr(self)
 |      Cue.to_stderr prints the Cue
```
___

###  __Stream__ Class
  * src [stream.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/stream.py)
  * The threefive.__Stream__ class parses __SCTE35__ from __Mpegts__.
  * Supports:
     *  __File__ and __Http(s)__ and __Udp__ and __Multicast__ protocols. 
  	 * __Multiple Programs__.
  	 * __Multi-Packet PAT, PMT, and SCTE35 tables__. 

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

#### Stream.decode(func=show_cue)
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

#### Stream.decode_next()

* Stream.decode_next returns the next SCTE35 cue as a threefive.Cue instance.
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
___


#### Stream.decode_program(the_program, func = show_cue)

* Use Stream.__decode_program()__ instead of Stream.__decode()__ 
to decode SCTE-35 from packets where program == __the_program__

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


#### Stream.decode_proxy(func = show_cue)

*  Writes all packets to __sys.stdout__.

*  Writes scte35 data to __sys.stderr__.

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

* Pipe to __mplayer__
```bash
$ python3 proxy.py | mplayer -
```
___

#### Stream.show()

 *  List programs and streams and info for MPEGTS
  ```js
 |  show(self)
 |      displays streams that will be
 |      parsed for SCTE-35.
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
#### Stream.decode_fu(func = show_cue)

 ```js
 |  decode_fu(self, func=show_cue)
 |      Stream.decode_fu decodes
 |      2016 packets at a time.
 ```

#### Stream.dump(fname)
 ```js
 |  dump(self, fname)
 |      Stream.dump dumps all the packets to a file (fname).
 ```
#### Stream.strip_scte35(func=show_cue_stderr)
 
 ```js
 |  strip_scte35(self, func=show_cue_stderr)
 |      Stream.strip_scte35 works just like Stream.decode_proxy,
 |      MPEGTS packets, ( Except the SCTE-35 packets) ,
 |      are written to stdout after being parsed.
 |      SCTE-35 cues are printed to stderr.
```

___



