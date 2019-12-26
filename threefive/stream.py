from .splice import Splice
from struct import unpack
from .util import grab_bits


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
                    if not packet:  break
                    self.parse_tspacket(packet)
                else: return 

    def parse_tspacket(self,packet):
        two_bytes,one_byte,_, cue = unpack('>HBB183s', packet)
        pid=grab_bits(two_bytes,12,13)
        if self.PID:
            if pid !=self.PID: return
        if cue[0] !=0xfc : return
        if cue[13]==0: 
            if not self.show_null: return 
        tei=grab_bits(two_bytes,15,1)
        pusi=grab_bits(two_bytes,14,1)
        ts_priority=grab_bits(two_bytes,13,1)
        scramble=grab_bits(one_byte,7,2)
        afc=grab_bits(one_byte,5,2)
        count=grab_bits(one_byte,3,4)
        try:tf=Splice(cue)
        except: return 
        if not self.PID: 
            self.PID=pid
            print(f'\n\n[  SCTE 35 Stream found with Pid {hex(self.PID)}  ]')
        tf.show()
        self.splices.append(tf)
        return

