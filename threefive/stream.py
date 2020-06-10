from .splice import Splice
import sys

class Stream:
    '''
    Fast parse mpegts files and streams
    for SCTE 35 packets
    '''
    cmd_types = [4,5,6,7,255] # splice command types
    sync_byte = b'G'
    def __init__(self,tsdata, show_null = False):
        if show_null:
            self.cmd_types.append(0)
        self.tsdata = tsdata

    def decode(self):
        '''
        Split data into 188 byte packets
        '''
        pkt_sz = 188  # mpegts packet size
        pkt_ct = 384 # packet count
        chunk_sz = pkt_sz * pkt_ct
        while self.tsdata:
            first_byte = self.tsdata.read(1)
            if not first_byte: break
            if first_byte == self.sync_byte:
                chunk = first_byte + self.tsdata.read(chunk_sz -1)
                if not chunk: break
                self.parse([chunk[i:i+pkt_sz]
                        for i in range(0,len(chunk),pkt_sz)])

    def chk_tid(self,byte5):
        return byte5 == 0xfc

    def chk_resrvd(self,byte6):
        return byte6 >> 4 == 3

    def chk_prvt(self, byte8):
        return byte8 == 0

    def chk_cmdtype(self,byte18):
        return byte18 in self.cmd_types
    
    def chk_magic(self,packet):
        '''
        Fast scte35 packet detection
        '''
        if self.chk_tid(packet[5]):
            if self.chk_resrvd(packet[6]):
                if self.chk_prvt(packet[8]): 
                    if self.chk_cmdtype(packet[18]):
                        return True
        return False
    
    def parse(self,packets):
        '''
        Parse scte35 packets
        '''
        [Splice(pkt).show() for pkt in filter(self.chk_magic,packets)]
