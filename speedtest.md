#  `threefive + Python3` VS. `threefive + pypy3` VS. `tsduck in C++` VS. `cuei in Go.` 

* The video: 4.9GB MPEGTS. 

```rebol
a@slow:~/cuei$ ls -alh ../v2.ts
-rw-r--r-- 1 a a 4.9G Mar  8 04:03 ../v2.ts
```
* I used SuperKabuki to insert 14,862 SCTE-35 Time Signals
---  
### Test 1: `threefive` with `Python 3.11.2`

* __0.5697674__ GB / second

```smalltalk
a@slow:~/cuei$ time threefive  ../v2.ts 2>&1 | grep sap_type | wc -l
14862

real    0m8.600s
user    0m8.026s
sys     0m0.778s

```
---

### Test 2: `threefive` with `PyPy 7.3.11`

* __1.3830087__ GB / second

``` smalltalk
a@slow:~/cuei$ time threefivepypy3  ../v2.ts 2>&1 | grep sap_type | wc -l
14862

real    0m3.543s
user    0m2.880s
sys     0m0.846s
```

---
### Test 3: `tsduck 3.36-3528` written in `C++`

* __3.4146341__ GB / second
```smalltalk
a@slow:~/cuei$ time  tsp -I file ../v2.ts -P splicemonitor -a -O drop | grep "Command type:" | wc -l
14862

real    0m1.435s
user    0m2.006s
sys     0m0.861s
```
---


### Test 4: `cuei v1.1.93 "Junior"` written in `Go`

* __4.6755725__ GB / second

```smalltalk
a@slow:~/cuei$ time ./cuei ../v2.ts | grep SapType | wc -l
14862

real    0m1.048s
user    0m0.605s
sys     0m0.509s


```
---



# Winner: `cuei v1.1.93 "Junior"`


