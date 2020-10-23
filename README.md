
# :rocket: threefive
## SCTE35 Decoder
  * All __2019__ SCTE-35 __Splice Commands__ and __Splice Descriptors__ are Fully Supported.
---
#### [__Heads Up!__ Changes as of 10/23/2020](#changes)
* [ __threefive__ works best with __pypy3__](https://www.pypy.org/)
* [__Requires Python 3.6+__](https://www.python.org/downloads/release/python-390/)
* [ Latest __Pip__ Version]( https://pypi.org/project/threefive/)
*  [__Fast__ Start](#fast-start-directions)
      * [__Dependencies__](#dependencies)
      * [__Install__](#install)
      * [__Examples__](https://github.com/futzu/SCTE35-threefive/tree/master/examples)
* [Easy __threefive__](#easy-threefive)
  *   [The __decode__ Function](#the-decode-function)
      * [Parsing __SCTE 35__ messages from __Mpeg-TS Streams__](#mpegts)
      * [Parsing __SCTE 35__ messages encoded in __Base64, Binary, or Hex__](#base64-encoded-strings)
*  [Advanced __threefive__](#advanced-threefive)
     *  [__Cue__ Class](#cue-class)
          * [Return __Cue__ instance as __dict__](#return-cue-as-dict)   
          * [Return __Cue__ instance as __JSON__](#return-cue-as-json)   
          * [Print __Cue__ instance as __JSON__](#print-cue-as-json)   
     * [__Stream__ Class](#stream-class)
          * [__Stream.decode__(func=show_cue)](#streamdecodefuncshow_cue)                                                                
               * [__Parse__ a Local File with a __Stream__ Instance](#parse-a-local-file-with-a-stream-instance)
               * [__Pipe__ a Video to a Stream __Instance__](#pipe-a-video-to-stream-instance)
          * [Stream.__decode_next__()](#streamdecode_next)
          * [Stream.__decode_pid__(the_pid,func=show_cue)](#streamdecode_pidthe_pid-func--show_cue)
          * [Stream.__decode_proxy__(func=show_cue)](#Streamdecodeproxyfuncnone)    
 *   [__Examples__](https://github.com/futzu/SCTE35-threefive/tree/master/examples)
     * __HLS__
          * [Using threefive with __HLS Manifests__](https://github.com/futzu/SCTE35-threefive/tree/master/examples/hls)
     * __Multicast__
          * [Parsing SCTE-35 from a __Multicast__ Source](https://github.com/futzu/SCTE35-threefive/blob/master/examples/multicast/ts_scte_parser.py)
     * __Splice Insert__
          * [Splice __Insert__](https://github.com/futzu/SCTE35-threefive/blob/master/examples/spliceinsert/Splice_Insert.py)
          * [__Splice Insert__ Too](https://github.com/futzu/SCTE35-threefive/blob/master/examples/spliceinsert/Splice_Insert_Too.py)
     * __Splice_Null__
          * [Splice __Null__](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Splice_Null.py)
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
     * [__Stream.decode_proxy()__ Example](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Proxy_Demo.py)
---

#### __Changes__
   *  As of version __2.1.95__, __threefive.version__ returns a string for the current __version__. 
   ```python
   
     >>> import threefive
     >>> threefive.version
    '2.1.95'
``` 

   *  Stream.decode, Stream.decode_pid, and Stream.decode_proxy now all take an optional function as an arg. See [__Stream__](#stream-class)
   *  Stream.decode_until_found() is now [__Stream.decode_next()__](#streamdecode_next)
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

 ```python
import threefive
```
 *  __MpegTS__
```python
threefive.decode('/path/to/mpegwithscte35.ts') 
```
 *  __Binary__
```python
threefive.decode('/mnt/build/file.bin')
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
```
##### Return cue __as dict__
```python
cue.get()

# Splice Info Section
cue.get_info_section()

# Splice Command
cue.get_command()

# Splice Descriptors
cue.get_descriptors()
````
##### Return cue as JSON
```python
jason = cue.get_json()
```
###### Print cue as JSON 
```python
cue.show()
```    

 [🡡 top](#threefive)


##  __Stream__ Class
  * source [stream.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/stream.py)

  * The threefive.__Stream__ class parses SCTE35 messages from a file or stream.
  * __init__
       *  __tsdata__ is an open file handle or __sys.stdin.buffer__ to read 'piped' in data.
   
       *  __show_null__ if set to __True__, enables showing SCTE 35 __null commands__.
   
 ```python3
  threefive.Stream(tsdata, show_null = False)
  ```

   * __Methods__
   
   
Method                              | Description
------------------------------------| -------------------------------------
Stream.__decode__(*func = show_cue*)             | __Prints__ SCTE-35 __cues__ for SCTE-35 packets. Accepts an optional function, func, as arg. 
Stream.__decode_next()__                       | __Returns__ a __Cue__ instance for a SCTE-35 packet.
Stream.__decode_pid__(*the_pid,func = show_cue*) |Same as Stream.__decode__ except only packets where pid == __the_pid__
Stream.__decode_proxy__(*func = show_cue*)       |Same as Stream.__decode__ except raw packets are written to stdout for piping to another program.


### ```Stream.decode(func=show_cue)```

##### Parse a Local File with a Stream Instance
 
 ```python3
 
 import sys
 from threefive import Stream
 '''
 
 if __name__ =='__main__':
    with open(sys.argv[1],'rb') as tsdata:
        sp = Stream(tsdata)
        sp.decode()

```

##### Pipe a Video to Stream

```sh

curl -s https://futzu.com/xaa.ts -o -  \
  | python3 -c 'import sys;import threefive; threefive.Stream(sys.stdin.buffer).decode()' 
```

#####  Pass in custom function 

   *  __func__ should match the interface
```
    func(cue)
```
   * __example__
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

* Returns a threefive.Cue instance when a SCTE-35 packet is found.
```python3
import sys
from threefive import Stream

def display(cue):
   print(f'\033[92m{cue.command.name}\033[00m')
   print(f'{cue.packet_data}')

def do():
   with open(sys.argv[1],'rb') as tsdata:
      sp = Stream(tsdata)
      while tsdata:
         cue = sp.decode_next()
         if not cue :
            sys.exit()
         display(cue)

if __name__ == '__main__':
   do()

```
* [Stream.__decode_next()__ multicast __example__](https://github.com/futzu/SCTE35-threefive/blob/master/examples/multicast/ts_scte_parser.py)


### ```Stream.decode_pid(the_pid, func = show_cue)```

* Use Stream.__decode_pid()__ instead of Stream.__decode()__ 
to decode SCTE-35 from packets where pid == __the_pid__

```python3
import threefive

with open('../35.ts','rb') as tsdata:
    threefive.Stream(tsdata).decode_pid(1035)
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
