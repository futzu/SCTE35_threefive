from .util import PACKET_SIZE
from .splice import Splice
from struct import unpack

SYNC_BYTE=b'\x47'

class Stream:
    def __init__(self,tsfile=None,show_null=True):
        self.splices=[]
        self.PID=False
        self.show_null=show_null
        self.tsfille=4
        self.parse_tsfile(tsfile)

    def parse_tsfile(self,tsfile):
        with open(tsfile,'rb') as tsdata:
            while tsdata:
                # read a byte and see if it's a SYNC_BYTE, if so , read a packet. 
                sync_chk=tsdata.read(1)
                if sync_chk==SYNC_BYTE:
                    packet =sync_chk+ tsdata.read(PACKET_SIZE-1)
                    if len(packet) == PACKET_SIZE:  self.parse_tspacket(packet)
                    else: break
                else: return
                
    def parse_tspacket(self,packet):
        sync, pid, _, cue = unpack('>BHH183s', packet)
        pid= pid & 0x1fff
        if self.PID:
            if pid !=self.PID: return
        if cue[0]==0xfc:
            if cue[13]==0:
                if not self.show_null: return 
            try:
                tf=Splice(cue)
                if tf:
                    tf.show()
                    self.splices.append(tf)
                    if not self.PID: self.PID=pid
            finally: return
