from .splice import Splice
import sys

class Stream:
    '''
    Fast parse mpegts files and streams
    for SCTE 35 packets
    '''
    cmd_types = [4,5,6,7,255] # splice command types

    def __init__(self,tsdata, show_null = False):
        if show_null:
            self.cmd_types.append(0)
        self.tsdata = tsdata

    def decode(self):
        '''
        Split data into 188 byte packets
        '''
        pkt_sz = 188  # mpegts packet size
        pkt_ct = 256 # packet count
        chunk_sz = pkt_sz * pkt_ct
        while self.tsdata:
            chunk = self.tsdata.read(chunk_sz)
            if not chunk: break
            self.parse([chunk[i:i+pkt_sz]
                        for i in range(0,len(chunk),pkt_sz)])

    def chk_magic(self,packet):
        '''
        Fast scte35 packet detection
        '''
        if packet[5] == 0xfc: # info section TID
            if packet[6] >> 4 == 3: # info section reserved
                if packet[8] == 0: # info section private 
                    return packet[18] in self.cmd_types
        return False
    
    def parse(self,packets):
        '''
        Parse scte35 packets
        '''
        [Splice(pkt).show() for pkt in filter(self.chk_magic,packets)]
