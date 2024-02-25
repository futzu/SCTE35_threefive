## <pre>Triggering on SCTE-35 Events with threefive.Stream.<pre>


__threefive.Stream__, like all of the classes in threefive is made to be easy to customize and subclass. <br>

The __threefive.Stream__ class has a few ways to trigger on SCTE-35.<br>Most of the Stream methods take an optional arg __func__, a function to be called when a SCTE-35 Cue is found.  
<br>
The __func__ function __must__ take __only one arg__, and that is  __a threefive.Cue object__.
<br>
  
I use __sidecar__ files for some of my other projects a __sidecar__ file consists
of __(PTS, Cue)__ pairs, one per line.
<br>
<br> A __sidecar  file__ looks this.
<br><br>

```js
a@slow:~$ cat sidecar.txt 


41.273211,/DAWAAAAAAAAAP/wBQb+ADi52AAAp77zBQ==
42.240844,/DAWAAAAAAAAAP/wBQb+ADoZwgAAaVWytQ==
43.275211,/DAWAAAAAAAAAP/wBQb+ADt5rAAAXIo9lg==
44.276211,/DAWAAAAAAAAAP/wBQb+ADzZlgAAwI0IyA==
45.277211,/DAWAAAAAAAAAP/wBQb+AD45gAAA1tIPCQ==
46.244844,/DAWAAAAAAAAAP/wBQb+AD+ZagAAf8zc/g==
47.279211,/DAWAAAAAAAAAP/wBQb+AED5VAAAVMj9Dw==
48.246844,/DAWAAAAAAAAAP/wBQb+AEJZPgAAypfF7w==
49.281211,/DAWAAAAAAAAAP/wBQb+AEO5KAAAB99quQ==
```


One of the ways I use a sidecar file is to exact the SCTE-35 before using ffmpeg to encode to HLS, 
and then I use the sidecar file to generate HLS tags and insert them into the ffmpeg m3u8 files in real time. 

* To make a sidecar file, I write a function.

```py3

def mk_sidecar(cue):
    """
    mk_sidecar generates a sidecar file with the SCTE-35 Cues
    """
    pts = 0.0
    with open("sidecar.txt", "a") as sidecar:
        cue.show()
        if cue.packet_data.pts:
            pts = cue.packet_data.pts
        data = f"{pts},{cue.encode()}\n"
        sidecar.write(data)


```

* The only other step is to call __Stream.decode__ and pass in the mk_sidecar function.

* Here's the complete example to generate a sidecar file.

```py3

#!/usr/bin/env python3

import sys
from threefive import Stream


def mk_sidecar(cue):
    """
    mk_sidecar generates a sidecar file with the SCTE-35 Cues
    """
    pts = 0.0
    with open("sidecar.txt", "a") as sidecar:
        cue.show()
        if cue.packet_data.pts:
            pts = cue.packet_data.pts
        data = f"{pts},{cue.encode()}\n"
        sidecar.write(data)


if __name__ == '__main__':
        strm = Stream(sys.argv[1])
        strm.decode(func=mk_sidecar)



```
* Run it like this:

```py3
pypy3 sidecar_gen.py https://example.com/nmx.ts
```

* If you want to limit your sidecar file to the SCTE-35 in a specific MPEGTS program, call __decode_program__ instead.


```py3
if __name__ == '__main__':
	the_program = 3
        strm = Stream(sys.argv[1])
        strm.decode_program(the_program, func=mk_sidecar)

```

* To limit the sidecar file to SCTE-35 from a list of pids, call __decode_pids__. 

```py3
if __name__ == '__main__':
	scte35_pids =[259,1023,399]
        strm = Stream(sys.argv[1])
        strm.decode_pids(scte35_pids, func=mk_sidecar)

```

* to parse the video and then pipe it to ffmpeg or another program, __Stream.proxy__ writes the video stream sys.stdout.

```py3
if __name__ == '__main__':
	scte35_pids =[259,1023,399]
        strm = Stream(sys.argv[1])
        strm.proxy(func=mk_sidecar)

```

  

