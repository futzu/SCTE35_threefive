> threefive Performance
## Python3 vs. Pypy3 vs. threefive/go
>
>I've found pypy3 to be 100% compatible with threefive. Everything works.
>
>pypy3 is much faster than python3 at bitwise operations and just about everything else.
>
> pypy3 parses mpegts at (__1GB/second__).
>
>threefive/go is even faster.
> parsing mpegts at (__3GB/second__).
>
>
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
* threefive version 2.3.0
```python3
a@fu:~/$ cat cli.py

import sys 
from threefive import Stream, version 
 
 
def do(): 
    print(version()) 
    args = sys.argv[1:] 
    for arg in args: 
        print(f'next file: {arg}') 
        with open(arg,'rb') as vid: 
            Stream(vid).decode_fu() 
 
 
if __name__ == "__main__": 
    do()
 
```
___
### Python3 
* version 3.9.2
```sh

a@fu:~/$ time python3 cli.py plp0.ts
```

#### real:   14.367s

___
### pypy3 
* version 7.3.3 

```sh

a@fu:~/$  time pypy3 cli.py plp0.ts

```
### real	:   2.89s

___
### threefive/go

```go
cat cli.go


package main

import (
	"fmt"
	"github.com/futzu/threefive/go"
	"os"
)

func main() {
 args := os.Args[1:]
	 for i := range args {
		  fmt.Printf("\nNext File: %s\n\n", args[i])
		  var stream threefive.Stream
		  stream.Decode(args[i])
	 }
}

```
* version 1.15.9 linux/amd64
```sh

a@fu:~/$ go build cli.go

a@fu:~/$  time ./cli plp0.ts

```
### real:  1.03s

