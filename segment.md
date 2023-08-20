  ### The threefive.Segment Class
The Segment class is a sub class of threefive.Stream,<br/> designed for processing HLS segments.

   
* Segment Class Specific Features:
  * Decryption of AES Encrypted MPEGTS.
  * Segment.cues  a list of SCTE35 cues found in the segment.
---
* Usage:

```lua

from threefive import Segment

uri = "https://example.com/1.ts"
seg = Segment(uri)
seg.decode()
  
# Make a list comprehension of cues found in the segment.
data = [cue.encode() for cue in seg.cues]
print(data)

['/DARAAAAAAAAAP/wAAAAAHpPv/8=',
'/DAvAAAAAAAAAP/wFAUAAAKWf+//4WoauH4BTFYgAAEAAAAKAAhDVUVJAAAAAOv1oqc=']

```

* For aes encrypted files


```lua
from threefive import Segment

key = "https://example.com/aes.key"
IV=0x998C575D24F514AEC84EDC5CABCCDB81
uri = "https://example.com/aes-1.ts"

seg = Segment(uri,key_uri=key, iv=IV)
seg.decode()

# make a dictionary comprehension of pts and base64 encoded cues 

data = {cue.packet_data.pts:cue.encode() for cue in seg.cues}

print(data)

{ 89718.451333: '/DARAAAAAAAAAP/wAAAAAHpPv/8=',
89730.281789: '/DAvAAAAAAAAAP/wFAUAAAKWf+//4WoauH4BTFYgAAEAAAAKAAhDVUVJAAAAAOv1oqc='}
```

