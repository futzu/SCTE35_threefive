

 ### Fast Start 

* Install python3 and curl
* pip install threefive
```python
pip install threefive
```
* Create a file call it cli.py, and put the following in it.
 ```python3
#!/usr/bin/env python3

import sys
import threefive
 
def do():
    try: 
        threefive.decode(sys.argv[1])
    except: 
        # Handles piped in data
        try: threefive.decode()
        except: pass
   
if __name__ == '__main__':
    do()   
```
* Chmod cli.py
```bash
chmod +x cli.py
```
* Parse SCTE 35 and PTS data from a video over the network( requires curl )
```bash
 curl -s https://futzu.com/mpegwithscte35.ts -o - | ./cli.py 
```


