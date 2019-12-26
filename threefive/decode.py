
import sys
from .splice import Splice
from .stream import Stream

def decode(stuff):
    '''
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

    '''
    try: 
        scte35=Splice(stuff)
        scte35.show()
        return scte35
    except: 
        try:  
            return Stream(stuff,show_null=False)
        except: 
            print(' No SCTE 35 data found')  
            return None
