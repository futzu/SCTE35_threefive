### threefive Is The Most Advanced SCTE35 Parser lib Available, probably.

   * Supports All 2020 SCTE-35: 
      [`Commands`](https://github.com/futzu/threefive/blob/master/threefive/commands.py)
     [`Descriptors`](https://github.com/futzu/threefive/blob/master/threefive/descriptors.py)
     [`Upids`](https://github.com/futzu/threefive/blob/master/threefive/upid.py)
   * Parses [__Mpegts__](#stream-class)
   * Decrypts [__AES__ ](https://github.com/futzu/scte35-threefive/blob/901456089d369e8cd81c0dc3c2bd6600e303562e/threefive/segment.py#L37) 
  * [__ffmpeg__ and __SCTE35__ and __Stream Type 0x6__ bin data and __threefive__](https://github.com/futzu/SCTE35-threefive/blob/master/threefive-ffmpeg.md)

*  [Multicast?    __HLS?__   Custom Upid Handling?     __Frame Accurate__ Preroll timings?`... __Yes__.](https://github.com/futzu/SCTE35-threefive/tree/master/examples#threefive-examples)
* [__threefive /go__ this code is cleaner than your dishes.](https://github.com/futzu/scte35-threefive/tree/master/go)


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
     
* [Super Cool Examples](https://github.com/futzu/SCTE35-threefive/blob/master/examples/README.md)
   * New
     * [Display SCTE35 info via Webvtt Subtitles](https://github.com/futzu/threefive/blob/master/examples/stream/cue2vtt.py)
    * CLI
      * [Cli](https://github.com/futzu/SCTE35-threefive/blob/master/examples/cli.py)
    * DTMF
      * [DTMF Descriptor](https://github.com/futzu/SCTE35-threefive/blob/master/examples/dtmf)
    * Encode
      * [Edit Break Duration](https://github.com/futzu/scte35-threefive/blob/master/examples/encode/edit_break_duration.py)
      * [Encode Time Signal](https://github.com/futzu/scte35-threefive/blob/master/examples/encode/encode_time_signal.py)
      * [MPEGTS pass-through SCTE35 Cue Re-Encoding](https://github.com/futzu/scte35-threefive/blob/master/examples/encode/streamedit.py)
   * HLS
      * [Using threefive with HLS Manifests](https://github.com/futzu/SCTE35-threefive/tree/master/examples/hls)
      * [HASP Hls Aes Scte-35 Parser](https://github.com/futzu/threefive/blob/master/examples/hls/hasp.py)
  * Multicast
     * [Parsing SCTE-35 from a Multicast_Source](https://github.com/futzu/SCTE35-threefive/blob/master/examples/multicast/README.txt)
  * Splice Insert
    * [Splice Insert](https://github.com/futzu/SCTE35-threefive/blob/master/examples/spliceinsert/splice_insert.py)
    * [Splice Insert Too](https://github.com/futzu/SCTE35-threefive/blob/master/examples/spliceinsert/splice_insert_too.py)
  * Splice_Null
    * [Splice Null](https://github.com/futzu/SCTE35-threefive/blob/master/examples/splicenull)  
  * MpegTS Streams
     * [Display SCTE35 info via Webvtt Subtitles](https://github.com/futzu/threefive/blob/master/examples/stream/cue2vtt.py)
     * [Return a list of SCTE-35 Cues from an MPEGTS file](https://github.com/futzu/threefive/blob/master/examples/stream/cue_list.py)
     * [Cool SCTE35 Decoding from MPEGTS over HTTPS](https://github.com/futzu/threefive/blob/master/examples/stream/cool_decode_http.py)
     * [Decode SCTE3 from MPEGTS over HTTPS](https://github.com/futzu/threefive/blob/master/examples/stream/decode_http.py)
     * [Stream.decode_proxy() Example](https://github.com/futzu/SCTE35-threefive/blob/master/examples/stream/decode_proxy.py)
     * [Show preroll](https://github.com/futzu/threefive/blob/master/examples/stream/preroll.py)
  * Time Signal
    * [Time Signal Placement Opportunity End](https://github.com/futzu/threefive/blob/master/examples/timesignal/time_signal-placement_opportunity_end.py)
    * [Time Signal Program Overlap](https://github.com/futzu/threefive/blob/master/examples/timesignal/time_signal-program_overlap.py)
    * [Time Signal Program Start End](https://github.com/futzu/threefive/blob/master/examples/timesignal/time_signal_blackout_override_program_end.py)
  *  UPID
     * [Upids with Custom Output](https://github.com/futzu/threefive/blob/master/examples/upid/upid_custom_output.py)
     * [Multiple Segmentation Descriptors](https://github.com/futzu/threefive/blob/master/examples/upid/multi_upid.py)
     * [Combination Upid Segmentation Descriptor](https://github.com/futzu/threefive/blob/master/examples/upid/upid_combo.py)
     * [Custom Handling MPU Upid data](https://github.com/futzu/threefive/blob/master/examples/upid/custom_upid_handling.py)

* [Diagram](https://github.com/futzu/threefive/blob/master/cue.md)  of a threefive SCTE-35 Cue
* [`Issues` and `Bugs` and `Feature` Requests](#issues-and-bugs-and-feature-requests)
 *No forms man, just open an issue.*  
* [threefive Spotted `in The Wild`](https://gist.github.com/flavioribeiro/9b52c603c70cdb34c6910c1c5c4d240d)






### Requirements
* threefive requires [pypy3](https://pypy.org) or python 3.6+ 
    * (pypy3 runs threefive 4x Faster than python3)
* threefive 2.3.02+ requires crcmod for encoding and pyaes for decrypting.

 

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

> __threefive.decode__ is a SCTE-35 decoder function
> with input type __auto-detection__. 
```Base64```, ```Binary```, 
> ```Hex Strings```,```Hex literals```, ```Integers```, ```Mpegts files``` and ```Mpegts HTTP/HTTPS Streams```
> 

> __SCTE-35__ data can be __parsed__ 
> with just __one function call__.
    
> the arg __stuff__ is the input.
> if __stuff is not set__, 
> decode will attempt to __read__ from __sys.stdin.buffer__.

> if __stuff is a file__, the file data
> will be read and the type of the data
> will be autodetected and decoded.

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

##### Read from File [cue.txt](https://github.com/futzu/threefive/files/6986120/cue.txt)

```python3
from threefive import decode

decode('cue.txt')

```

```  A threefive SCTE-35 Cue```
```js
{
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x3",
        "sap_details": "No Sap Type",
        "section_length": 47,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x0",
        "tier": "0xfff",
        "splice_command_length": 4095,
        "splice_command_type": 5,
        "descriptor_loop_length": 10,
        "crc": "0x10fa4d9e"
    },
    "command": {
        "calculated_length": 20,
        "name": "Splice Insert",
        "time_specified_flag": true,
        "pts_time": 89742.161689,
        "break_auto_return": false,
        "break_duration": 242.0,
        "splice_event_id": 662,
        "splice_event_cancel_indicator": false,
        "out_of_network_indicator": true,
        "program_splice_flag": true,
        "duration_flag": true,
        "splice_immediate_flag": false,
        "unique_program_id": 1,
        "avail_num": 0,
        "avail_expected": 0
    },
    "descriptors": [
        {
            "tag": 0,
            "descriptor_length": 8,
            "name": "Avail Descriptor",
            "identifier": "CUEI",
            "provider_avail_id": 0
        }
    ],
    "packet_data": {
        "pid": "0x135",
        "program": 1,
        "pcr": 89730.281789,
        "pts": 89730.289522
    }
}
```
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
  * The threefive.__Stream__ class parses SCTE35 messages from a file or stream.
  * Supports
   * __file and http(s) URIs directly. 
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

Program:1030

   1031 [0x407] Type: 0x1b   PCR 
   1032 [0x408] Type: 0x3  
   1034 [0x40a] Type: 0x6  
   1035 [0x40b] Type: 0x86   SCTE35 

Program:1100

   1101 [0x44d] Type: 0x1b   PCR 
   1102 [0x44e] Type: 0x3  
   1104 [0x450] Type: 0x6  
   1105 [0x451] Type: 0x86   SCTE35 

Program:1080

   1081 [0x439] Type: 0x1b   PCR 
   1082 [0x43a] Type: 0x3  
   1084 [0x43c] Type: 0x6  


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


