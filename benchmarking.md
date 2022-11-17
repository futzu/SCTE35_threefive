### the video
```sh
a@debian:~/build/scte35-threefive$ ls -alh ~/mpegts/plp0.ts
-rw-r--r-- 1 a a 3.7G May 21  2020 /home/a/mpegts/plp0.ts
```

### the code
```python3
import sys
import threefive

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            strm = threefive.Stream(arg)
            strm.decode()
```
### python 3.10
```
a@debian:~/build/scte35-threefive$ time python3 test.py /home/a/mpegts/plp0.ts

real	0m22.824s
user	0m22.424s
sys	  0m1.713s
```
### PyPy 7.3.9

```
a@debian:~/build/scte35-threefive$ time pypy3 test.py /home/a/mpegts/plp0.ts

real	0m2.879s          Boom.
user	0m2.576s
sys	  0m1.101s
```
### [cuei](https://github.com/cuei) (golang)


```
a@debian:~/build/scte35-threefive$ time ~/cueified ~/mpegts/plp0.ts

real	0m1.037s         Boom << Boom
user	0m0.649s
sys	0m0.386s
```


#### the code
```go
package main

import (
	"os"
	"fmt"
	"github.com/futzu/cuei"
)

func main(){

	args := os.Args[1:]
	for i := range args{
		fmt.Printf( "\nNext File: %s\n\n",args[i] )
		var stream   cuei.Stream
		stream.Decode(args[i])
	}
} 

```
