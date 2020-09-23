import sys
from threefive import StreamProxy

'''
StreamProxy class example.
writes SCTE-35 data to stderr (in green)
writes the MPEG-TS packets to stdout
so you can pipe it.

Example:

python3 proxydemo.py video.ts | mplayer - 

'''


def do():
   with open(sys.argv[1],'rb') as tsdata:
      cue = StreamProxy(tsdata).decode() 
   
if __name__ == '__main__':
    do()

