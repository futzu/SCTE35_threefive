
# threefive is the undisputed heavyweight champion of SCTE-35.
### If you aren't using threefive, you're a loser and nobody likes you.

<br>⚡ `Decodes` __SCTE-35__.
<br>⚡ `Encodes` __SCTE-35__.
<br>⚡ `Parses` __SCTE-35__ from `Base64`, `Bytes`, `Hex`, `Integers`, and `MPEGTS` Streams.
<br>⚡ `Parses` __SCTE-36__ from `files`, `http(s)`, `Multicast`, `UDP` and even `stdin` _( you can pipe to it)_. 
<br>⚡ `Parses` __SCTE-35__ from streams converted to `bin data` ( _type 0x06_ ) by `ffmpeg`.



# Latest Version is `2`.`4`.`17`
### Heads Up, the new specification has field changes. 
> Most of you shouldn't have a problem, I think I've handled most of the potential issues.
> If you see something crazy, don't freak out, just open an issue, and we'll get it resolved.
* v2.4.15 fix for `encode.mk_splice insert` 
* v2.4.17 fix for `private descriptor` encoding
___

## [threefive has a lot of example SCTE-35 code](https://github.com/futzu/SCTE35-threefive/blob/master/examples/README.md)

# __Documentation__ _(click a topic to expand)_

<details><summary>Supported Platforms</summary> 
 
* threefive is expected to work on any platform that runs python3.6 and up.
* There are no known platform specific issues. 
  
</details>

<details><summary>Requirements</summary>

