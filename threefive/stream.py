from .splice import Splice

class Stream:
    '''
    Parse mpegts files and streams for SCTE 35 packets
    '''
    pkt_sz = 188
    pkt_ct = 384
    magic_bytes = b'\xfc0' # pattern used to detect scte35 packets.
    cmd_types = [4,5,6,7,255] # SCTE 35 splice command types

    def __init__(self,tsdata, show_null = False):
        if show_null:
            self.cmd_types.append(0)
        self.tsdata = tsdata

    def decode(self):
        '''
        split data into
        chunks of 188 byte packets
        '''
        chunk_sz = self.pkt_sz * self.pkt_ct
        while self.tsdata:
            chunky = self.tsdata.read(chunk_sz)
            if not chunky: break
            self.packets = [chunky[i:i+self.pkt_sz] for i in range(0, len(chunky), self.pkt_sz)]
            self.parse_packets()

    def chk_magic(self,pkt):
        '''
        Fast scte35
        packet detection
        '''
        if pkt[5:7] == self.magic_bytes: # splice info section tid and reserved
            if pkt[8] == 0: # splice info section protocol has to be 0
                return pkt[18] in self.cmd_types# splice info section command types
        return False

    def parse_packets(self):
        [Splice(pkt).show_command() for pkt in filter(self.chk_magic,self.packets)]
