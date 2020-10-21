import sys

from .cue import Cue
from .stream import Stream


def read_stdin():
    ssb = sys.stdin.buffer.read(1)
    if ssb == b'G':
        sys.stdin.buffer.seek(0)   
        Stream(sys.stdin.buffer).decode()
    else:
        try:
            stuff = ssb+sys.stdin.buffer.read()
            Cue(stuff).show()
        except Exception:
            pass

def read_stuff(stuff):
    try:
        Cue(stuff).show()
    except Exception:
        try:
            with open(stuff, 'rb') as tsdata:
                Stream(tsdata).decode()
        except Exception:
            pass        

def decode(stuff=None):
    '''
    All purpose SCTE 35 decoder function

    # for a mpegts video

        import threefive
        threefive.decode('/path/to/mpegts')

    # for a base64 encoded string

        import threefive
        Bee64='/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g='
        threefive.decode(Bee64)  
    '''
    if stuff in [None, sys.stdin.buffer]:
        read_stdin()
    else:
        read_stuff(stuff)