* threefive requires
  * [pypy3](https://pypy.org) or python 3.6+ (pypy3 runs threefive 2-3 times faster than python 3.10)
  * [new_reader](https://github.com/futzu/new_reader)
  *  __pyaes__


* [Install threefive](#install)
   * [Fast Start](https://github.com/futzu/SCTE35-threefive/blob/master/FastStart.md)
   * [Super Cool Examples](https://github.com/futzu/SCTE35-threefive/blob/master/examples/README.md)
* [Versions and Releases](#versions-and-releases)
</details>

<details><summary>Versions and Releases</summary>

Every time I fix a bug or add a feature, I do a new release. 
I only support the latest version. Stay up with me. 
```lua
a@fu:~$ pypy3
Python 3.9.17 (7.3.12+dfsg-1, Jun 16 2023, 18:55:49)
[PyPy 7.3.12 with GCC 12.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>> import threefive
>>>> threefive.version
'2.4.9'
>>>> 

```
* __Release__ versions are  __odd__.
* __Unstable__ testing versions are __even__.
</details>

 <details><summary>Parse SCTE-35 on the command line.</summary>
 
* `Parse base64`
```js
threefive '/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo='
```
* `Parse a hex value`
```js
threefive 0xFC302F000000000000FFFFF014054800008F7FEFFE7369C02EFE0052CCF500000000000A0008435545490000013562DBA30A
```
* `Parse MPEGTS from stdin`
```js
cat video.ts | threefive
```
* `Parse MPEGTS video over https`
```js
threefive https://so.slo.me/longb.ts
```
* `Parse multicast`
```lua
threefive udp://@235.35.3.5:3535
```

</details>

 <details><summary>Parse SCTE-35 programmatically with a few lines of code.</summary>

   <details><summary>Mpegts Multicast in three lines of code.</summary>

```python3
import threefive

strm = threefive.Stream('udp://@239.35.0.35:1234')
strm.decode()
````
  _(need an easy multicast server?_ [gumd](https://github.com/futzu/gumd) )

---
  </details>

 <details><summary>Mpegts over Https in three lines of code.</summary>

```python3
import threefive
strm = threefive.Stream('https://iodisco.com/ch1/ready.ts')
strm.decode()


       
   </details>

 <details><summary>Base64 in five lines of code.</summary>

```python3
>>> from threefive import Cue
>>> stuff = '/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g='
>>> cue=Cue(stuff)
>>> cue.decode()
True
 >>> cue.show()

```
---
   </details>

 <details><summary>Bytes in five lines of code.</summary>

```python3
>>> import threefive

>>> stuff = b'\xfc0\x11\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00O%3\x96'
>>> cue=Cue(stuff)
>>> cue.decode()
True
>>> cue.show()
```
---
   </details>

<details><summary>Hex in 4 lines of code.</summary>

```python3
import threefive

cue = threefive.Cue("0XFC301100000000000000FFFFFF0000004F253396")
cue.decode()
cue.show()
```
</details>

 </details>

<details><summary>Easy SCTE-35 encoding with threefive. </summary>

* Need SCTE-35 Packet Injection? [SuperKabuki](https://github.com/futzu/SuperKabuki), powered by threefive.


 * `Helper functions for SCTE35 Cue encoding`

```python3
Python 3.8.13 (7.3.9+dfsg-5, Oct 30 2022, 09:55:31)
[PyPy 7.3.9 with GCC 12.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>> import threefive.encode
>>>> help(threefive.encode)



Help on module threefive.encode in threefive:

NAME
    threefive.encode - encode.py

DESCRIPTION
    threefive.encode has helper functions for Cue encoding.

FUNCTIONS
    mk_splice_insert(event_id, pts=None, duration=None, out=False)
        mk_cue returns a Cue with a Splice Insert.

        The args set the SpliceInsert vars.

        splice_event_id = event_id

        if pts is None (default):
            splice_immediate_flag      True
            time_specified_flag        False

        if pts:
            splice_immediate_flag      False
            time_specified_flag        True
            pts_time                   pts

        If duration is None (default)
            duration_flag              False

        if duration IS set:
            out_of_network_indicator   True
            duration_flag              True
            break_auto_return          True
            break_duration             duration
            pts_time                   pts

        if out is True:
            out_of_network_indicator   True

        if out is False (default):
            out_of_network_indicator   False

    mk_splice_null()
        mk_splice_null returns a Cue
        with a Splice Null

    mk_time_signal(pts=None)
         mk_time_signal returns a Cue
         with a Time Signal
        if pts is None:
             time_specified_flag   False

        if pts IS set:
             time_specified_flag   True
             pts_time              pts

```
</details>



 <details><summary>Cue Class</summary>

   *  src [cue.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/cue.py)
   *  The __threefive.Cue__ class decodes a SCTE35 binary, base64, or hex encoded string.

```py3

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
* After Calling cue.decode() the __instance variables can be accessed via dot notation__.
```python3

    >>>> cue.command
    {'calculated_length': 5, 'name': 'Time Signal', 'time_specified_flag': True, 'pts_time': 21695.740089}

    >>>> cue.command.pts_time
    21695.740089

    >>>> cue.info_section.table_id

    '0xfc'
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
</details>

<details><summary>Stream Class</summary>

  * src [stream.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/stream.py)
  * The threefive.__Stream__ class parses __SCTE35__ from __Mpegts__.
  * Supports:
     *  __File__ and __Http(s)__ and __Udp__ and __Multicast__ protocols.
  	 * __Multiple Programs__.
  	 * __Multi-Packet PAT, PMT, and SCTE35 tables__.

* threefive tries to include __pid__, __program__, anf  __pts__ of the SCTE-35 packet.

```js
class Stream(builtins.object)
 |  Stream(tsdata, show_null=True)
 |
 |  Stream class for parsing MPEG-TS data.
 ```
 ```py3
 |  __init__(self, tsdata, show_null=True)
 |
 |      tsdata is a file or http, https,
 |       udp or multicast url.
 |
 |      set show_null=False to exclude Splice Nulls

 ```

* `Stream.decode(func=show_cue)`
 ```py3
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
    with open(arg,'rb',encoding="utf-8") as tsdata:
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

* `Stream.proxy(func = show_cue)`

  *  Writes all packets to sys.stdout.

  *  Writes scte35 data to sys.stderr.

 ```js
 |  decode(self, func=show_cue_stderr)
 |      Stream.decode_proxy writes all ts packets are written to stdout
 |      for piping into another program like mplayer.
 |      SCTE-35 cues are printed to stderr.
 ```
> `Stream.proxy Example`
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
    Service:    fancy ˹
    Provider:   fu-corp
    Pcr Pid:    1051[0x41b]
    Streams:
                Pid: 1051[0x41b]        Type: 0x1b AVC Video
                Pid: 1052[0x41c]        Type: 0x3 MP2 Audio
                Pid: 1054[0x41e]        Type: 0x6 PES Packets/Private Data
                Pid: 1055[0x41f]        Type: 0x86 SCTE35 Data

```
</details>


<details><summary> Need to verify your splice points? </summary> 
 

 
 
* Try [cue2vtt.py](https://github.com/futzu/scte35-threefive/blob/master/examples/stream/cue2vtt.py) in the examples.

   * cue2vtt.py creates webvtt subtitles out of SCTE-35 Cue data
 
* use it like this 

 ```rebol
 pypy3 cue2vtt.py video.ts | mplayer video.ts -sub -
```


 ![image](https://github.com/futzu/scte35-threefive/assets/52701496/5b8dbea3-1d39-48c4-8fbe-de03a53cc1dd)


---

</details> 

<details><summary>Custom charsets for UPIDS aka upids.charset</summary>

`Specify a charset for Upid data by setting threefive.upids.charset` [`issue #55`](https://github.com/futzu/scte35-threefive/issues/55)

* default charset is ascii
* python charsets info [Here](https://docs.python.org/3/library/codecs.html)
* setting charset to None will return raw bytes.


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

</details>

<details> <summary> Parse Custom Splice Descriptors</summary>


1.   Subclass `threefive.descriptors.SpliceDescriptor`
2. Add `self.private_data` to` __init__`
3. Add a `decode` method 
4. Add it to `threefive.descriptors.descriptor_map` tag:Class  `112: MDSNDescriptor`
```py3
import threefive

class MDSNDescriptor(threefive.descriptors.SpliceDescriptor):
    """
    MDSNDescriptor
    """
    def __init__(self, bites=None):
        super().__init__(bites)
        self.name = "MDSN Descriptor"
        self.private_data=None

    def decode(self):
        self.private_data="".join(list(self.bites[: self.descriptor_length -4].decode()))


if __name__ == '__main__':
    threefive.descriptors.descriptor_map[112]=MDSNDescriptor 

    cue = threefive.Cue('/DBlAAAAAAAAAP/wBQb+GVJTDABPcAZNRFNOQzUCRUNVRUkAAKTff8MAACky4A8xdXJuOnV1aWQ6QnJlYWstQjAwMjA4NTU2ODlfMDAxMi0wNy0xMC1YMDExMjUxNjEyNDAAAPkSB7E=')
    cue.decode()
    cue.show()

```


```json
a@debian:~/clean/scte35-threefive$ pypy3 mdsn.py 
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x3",
        "sap_details": "No Sap Type",
        "section_length": 101,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment_ticks": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x0",
        "tier": "0xfff",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 79,
        "crc": "0xf91207b1"
    },
    "command": {
        "command_length": 5,
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 4720.284578,
        "pts_time_ticks": 424825612
    },
    "descriptors": [
        {
            "tag": 112,
            "descriptor_length": 6,
            "name": "MDSN Descriptor",   # <---- Custom Descriptor parsed. 
            "identifier": "MDSN",
            "private_data": "C5"
        },
        {
            "tag": 2,
            "descriptor_length": 69,
            "name": "Segmentation Descriptor",
            "identifier": "CUEI",
            "components": [],
            "segmentation_event_id": "0xa4df",
            "segmentation_event_cancel_indicator": false,
            "program_segmentation_flag": true,
            "segmentation_duration_flag": true,
            "delivery_not_restricted_flag": false,
            "web_delivery_allowed_flag": false,
            "no_regional_blackout_flag": false,
            "archive_allowed_flag": false,
            "device_restrictions": "No Restrictions",
            "segmentation_duration": 30.0,
            "segmentation_duration_ticks": 2700000,
            "segmentation_message": "Provider Advertisement Start",
            "segmentation_upid_type": 15,
            "segmentation_upid_type_name": "URI",
            "segmentation_upid_length": 49,
            "segmentation_upid": "urn:uuid:Break-B0020855689_0012-07-10-X0112516124",
            "segmentation_type_id": 48,
            "segment_num": 0,
            "segments_expected": 0
        }
    ]
}

```


</details>

 Powered by threefive
---
<br>⚡ [`threefive/go` is now `cuei`](https://github.com/futzu/cuei) <br/>
<br>⚡ [myvideeotools.com](https://myvideotools.com/scte35parser) online SCTE-35 Cue parser. Powered by threefive. 
<br>⚡ [POIS Server](https://github.com/scunning1987/pois_reference_server) is Super Cool.
<br>⚡ [bpkio-cli](https://pypi.org/project/bpkio-cli/): A command line interface to the broadpeak.io APIs. 
<br>⚡ [x9k3](https://github.com/futzu/x9k3): SCTE-35 HLS Segmenter and Cue Inserter.
      <br>⚡ [amt-play ](https://github.com/vivoh-inc/amt-play) uses x9k3.
<br>⚡ [m3ufu](https://github.com/futzu/m3ufu): SCTE-35 m3u8 Parser.
<br>⚡ [six2scte35](https://github.com/futzu/six2scte35): ffmpeg changes SCTE-35 stream type to 0x06 bin data, six2scte35 changes it back.
<br>⚡ [SuperKabuki](https://github.com/futzu/SuperKabuki): SCTE-35 Packet Injection.
<br>⚡ [showcues](https://github.com/futzu/showcues) m3u8 SCTE-35 parser.
  
 threefive | more
---
<br>⚡ [Diagram](https://github.com/futzu/threefive/blob/master/cue.md) of a threefive SCTE-35 Cue.
<br>⚡ [ffmpeg and threefive](https://github.com/futzu/SCTE35-threefive/blob/master/threefive-ffmpeg.md) and SCTE35 and Stream Type 0x6 bin data.
<br>⚡ [Issues and Bugs and Feature Requests](https://github.com/futzu/scte35-threefive/issues) No forms man, just open an issue and tell me what you need. <br><i>(It needs to be  threefive related or a "What is the meaning of life and stuff?" type of question)</i>
























### data
> this might be wild baseless speculation.
