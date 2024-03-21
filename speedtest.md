#  `threefive + Python3` VS. `threefive + pypy3` VS. `tsduck in C++` VS. `cuei in Go.` 

> Q. Why only use __threefive, tsduck and cuei__? What about other SCTE-35 parsers? 

> A. To be honest, they are very few other parsers that will parse SCTE-35 from MPEGTS, here are three that were excluded and why.
> 

1. __lib BitStream from the VLC folks__. Fast parser, but incomplete SCTE-35 Data last time I used it, and it requires writing about 500 lines of code to parse SCTE-35.
2. __gstreamer__ I believe it will parse SCTE-35, but I spent a few hours trying to figure out how to do it and I have no idea how to even run gstreamer, much less parse SCTE-35 with it.
3. __Comcast GOTS__ has about 13,000 lines of code, and requires you write about 300 more to parse SCTE-35, and I'm not exactly sure how to use it.

# The Contestants

1. the __threefive cli__ tool running on __python3__.
2. the __threeefive cli__ tool running on pypy3.
3. the __tsduck cli__ using the __SpliceMonitor__ plugin.
4. the __cuei library__ and __ten lines of code__ to make a cli tool.


# The File
```rebol
a@slow:~/cuei$ ls -alh ../v2.ts
-rw-r--r-- 1 a a 4.9G Mar  8 04:03 ../v2.ts
```
* I used [SuperKabuki](https://github.com/futzu/superkabuki) to insert 14,862 SCTE-35 Time Signals
---  
### Test 1: `threefive` with `Python 3.11.2`

```smalltalk
a@slow:~/cuei$ time threefive  ../v2.ts 2>&1 | grep sap_type | wc -l
14862

real    0m8.600s
user    0m8.026s
sys     0m0.778s

```

* We grep 'sap_type' because it appears in every SCTE-35 Cue, and only once, so we can count the nunmber of cues detected.

---

### Test 2: `threefive` with `PyPy 7.3.11`

``` smalltalk
a@slow:~/cuei$ time threefivepypy3  ../v2.ts 2>&1 | grep sap_type | wc -l
14862

real    0m3.543s
user    0m2.880s
sys     0m0.846s
```
* We grep 'sap_type' because it appears in every SCTE-35 Cue, and only once, so we can count the nunmber of cues detected. 


---
### Test 3: `tsduck 3.36-3528` written in `C++`

```smalltalk
a@slow:~/cuei$ time  tsp -I file ../v2.ts -P splicemonitor -a -O drop | grep "Command type:" | wc -l
14862

real    0m1.435s
user    0m2.006s
sys     0m0.861s
```
---
* We grep 'Command type' because it appears in every SCTE-35 Cue, and only once, so we can count the nunmber of cues detected. 


### Test 4: [`cuei v1.1.93 "Junior"`](https://github.com/futzu/cuei) written in `Go`

```smalltalk
a@slow:~/cuei$ time ./cuei ../v2.ts | grep SapType | wc -l
14862

real    0m1.048s
user    0m0.605s
sys     0m0.509s


```
* The code used for the test.
```go
package main                          // 1

import (                              // 2
        "os"                          // 3    
        "github.com/futzu/cuei"       // 4
)                                     // 5

func main(){                          // 6
        arg := os.Args[1]             // 7
        stream := cuei.NewStream()    // 8
        stream.Decode(arg)            // 9
}                                     // 10  lines
```
* We grep 'SapType' because it appears in every SCTE-35 Cue, and only once, so we can count the nunmber of cues detected. 

---

# Results:

| tool                | Cues Detected| GB/second     |
|---------------------|--------------|---------------|
| threefive w/ python3| 14862        |    0.5697674  |
| threefive w/ pypy3  | 14862        |    1.3830087  |
| tsduck              | 14862        |    3.4146341  |
| cuei                | 14862        |  __4.6755725__|



# Winner:  [`cuei v1.1.93 "Junior"`](https://github.com/futzu/cuei)

