from .splice import Splice
from functools import partial

class Stream:
    '''
    Parse mpegts files and streams for SCTE 35 packets
    '''
    PACKET_SIZE = 188
    PACKET_COUNT = 5384
    SCTE35_TID = 0xfc
    SPLICE_CMD_TYPES = [4,5,6,7,255]
    
    def __init__(self, tsdata, show_null = False):
        if show_null:  self.SPLICE_CMD_TYPES.append(0)
        self.parse_tsdata(tsdata)

    def parse_tsdata(self, tsdata):
        '''
         split tsdata into packets for parsing
        '''
        for packet in iter(partial(tsdata.read, self.PACKET_SIZE), b''):
            self.parse_tspacket(packet)
        '''
        while tsdata:
            chunky = tsdata.read(self.PACKET_SIZE * self.PACKET_COUNT)
            if not chunky: break
            [self.parse_tspacket(chunky[i:i+self.PACKET_SIZE] )
                     for i in range(0, len(chunky), self.PACKET_SIZE)]
        '''    
        return
 
    def parse_tspacket(self, packet):
        '''
        parse a mpegts packet for SCTE 35 and/or PTS
        '''
        if packet[5] is not self.SCTE35_TID : return
        if packet[18] in self.SPLICE_CMD_TYPES:
            try: 
                tf=Splice(packet)
                tf.show()
            except: pass  
        return
