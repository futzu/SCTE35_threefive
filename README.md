# Threefive<a name="threefive"></a>

- threefive is a __SCTE-35 Decoder / Parser library in Python3__.

- threefive references the __2020 SCTE-35__ Specification.

- threefive decodes __SCTE-35__ from __MPEG-TS video__ files and streams.

- threefive decodes __SCTE-35__ from __Base64, Hex, and Binary__ encoded strings.

- threefive decodes __SCTE-35__ from __ffmpeg__ [` Data: bin_data ([6][0][0][0] / 0x0006)`](https://github.com/futzu/SCTE35-threefive/blob/master/threefive-ffmpeg.md) streams.

## Table of Contents<a name="table-of-contents"></a>

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=1 -->

- [Threefive](#threefive)
  - [Table of Contents](#table-of-contents)
  - [Versions and Releases](#versions-and-releases)
  - [Install](#install)
    - [Pip package](#pip-package)
      - [Python 3](#python-3)
      - [Pypy 3](#pypy-3)
    - [Build from source](#build-from-source)
  - [Overview](#overview)
    - [The decode Function](#the-decode-function)
  - [Advanced threefive](#advanced-threefive)
    - [Cue Class](#cue-class)
    - [Stream Class](#stream-class)
      - [Stream.show()](#streamshow)
      - [Stream.decode(func=show_cue)](#streamdecodefuncshow_cue)
      - [Stream.decode_next()](#streamdecode_next)
      - [Stream.decode_program(the_program, func = show_cue)](#streamdecode_programthe_program-func--show_cue)
      - [Stream.decode_proxy(func = show_cue)](#streamdecode_proxyfunc--show_cue)

<!-- mdformat-toc end -->

## Versions and Releases<a name="versions-and-releases"></a>

- Odd numbered versions are releases.
- Even numbered versions are testing builds between versions

```python3
a@fumatica:~/threefive$ pypy3

Python 3.6.12 (7.3.3+dfsg-3, Feb 25 2021, 22:28:03)
[PyPy 7.3.3 with GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>> from threefive import version
>>>> version()
'2.2.82'
```

## Install<a name="install"></a>

### Pip package<a name="pip-package"></a>

Requires Python 3.6+ or pypy3

#### Python 3<a name="python-3"></a>

```python3
pip3 install threefive
```

#### Pypy 3<a name="pypy-3"></a>

```bash
$ pypy3 -mpip install threefive
```

### Build from source<a name="build-from-source"></a>

```bash
git clone https://github.com/futzu/threefive.git
```

```bash
cd threefive
```

```bash
make install
```

```
make pypy3
```

## Overview<a name="overview"></a>

### The __decode__ Function<a name="the-decode-function"></a>

- src [decode.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/decode.py)

- __threefive.decode__ is an all purpose function to decode SCTE 35 messages from a file or string.

- __MpegTS__

```python3
import threefive
threefive.decode('/path/to/mpegwithscte35.ts')

```

- New in __v.2.2.69__ threefive.decode can parse __MpegTS__ over __http and https__

```python3
import threefive
threefive.decode('https://futzu.com/xaa.ts')

```

- __Base64__

```python3
mesg='/DA4AAAAAAAA///wBQb+AAAAAAAiAiBDVUVJAAAAA3//AAApPWwDDEFCQ0QwMTIzNDU2SBAAAGgCL9A='
threefive.decode(mesg)
```

- __Hex__

```python3
hexed = "0xFC301100000000000000FFFFFF0000004F253396"
threefive.decode(hexed)
```

- __Read a string directly from a file__ encoded in __Base64__, __Binary__ or  __Base64__

```bash
$ cat cue.dat
/DBIAAAAAAAA///wBQb+ek2ItgAyAhdDVUVJSAAAGH+fCAgAAAAALMvDRBEAAAIXQ1VFSUgAABl/nwgIAAAAACyk26AQAACZcuND
```

-

```python3
from threefive import decode

decode('cue.dat')

```

______________________________________________________________________

![openbsdransom](https://user-images.githubusercontent.com/52701496/117953431-04568a00-b2e4-11eb-85eb-a26d7d4c9045.png)

______________________________________________________________________

## __Advanced__ threefive<a name="advanced-threefive"></a>

______________________________________________________________________

### __Cue__ Class<a name="cue-class"></a>

- src [cue.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/cue.py)
- The __threefive.Cue__ class decodes a SCTE35 binary, base64, or hex encoded string.
- __threefive.Cue__ provides several methods to access the parsed data.

```python3
from threefive import Cue

b64 = "/DBIAAAAAAAA///wBQb+ek2ItgAyAhdDVUVJSAAAGH+fCAgAAAAALMvDRBEAAAIXQ1VFSUgAABl/nwgIAAAAACyk26AQAACZcuND"

cue = Cue(b64)
cue.decode()
```

______________________________________________________________________

- A decoded __Cue__ instance contains:

  - **cue.info_section**

    - 1 [threefive.**SpliceInfoSection()**](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/section.py)

  - **cue.command**

    - 1 of these commands:

      - [ threefive.**BandwidthReservation()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L32)
      - [ threefive.**PrivateCommand()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L54)
      - [ threefive.**SpliceInsert()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L139)
      - [ threefive.**SpliceNull()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L43)
      - [ threefive.**TimeSignal()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/commands.py#L84)

  - **cue.descriptors**

    - a list of 0 or more of these descriptors :

      - [ threefive.**AudioDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L153)
      - [ threefive.**AvailDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L50)
      - [ threefive.**DtmfDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L78)
      - [ threefive.**SegmentationDescriptor()** ](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L201)
      - [threefive.**TimeDescriptor()**](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptors.py#L119)

  - __crc__

  - 'When parsing SCTE35 Cues from MPEGTS streams,
    threefive attempts to include as many of the
    following as possible.'

    - __pid__ of the packet
    - __program__ of the pid
    - __pts__ of the packet
    - __preroll__ ( difference between the packet pts and the pts specified in a TimeSignal or SpliceInsert)

______________________________________________________________________

- All instance vars can be accessed via dot notation.

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

- call one or more of these methods after decode.

| Cue Method         | Description                      |
| ------------------ | -------------------------------- |
| cue.**get()**      | returns **cue as a dict**        |
| cue.**get_json()** | returns **cue as a JSON** string |
| cue.**show()**     | prints **cue as JSON**           |
|                    |                                  |

______________________________________________________________________

- Full Example

```python3

from threefive import Cue
b64 = "/DBIAAAAAAAA///wBQb+ek2ItgAyAhdDVUVJSAAAGH+fCAgAAAAALMvDRBEAAAIXQ1VFSUgAABl/nwgIAAAAACyk26AQAACZcuND"
cue.decode(b64)
cue_data = cue.get()

```

______________________________________________________________________

### __Stream__ Class<a name="stream-class"></a>

```python3
 threefive.Stream(tsdata, show_null = False)
```

- src [stream.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/stream.py)

- The threefive.__Stream__ class parses SCTE35 messages from a file or stream.

- Supports

  - __Multiple Programs__.
  - __Multiple SCTE35 Streams__.
  - __Multi-Packet PMT, and SCTE35 data__.
  - __Constant Data Parsing__.
    - threefive.Stream is designed to __run continuously__
    - __Longest run reported__: a single Stream instance parsing video __nonstop for 47 days__.

- __tsdata__ is an open file handle.

- __show_null__ if set to __True__, enables showing SCTE 35 __null commands__.

| Method                                                                                                        | Description                                                                                       |
| ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| [Stream.__show__()](#streamshow)                                                                              | __Prints__ Streams that will be checked for SCTE35                                                |
| [Stream.__decode__(func=show_cue)](#streamdecodefuncshow_cue)                                                 | __Prints__ SCTE-35 __cues__ for SCTE-35 packets. Accepts an optional function, func, as arg.      |
| [Stream.__decode_next__()](#streamdecode_next)                                                                | __Returns__ the next SCTE35 cue as a threefive.Cue instance.                                      |
| [Stream.__decode_program__(the_program=None, func=show_cue)](#streamdecode_programthe_program-func--show_cue) | Same as Stream.__decode__ except only packets where program == __the_program__                    |
| [Stream.__decode_proxy__(func=show_cue)](#streamdecode_proxyfunc--show_cue)                                   | Same as Stream.__decode__ except raw packets are written to stdout for piping to another program. |

#### Stream.show()<a name="streamshow"></a>

- List programs and streams that will be checked for SCTE35 data.

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

Program:1010
        PID: 1014(0x3f6) Type: 0x6
        PID: 1015(0x3f7) Type: 0x86 SCTE35

```

______________________________________________________________________

#### Stream.decode(func=show_cue)<a name="streamdecodefuncshow_cue"></a>

```python3
import sys
from threefive import Stream

if __name__ =='__main__':
   with open(sys.argv[1],'rb') as tsdata:
       sp = Stream(tsdata)
       sp.decode()

```

- Pass in custom function

- __func__ should match the interface
  ` func(cue)`

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

______________________________________________________________________

#### Stream.decode_next()<a name="streamdecode_next"></a>

- Stream.decode_next returns the next SCTE35 cue as a threefive.Cue instance.

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

______________________________________________________________________

#### Stream.decode_program(the_program, func = show_cue)<a name="streamdecode_programthe_program-func--show_cue"></a>

- Use Stream.__decode_program()__ instead of Stream.__decode()__
  to decode SCTE-35 from packets where program == __the_program__

```python3
import threefive

with open('../35.ts','rb') as tsdata:
    threefive.Stream(tsdata).decode_program(1)
```

______________________________________________________________________

#### Stream.decode_proxy(func = show_cue)<a name="streamdecode_proxyfunc--show_cue"></a>

- Writes all packets to __sys.stdout__.

- Writes scte35 data to __sys.stderr__.

```python3

import threefive

with open('vid.ts','rb') as tsdata:
    sp = threefive.Stream(tsdata)
    sp.proxy_decode()
```

- Pipe to __mplayer__

```bash
$ python3 proxy.py | mplayer -
```

______________________________________________________________________
