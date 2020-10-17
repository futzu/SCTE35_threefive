from .decode import decode
from .cue import Cue
from .stream import Stream

def i2b(i,wide):
    return int.to_bytes(i,wide,byteorder='big')
