from .util import PACKET_SIZE
from .splice import Splice
from struct import unpack

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
                packet = tsdata.read(PACKET_SIZE)
                if not packet: break
                self.parse_tspacket(packet)

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
