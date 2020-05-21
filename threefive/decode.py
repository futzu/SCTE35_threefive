import sys
from .splice import Splice
from .stream import Stream


def read_stdin():
    scte35 = None
    try:
        scte35 = Stream(sys.stdin.buffer, show_null=False).decode()
    except BaseException:
        scte35 = Splice(sys.stdin.buffer)
        scte35.show()        
    return scte35

def read_stuff(stuff):
    scte35 = None
    try:
        scte35 = Splice(stuff)
        scte35.show()
    except BaseException:
        try:
            with open(stuff, 'rb') as tsdata:
                scte35 = Stream(tsdata,show_null=False).decode()
        except BaseException:
            pass        
    return scte35

def decode(stuff=None):
    """
    All purpose SCTE 35 decoder function
    
    usage:

    # for a mpegts video

    import threefive
    threefive.decode('/path/to/mpegts')

    # for a base64 encoded string

    import threefive
    Bee64='/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g='
    threefive.decode(Bee64)  
    """

    if stuff in [None, sys.stdin.buffer]:
        return read_stdin()
    else:
        return read_stuff(stuff)
