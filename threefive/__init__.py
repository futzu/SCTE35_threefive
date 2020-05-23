from .decode import decode
#from .segmentation import Segmentation_Descriptor
from .splice import Splice
from .stream import Stream
from .streamplus import StreamPlus
from .splice_info_section import Splice_Info_Section

def i2b(i,wide):
    return int.to_bytes(i,wide,byteorder='big')
