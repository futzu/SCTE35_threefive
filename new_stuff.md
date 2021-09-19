## ```New Cool Stuff```
When new features are added to threefive. I wait at least a release before I announce them.
```py3
a@fumatica:~/threefive$ pypy3
Python 3.7.10 (7.3.5+dfsg-2, Jun 03 2021, 20:39:46)
[PyPy 7.3.5 with GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>> from threefive import smoke, Stream, decode
```
___
####  ```threefive.Stream.strip_scte35()```

Folks have been asking for a way to strip out SCTE-35 Cues in realtime. 


```py3
>>>> help(Stream.strip_scte35)


Help on function strip_scte35 in module threefive.stream:

strip_scte35(self, func=show_cue_stder)

   Stream.strip_scte35 works just likle Stream.decode_proxy,
        MPEGTS packets, ( Except the SCTE-35 packets) ,
        are written to stdout after being parsed.
        SCTE-35 cues are printed to stderr
```

Example:

* make strip.py like this:

```py3
import sys
from threefive import Stream


def do():
    arg = sys.argv[1]
    with open(arg,'rb') as vid:
        Stream(vid).strip_scte35()

if __name__ == "__main__":
    do()
```
Use:
```sh
pypy3 strip.py ../mpegts/udp.livetv.ts | mplayer - 
```

```sh 
pypy3 strip.py ../mpegts/udp.livetv.ts > stripped.ts 
```
---

#### ``` threefive.smoke()```   
A quick sanity check for threefive
  
```py3
>>>> help(smoke)
Help on function smoke in module threefive.smoketest:

smoke(tests=None)
    calls threefive.decode using the values in tests.
    The format for tests:
    { "test_name" : value to pass to threefive.decode}
    
    example:
    
     my_tests ={
    "Base64": "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g=",
    "Bytes": b"\xfc0\x11\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00O%3\x96",
    }
    
    import threefive
    threefive.smoke_test(my_tests)

```
 threefive.smoke() runs ten tests that verify core functionality.

```py3
ten_tests = {
    "Base64": "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g=",
    "Bytes": b"\xfc0\x11\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00O%3\x96",
    "Hex String": "0XFC301100000000000000FFFFFF0000004F253396",
    "Hex Literal": 0xFC301100000000000000FFFFFF0000004F253396,
    "Integer": 1439737590925997869941740173214217318917816529814,
    "HTTP/HTTPS Streams": "https://futzu.com/xaa.ts",
    
    # "Bad" tests are expected to fail.
    
    "Bad Base64 ": "/DAvAf45AA",
    "Bad File": "/you/me/fake.file",
    "Bad Integer": -0.345,
    " Bad String": "your momma",
}
```
threefive.smoke() takes about 10 seconds to run.
```py3
>>>> from threefive import smoke
>>>> smoke()

```

this is what you want as the output,
* six  __✔__
* four __✘__

```py3


Smoke Test

Base64  ✔
Bytes  ✔
Hex String  ✔
Hex Literal  ✔
Integer  ✔
HTTP/HTTPS Streams  ✔
Bad Base64   ✘
Bad File  ✘
Bad Integer  ✘
 Bad String  ✘
```
