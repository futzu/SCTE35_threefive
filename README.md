# threefive
## SCTE35 Decoder
* [ Latest Pip Version]( https://pypi.org/project/threefive/)
---
* [Supported Splice Commands](#splice-commands)
* [Supported Splice Descriptors](#splice-descriptors)

* [__Fast Start Directions__](#fast-start-directions)
* [Dependencies](#dependencies)
* [__Install__](#install)

* [__Examples__](https://github.com/futzu/SCTE35-threefive/tree/master/examples)
    * [Using threefive with HLS Manifests](https://github.com/futzu/SCTE35-threefive/tree/master/examples/hls)
    * [Splice Insert](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Splice_Insert.py)
    * [Splice Insert Too](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Splice_Insert_Too.py)
    * [Splice Null](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Splice_Null.py)
    * [Time Signal Blackout Override Program End](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Time_Signal_Blackout_Override_Program_End.py)
    * [Time Signal Placement Opportunity Start](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Time_Signal-Placement_Opportunity_Start.py)
    * [Time Signal Placement Opportunity End](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Time_Signal-Placement_Opportunity_End.py)
    * [Time Signal Program Overlap ](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Time_Signal-Program_Overlap.py)
    * [Time Signal Program Start End](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Time_Signal-Program_Start_End.py)
    * [Parsing SCTE-35 from a Multicast Source](https://github.com/futzu/SCTE35-threefive/blob/master/examples/multicast/ts_scte_parser.py)
   * [StreamProxy Example](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Proxy_Demo.py)
   * [Upids with Custom Output](https://github.com/futzu/SCTE35-threefive/blob/master/examples/Upid_Custom_Output.py)

* [__Easy threefive__](#easy-threefive)
  *   [The __decode__ Function](#the-decode-function)
      * [Parsing SCTE 35 messages from Mpeg Transport Streams and Binary files](#mpegts)
      * [Parsing SCTE 35 messages encoded in Base64, Binary, or Hex](#base64-encoded-strings)
* [__Advanced threefive__](#advanced-threefive)
  *   [__Splice Class__](#splice-class)
      * [JSON Pretty Print SCTE 35 Message](#json-pretty-print-scte-35-message)
      * [Return SCTE 35 Message](#return-scte-35-message)
      * [JSON Pretty Print Splice Info Section](#json-pretty-print-splice-info-section)
      * [Return Splice Info Section](#return-splice-info-section)
      * [JSON Pretty Print Splice Command](#json-pretty-print-splice-command)
      * [Return Splice Command](#return-splice-command)
      * [JSON Pretty Print Splice Descriptors](#json-pretty-print-splice-descriptors)
      * [Return Splice Descriptors](#return-splice-descriptors)  
  *   [__Stream Class__](#stream-class)
      * [__Stream.decode()__](#Streamdecode)                                                                
         * [Parse a Local File with a Stream Instance](#parse-a-local-file-with-a-stream-instance)
         * [Pipe a Video to Stream](#pipe-a-video-to-stream)
      * [__Stream.decode_until_found()__](#Streamdecode_until_found)
         * [Custom Output](#customized-scte-35-message-handling)
         
  *  [__StreamPlus Class__](#streamplus-class)
      * [__StreamPlus.decode()__](#streamplusdecode)
      * [__StreamPus.decode_until_found()__](#Streamplusdecode_until_found)
      
  * [__StreamProxy Class__](#streamproxy-class)
      * [__StreamProxy.decode()__](#StreamProxydecode)
---  
##  ```Splice Commands``` 
  *  source [command.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/command.py)
  *  Splice Null  
  *  Splice Schedule
  *  Splice Insert 
  *  Time Signal 
  *  Bandwidth Reservation
##  ```Splice Descriptors```  
  *  source [descriptor.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/descriptor.py)
  *  DTMF Descriptor 
  *  Segmentation Descriptor (all segmentation Upids) 
  *  Segmentation Types and Messages 
  *  Time Descriptor 
  *  Audio Descriptor
  
  ---
  
  [🡡 top](#threefive)


## ```Fast Start Directions```

*  [__Up and Running in Less Than Seven Seconds__](https://github.com/futzu/SCTE35-threefive/blob/master/FastStart.md) 


##  ```Dependencies``` 
*  Python 3
*  [__bitn__](https://github.com/futzu/bitn)

##  ```Install``` 
#####  git  
```sh
git clone https://github.com/futzu/SCTE35-threefive.git

cd SCTE-threefive

# you need root to install for the system
make install
```
---
```
...
Processing threefive-2.1.39-py3.8.egg
Copying threefive-2.1.39-py3.8.egg to /usr/local/lib/python3.8/dist-packages
Adding threefive 2.1.39 to easy-install.pth file

Installed /usr/local/lib/python3.8/dist-packages/threefive-2.1.39-py3.8.egg
Processing dependencies for threefive==2.1.39
Searching for bitn==0.0.27
Best match: bitn 0.0.27
Processing bitn-0.0.27-py3.8.egg
bitn 0.0.27 is already the active version in easy-install.pth

Using /usr/local/lib/python3.8/dist-packages/bitn-0.0.27-py3.8.egg
Finished processing dependencies for threefive==2.1.39

```

##### pip3
```sh
pip3 install threefive
```
---

```
Collecting threefive
  Downloading threefive-2.0.99-py3-none-any.whl (12 kB)
Collecting bitn>=0.0.27
  Downloading bitn-0.0.27-py3-none-any.whl (3.0 kB)
Installing collected packages: bitn, threefive
Successfully installed bitn-0.0.27 threefive-2.0.99

```
 
  
[🡡 top](#threefive)


##  ```Easy threefive```  

###   ```The decode Function``` 
 *   source [decode.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/decode.py)
 * __threefive.decode__ is an all purpose function to decode SCTE 35 messages from a file or string.

 ```python
import threefive
```
####    ```MpegTS```
```python
threefive.decode('/path/to/mpegwithscte35.ts') 
```
####    ```Binary```
```python
threefive.decode('/mnt/build/file.bin')
```
####  ```Base64 Encoded Strings```
```python
mesg='/DBUAAAAAAAA///wBQb+AAAAAAA+AjxDVUVJAAAACn+/Dy11cm46dXVpZDphYTg1YmJiNi01YzQzLTRiNmEtYmViYi1lZTNiMTNlYjc5OTkRAAB2c6LA'
threefive.decode(mesg)
```
#### ```Hex Encoded Strings```
```python
hexed='0xFC302F000000000000FFFFF014054800008F7FEFFE7369C02EFE0052CCF500000000000A0008435545490000013562DBA30A'
threefive.decode(hexed)
```

 [🡡 top](#threefive)
 

## ```Advanced threefive```

###  ```Splice Class```  
   *  source [splice.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/splice.py)

   *  The __threefive.Splice__ class decodes a SCTE35 binary, base64, or hex encoded string. 
   *  __threefive.Splice__ provides several methods to access the parsed data.

```python

from threefive import Splice

b64 = "/DBIAAAAAAAA///wBQb+ek2ItgAyAhdDVUVJSAAAGH+fCAgAAAAALMvDRBEAAAIXQ1VFSUgAABl/nwgIAAAAACyk26AQAACZcuND"

scte35 = Splice(b64)

````
#### ```JSON Pretty Print SCTE 35 Message```
```python
scte35.show()
```
#### ```Return SCTE 35 Message```
```python
scte35.get()
```
#### ```JSON Pretty Print Splice Info Section```
```python
scte35.show_info_section()
```
#### ```Return Splice Info Section```
```python
scte35.get_info_section()
```        
#### ```JSON Pretty Print Splice Command```
```python
scte35.show_command()
```
#### ```Return Splice Command```
```python
scte35.get_command()
``` 
#### ```JSON Pretty Print Splice Descriptors```
```python
scte35.show_descriptors()
```    
#### ```Return Splice Descriptors```
```python
scte35.get_descriptors()
```

 [🡡 top](#threefive)

---
###  ```Stream Class``` 
  * source [stream.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/stream.py)

  * The __threefive.Stream__ class parses SCTE35 messages from a file or stream.
  
```python3
  threefive.Stream(tsdata, show_null = False)
  ```
   * __tsdata__ is an open file handle or sys.stdin.buffer to read 'piped' in data.
   * __show_null__ if set to True, enables showing SCTE 35 null commands.

#### ```Stream.decode()```
* Calls Splice.show() when a SCTE-35 message is found

 ##### ```Parse a Local File with a Stream Instance```
 
 ```python3
 
 import sys
 from threefive import Stream
 '''
 
 if __name__ =='__main__':
    with open(sys.argv[1],'rb') as tsdata:
        Stream(tsdata).decode()

```

##### ```Pipe a Video to Stream```

```sh

curl -s https://futzu.com/xaa.ts -o -  \
  | python3 -c 'import sys;import threefive; threefive.Stream(sys.stdin.buffer).decode()' 
```
---

####  ```Stream.decode_until_found()```
* Use the Stream.decode_until_found method instead of Stream.decode().
* Returns Splice instances when SCTE-35 packets are found.
* Allows for customized SCTE-35 message handling.
##### Customized SCTE-35 Message Handling
```python
import sys
from threefive import Stream

def do():

   with open(sys.argv[1],'rb') as tsdata:
         while True:
            cue = Stream(tsdata).decode_until_found() 
            if not cue :
                sys.exit()
            else:
            # Customized output
               print('pid :',cue.header.pid, 'command:',
                     cue.command.name,'@',cue.command.pts_time,
                     'Out of Network:',
                     cue.command.out_of_network_indicator)


if __name__ == '__main__':
    do()

```
   *   Output:
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
 [🡡 top](#threefive)

---
###  ```StreamPlus Class``` 
  * source [streamplus.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/streamplus.py)
  * __threefive.StreamPlus__ is a sub class of  __threefive.Stream__

```python3
  threefive.StreamPlus(tsdata, show_null = False)
```
   * __tsdata__ is an open file handle or sys.stdin.buffer to read 'piped' in data.
   * __show_null__ if set to True, enables showing SCTE 35 null commands.
    
   * __threefive.StreamPlus__ adds PTS timestamp for each SCTE 35 packet.

#### ```StreamPlus.decode()```
   * See [__Stream.decode__()](#Streamdecode)

#### ```StreamPlus.decode_until_found()```
   * See [__Stream.decode_until_found()__](#Streamdecode_until_found)

---

[🡡 top](#threefive)

### ```StreamProxy Class```
  * source [streamproxy.py](https://github.com/futzu/SCTE35-threefive/blob/master/threefive/streamproxy.py)
  * __threefive.StreamProxy__ is a sub class of  __threefive.StreamPlus__

```python3
  threefive.StreamProxy(tsdata, show_null = False)
```
 * Writes scte35 data to sys.stderr
 * Writes all packets to sys.stdout
 * Parse the scte35 and pipe the MPEG-TS stream.

#### ```StreamProxy.decode()```
```python3

   import threefive
   
   # Name this proxy.py
   
   with open('vid.ts','rb') as tsdata:
      threefive.StreamProxy(tsdata).decode()
```
* Pipe to mplayer
```
python3 proxy.py | mplayer -
```
[🡡 top](#threefive)
