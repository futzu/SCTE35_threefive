from .decode import decode
from .cue import Cue
from .stream import Stream
from .packet import Packet
def i2b(i,wide):
    return int.to_bytes(i,wide,byteorder='big')
