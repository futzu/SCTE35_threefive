import sys
from .splice import Splice
from .stream import Stream
from .live_stream import LiveStream
    
def read_stdin(scte35):
    print(f'\n Reading from stdin')
    try:
        scte35 = LiveStream(tsstream=sys.stdin.buffer, show_null=False)
    except BaseException:
        scte35 = Splice(sys.stdin.buffer) 
        scte35.show()
    return scte35

def read_stuff(stuff,scte35):
    try:
        scte35 = Splice(stuff)
        scte35.show()
    except BaseException:
        try:
            print(f'\nfile: {stuff}')
            scte35 = Stream(tsfile=stuff, show_null=False)
        except BaseException:
            pass
    return scte35


def decode(stuff = None):
    """
    All purpose SCTE 35 decoder function
    the  stuff arg can be
         mpegts file,
         binary file,
         base64 encoded string,
         binary encoded string,
         hex encoded string.

    usage:

    # for a mpegts video

    import threefive
    threefive.decode('/path/to/mpegts')

    # for a base64 encoded string

    import threefive
    Bee64='/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g='
    threefive.decode(Bee64)
    
    Calling decode with out a value for stuff causes decode to attempt to read bytes 
    from sys.stdin.buffer as tsstream for a Stream instance, 
    with a fallback to call Splice in the case of a message string being piped in.    
    
    I realize this is a bit klunky, the only goal of the decode fuction is to make 
    it easy for folks to use threefive without having to learn a bunch of options just to 
    get started. 
    I am open to suggestions.
    
    
    """
    
    scte35 = None
    
    if stuff in [None,sys.stdin.buffer]: 
        return read_stdin(scte35)
    else: 
        return read_stuff(stuff,scte35)


