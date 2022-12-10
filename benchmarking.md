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
```lua
a@debian:~/build/scte35-threefive$ time python3 test.py /home/a/mpegts/plp0.ts

real	0m14.293s
user	0m12.666s
sys	    0m1.406s

```
### PyPy 7.3.9

```lua
a@debian:~/build/scte35-threefive$ time pypy3 test.py /home/a/mpegts/plp0.ts

real	0m2.879s         <--  Boom goes the dynamite.
user	0m2.576s
sys	0m1.101s
```
