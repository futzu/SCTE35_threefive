# threefive
## SCTE35 Decoder
  * All __2019__ SCTE-35 __Splice Commands__ and __Splice Descriptors__ are Fully Supported.
---
## [__Heads Up!__ Changes as of 9/24/2020](#changes)

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
          * [Print SCTE-35 as JSON](#print-scte-35-as-json)
          * [Return SCTE-35 as dict](#return-scte-35-as-dict)
       
     * [__Stream__ Class](#stream-class)
          * [__Stream.decode()__](#Streamdecode)                                                                
               * [__Parse__ a Local File with a __Stream__ Instance](#parse-a-local-file-with-a-stream-instance)
               * [__Pipe__ a Video to a Stream __Instance__](#pipe-a-video-to-stream)
          * [Stream__.decode_until_found()__](#Streamdecode_until_found)
          * [Stream__.proxy(func=None)__](#Streamproxyfuncnone)
         
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
          * [__Upids__ with Custom Output](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Upid_Custom_Output.py)
          * [__Multiple__ Segmentation __Descriptors__](https://github.com/futzu/SCTE35-threefive/blob/master/examples/upid/Multi_Upid.py)
          * [Combination __Upid__ Segmentation Descriptor](https://github.com/futzu/SCTE35-threefive/blob/master/examples/upid/Upid_Combo.py)
          
     * [__Stream.proxy__ Example](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Proxy_Demo.py)

---

## __Changes__
   *  Splice class has been renamed Cue. See [Cue](#cue-class)
   *  Stream, StreamPlus, and StreamProxy classes have been consolidated. See [Stream](#stream-class)

---

## Fast __Start__

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

*  __pip3__

```sh
pip3 install threefive

```

   *    __pip3 and pypy3__

```
# If you don't have pip installed, try this.

pypy3 -mensurepip install pip 


pypy3 -mpip install threefive
```
---
 

[🡡 top](#threefive)


---

# __Easy__ threefive

##   The __decode__ Function
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
---
##  __Cue__ Class
   *  source [cue.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/cue.py)
   *  The __threefive.Cue__ class decodes a SCTE35 binary, base64, or hex encoded string. 
   *  __threefive.Cue__ provides several methods to access the parsed data.

```python

from threefive import Cue

b64 = "/DBIAAAAAAAA///wBQb+ek2ItgAyAhdDVUVJSAAAGH+fCAgAAAAALMvDRBEAAAIXQ1VFSUgAABl/nwgIAAAAACyk26AQAACZcuND"

scte35 = Cue(B64)
```
#### __Print__ SCTE-35 as JSON 

```python

scte35.show()

# Splice Info Section
scte35.show_info_section()

# Splice Command
scte35.show_command()

# Splice Descriptors
scte35.show_descriptors()
```    

#### Return SCTE 35 __as dict__

```python

scte35.get()

# Splice Info Section
scte35.get_info_section()

# Splice Command
scte35.get_command()

# Splice Descriptors
scte35.get_descriptors()

````

 [🡡 top](#threefive)

---
##  __Stream__ Class 
  * source [stream.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/stream.py)

  * The __threefive.Stream__ class parses SCTE35 messages from a file or stream.
  
```python3
  threefive.Stream(tsdata, show_null = False)
  ```
   * __tsdata__ is an open file handle or sys.stdin.buffer to read 'piped' in data.
   * __show_null__ if set to True, enables showing SCTE 35 null commands.

### Stream.decode()
* Calls __Cue.show()__ when a SCTE-35 message is found

 #### ```Parse a Local File with a Stream Instance```
 
 ```python3
 
 import sys
 from threefive import Stream
 '''
 
 if __name__ =='__main__':
    with open(sys.argv[1],'rb') as tsdata:
        Stream(tsdata).decode()

```

#### ```Pipe a Video to Stream```

```sh

curl -s https://futzu.com/xaa.ts -o -  \
  | python3 -c 'import sys;import threefive; threefive.Stream(sys.stdin.buffer).decode()' 
```
---

###  Stream.decode_until_found()
* Use the __Stream.decode_until_found__() method instead of __Stream.decode()__.
* Returns __Cue__ instances when SCTE-35 packets are found.
* Allows for customized SCTE-35 message handling.

```python
import sys
from threefive import Stream

def do():
   with open(sys.argv[1],'rb') as tsdata:
         while True:
            cuep = Stream(tsdata).decode_until_found() 
            if not cuep :
                sys.exit()
            else:
            # Customized output
               print('pid :',cuep.header.pid, 'command:',
                     cuep.command.name,'@',cuep.command.pts_time,
                     'Out of Network:',
                     cuep.command.out_of_network_indicator)

if __name__ == '__main__':
    do()

```
   *   __Output__
```python
pid : 1055 command: Splice Insert @ 21951.133267 Out of Network: True
pid : 1015 command: Splice Insert @ 22516.907656 Out of Network: True
pid : 1055 command: Splice Insert @ 22026.133267 Out of Network: False
pid : 1045 command: Splice Insert @ 22864.350067 Out of Network: True
pid : 1015 command: Splice Insert @ 22696.907656 Out of Network: False
pid : 1045 command: Splice Insert @ 22960.350067 Out of Network: False
pid : 1015 command: Splice Insert @ 23516.827656 Out of Network: True
pid : 1015 command: Splice Insert @ 23696.827656 Out of Network: False
```
---

### Stream.proxy(func = None)
*  Writes all packets to sys.stdout.
*  Writes scte35 data to sys.stderr.
*  The optional func arg allows a function
   to be used for custom handling of the SCTE-35
   cue instance.
*  If func is not set, threefive.Cue.show() is called.


```python3

   import threefive
   
   # Name this proxy.py
   
   with open('vid.ts','rb') as tsdata:
      sp = threefive.Stream(tsdata)
      sp.proxy()
```

*  the function should match the interface
```
    func(cuep)
```
* cuep is an instance of __threefive.Cue__

```python3
import sys
import threefive
import json

def display(cuep):
   print(f'\033[92m{json.dumps(vars(cuep.header))}\033[00m', file=sys.stderr,end='\r')
   print(f'\033[92m{json.dumps(cuep.get_command(),indent=2)}\033[00m', file=sys.stderr)

def do():

   with open(sys.argv[1],'rb') as tsdata:
            sp = threefive.Stream(tsdata)
            cue = sp.proxy(func = display) 
            if not cue :
                sys.exit()

if __name__ == '__main__':
    do()

```

* Pipe to mplayer
```
python3 proxy.py | mplayer -
```

[🡡 top](#threefive)
