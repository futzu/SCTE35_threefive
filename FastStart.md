## Fast Start  (Requires Python3 and Curl)


### Up and Running in Less Than Thirty-Seven Seconds


* pip install threefive
```python
pip install threefive
```
* Create a file call it cli.py, and put the following in it.
 ```js
#!/usr/bin/env python3
import sys
import threefive

"""
example command line tool.
pass in a file name or message string to decode

example:
python cli.py '/DBIAAAAAAAA///wBQb+ek2ItgAyAhdDVUVJSAAAGH+fCAgAAAAALMvDRBEAAAIXQ1VFSUgAABl/nwgIAAAAACyk26AQAACZcuND'

or
python cli.py /path/to/mpeg.ts

"""

def do():
   try: 
       threefive.decode(sys.argv[1])
   except: 
       # Handles piped in data
       try: threefive.decode()
       except: pass
if __name__ =='__main__':
   do()

```
* Parse SCTE 35 and PTS data from a video over the network
```bash
 curl -s https://futzu.com/mpegwithscte35.ts -o - | python3 cli.py 
```


