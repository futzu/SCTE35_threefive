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


   
if __name__ == '__main__':
	try: 
  	threefive.decode(sys.argv[1])
	except: 
  	# Handles piped in data
    try: 
    	threefive.decode()
    except: 
    	pass
```
* Parse SCTE 35 and PTS data from a video over the network
```bash
 curl -s https://futzu.com/mpegwithscte35.ts -o - | python3 cli.py 
```


