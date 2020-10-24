from .decode import decode
from .cue import Cue
from .stream import Stream
from .streamb import StreamB
from .version import version

def i2b(i,wide):
    return int.to_bytes(i,wide,byteorder='big')
