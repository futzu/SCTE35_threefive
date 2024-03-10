# Speed Test `threefive + Python3` VS. `threefive + pypy3` VS. `cuei in Go.` 

* The video: 4.9GB MPEGTS. 

```rebol
a@slow:~/cuei$ ls -alh ../vt.ts
-rw-r--r-- 1 a a 4.9G Mar  8 04:03 ../vt.ts
```
* I used SuperKabuki to insert 14,862 SCTE-35 Time Signals
---  
### Test 1: `threefive` with `Python 3.11.2`

* __0.5697674__ GB / second

```smalltalk
a@slow:~/cuei$ time threefive  ../vt.ts 2>&1 | grep sap_type | wc -l
14862

real    0m8.600s
user    0m8.026s
sys     0m0.778s

```
---

### Test 2: `threefive` with `PyPy 7.3.11`

* __1.3830087__ GB / second

``` smalltalk
a@slow:~/cuei$ time threefivepypy3  ../vt.ts 2>&1 | grep sap_type | wc -l
14862

real    0m3.543s
user    0m2.880s
sys     0m0.846s
```

---

### Test 3: `cuei` written in `Go`

* __3.5430001__ GB / second

```smalltalk
a@slow:~/cuei$ time ./cuei ../v2.ts | grep SapType | wc -l
14862

real    0m1.084s
user    0m0.681s
sys     0m0.551s

```
---


