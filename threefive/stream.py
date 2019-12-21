from .splice import Splice
from struct import unpack

PACKET_SIZE=188
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
                sync_chk=tsdata.read(1)
                if sync_chk==SYNC_BYTE:
                    packet =sync_chk+ tsdata.read(PACKET_SIZE-1)
                    if len(packet) == PACKET_SIZE:  self.parse_tspacket(packet)
                    else: break
                else: return 
                
                                
    def parse_tspacket(self,packet):
        sync, pid,_, cue = unpack('>BHB184s', packet)
        tei = pid & 0X8000
        pusi = pid & 0X4000 
        ts_priority = pid & 0X2000
        pid= pid & 0x1fff
        if self.PID:
            if pid !=self.PID: return
        cue=cue[1:]
        if cue[0] !=0xfc : return 
        if cue[13]==0:
            if not self.show_null: return 
        try: tf=Splice(cue)
        except: return 
        tf.show()
        self.splices.append(tf)
        if not self.PID: self.PID=pid
        return 
            

