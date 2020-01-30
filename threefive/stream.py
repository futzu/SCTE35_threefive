from .splice import Splice
from bitslicer9k import Slicer9k

PACKET_SIZE=188
SYNC_BYTE=b'\x47'


class Stream:
    def __init__(self,tsfile=None,show_null=True):
        self.splices=[]
        self.PID=False
        self.show_null=show_null
        self.parse_tsfile(tsfile)

    def parse_tsfile(self,tsfile):
        with open(tsfile,'rb') as tsdata:
            while tsdata:
                if tsdata.read(1)==SYNC_BYTE: 
                    packet =tsdata.read(PACKET_SIZE - 1)
                    if packet: self.parse_tspacket(packet)
                    else: break
                else: return 

    def parse_tspacket(self,packet):
        if packet[4] !=0xfc :return
        three_bytes=Slicer9k(packet[:3])
        tei=three_bytes.asflag(1)
        pusi=three_bytes.asflag(1)
        ts_priority=three_bytes.asflag(1)
        pid=three_bytes.asint(13)
        if self.PID and (pid !=self.PID): return
        scramble=three_bytes.asint(2)
        afc=three_bytes.asint(2)
        count=three_bytes.asint(4)
        cue=packet[4:]
        try:tf=Splice(cue)
        except: return 
        if not self.PID:  self.PID=pid
        if not self.show_null and (cue[13]==0) : return
        tf.show()
        self.splices.append(tf)
        return

    def show(self):
        for s in self.splices:
            print( f'\n[ Splice {self.splices.index(s)} ]')
            s.show()
