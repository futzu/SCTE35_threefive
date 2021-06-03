___
### Test File
___
  * 3.7GB MPEGTS
  * 10 Programs
  * 30 Streams
  * 5 SCTE-35 Streams
  * 18 SCTE-35 Cues

```sh
a@fu:~/$  ls -alh plp0.ts 

-rwxr-xr-x 1 a a 3.7G Apr 21 13:58 plp0.ts
```
___
### Code:
* threefive version 2.2.90
```python3
a@fu:~/$ cat cli.py


import sys
from threefive import Stream, version

def do():
    args = sys.argv[1:]
    for arg in args:
        print(f'next file: {arg}')
        with open(arg,'rb') as vid:
            strm = Stream(vid)
            strm.decode_fu()

if __name__ == "__main__":
    do()
    print(version())

```
___
### Python3 
* version 3.9.2
```sh

a@fu:~/$ time python3 cli.py plp0.ts
```

#### real:   15.547s



___
### pypy3 
* version 7.3.3 

```sh

a@fu:~/$  time pypy3 cli.py plp0.ts

```
#### real	:   4.592s



