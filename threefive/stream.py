from .splice import Splice
from struct import unpack
from .util import bit_slice


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
        two_bytes,one_byte,_, cue = unpack('>HBB183s', packet)
        pid=bit_slice(two_bytes,12,13)
        if self.PID and (pid !=self.PID): return
        if cue[0] !=0xfc : return
        try:tf=Splice(cue)
        except: return 
        if not self.PID: 
            self.PID=pid
            print(f'\n\n[  SCTE 35 Stream found with Pid {hex(self.PID)}  ]')
        if not self.show_null and (cue[13]==0) : return
        tei=bit_slice(two_bytes,15,1)
        pusi=bit_slice(two_bytes,14,1)
        ts_priority=bit_slice(two_bytes,13,1)
        scramble=bit_slice(one_byte,7,2)
        afc=bit_slice(one_byte,5,2)
        count=bit_slice(one_byte,3,4)
        tf.show()
        self.splices.append(tf)
        return

