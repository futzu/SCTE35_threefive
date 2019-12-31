from .splice import Splice
from .util import bitslice
from bitslicer9k import BitSlicer9k

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
        three_bytes=BitSlicer9k(packet[:2])
        tei=three_bytes.boolean(1)
        pusi=three_bytes.boolean(1)
        ts_priority=three_bytes.boolean(1)
        pid=three_bytes.slice(13)
        if self.PID and (pid !=self.PID): return
        cue=packet[4:]
        try:tf=Splice(cue)
        except: return 
        if not self.PID: 
           self.PID=pid
           print(f'\n\n[  SCTE 35 Stream found with Pid {hex(self.PID)}  ]')
        if not self.show_null and (cue[13]==0) : return
        '''
        scramble=bitslice(one_byte,7,2)
        afc=bitslice(one_byte,5,2)
        count=bitslice(one_byte,3,4)
        '''
        tf.show()
        self.splices.append(tf)
        return

    def show(self):
        for s in self.splices:
            print( f'\n[ Splice {self.splices.index(s)} ]')
            s.show()
