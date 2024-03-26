
## Simple SCTE-35 Ad Breaks in just Two Steps.

### `Pre-flight`

* Install [__adbreak2__](https://github.com/futzu/adbreak2) and [__superkabuki__](https://github.com/futzu/superkabuki)
```js
 python3 -mpip install adbreak2 superkabuki
```
---

## `Two Step SCTE-35 Encoding`

### `Step 1.` Use adbreak2 to populate a sidecar file

* Add an ad break at `PTS` __37.422__ with a  __30__ second `Duration`  and write it to the `Sidecar` file __mysidecar.txt__
```js
a@slow:~$ adbreak2 --pts 37.422 --duration 60 --sidecar mysidecar.txt
...
a@slow:~$ cat mysidecar.txt
37.422,/DAlAAAAAAAAAP/wFAUAAAABf+/+ADNkLP4AKTLgAAEAAAAA05qKQQ==
67.422,/DAgAAAAAAAAAP/wDwUAAAABf0/+AFyXDAABAAAAAG47zrg=

```
* Repeat the above process for other ad breaks and they will be appended to the sidecar file.
```js
a@slow:~$ adbreak2 -p 220.333881 -d 45.75 -s mysidecar.txt

...
a@slow:~$ cat mysidecar.txt

37.422,/DAlAAAAAAAAAP/wFAUAAAABf+/+ADNkLP4AKTLgAAEAAAAA05qKQQ==
67.422,/DAgAAAAAAAAAP/wDwUAAAABf0/+AFyXDAABAAAAAG47zrg=
220.333881,/DAlAAAAAAAAAP/wFAUAAAABf+/+AS6VIf4APtP8AAEAAAAAy49C5g==
266.083881,/DAgAAAAAAAAAP/wDwUAAAABf0/+AW1pHQABAAAAAKGAea0=
```
### `Step 2.` Use superkabuki to encode the ad breaks into the MPEGTS stream.
```js
a@slow:~$ superkabuki -i input.ts -o output_with_scte35.ts -s mysidecar.txt --scte35_pid 355

Output File:    output_with_scte35.ts
PMT Section Length: 29
Program Number: 1
PCR PID: 257
Program Info Length: 0

Added Registration Descriptor:
        b'\x05\x04CUEI'

Found Streams:
        Stream Type: 15  PID: 256  EI Len:  6
        Stream Type: 27  PID: 257  EI Len:  0

Added Stream:
        Stream Type: 134 PID: 355 EI Len:  3   # This is the new SCTE-35 Stream 

# the PTS times are adjusted to make sure the ad break is on an iFrame

Inserted Cue:        
        @37.502733, /DAlAAAAAAAAAP/wFAUAAAABf+/+ADNkLP4AKTLgAAEAAAAA05qKQQ==

Inserted Cue:
        @67.532733, /DAgAAAAAAAAAP/wDwUAAAABf0/+AFyXDAABAAAAAG47zrg=

Inserted Cue:
        @221.686733, /DAlAAAAAAAAAP/wFAUAAAABf+/+AS6VIf4APtP8AAEAAAAAy49C5g==

Inserted Cue:
        @267.732733, /DAgAAAAAAAAAP/wDwUAAAABf0/+AW1pHQABAAAAAKGAea0=
a@slow:~$
```


#### for HLS use [x9k3](https://github.com/futzu/x9k3)  with adbreak2.

# `FIN`
