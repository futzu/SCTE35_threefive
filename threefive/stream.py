from .splice import Splice
from functools import partial

class Stream:
    '''
    Parse mpegts files and streams for SCTE 35 packets
    '''
    PACKET_SIZE = 188
    SCTE35_TID = 0xfc
    SPLICE_CMD_TYPES = [4,5,6,7,255]
    
    def __init__(self, tsdata, show_null = False):
        if show_null:  self.SPLICE_CMD_TYPES.append(0)
        self.parse_tsdata(tsdata)

    def parse_tsdata(self, tsdata):
        '''
         split tsdata into packets for parsing
        '''
        for block in iter(partial(tsdata.read, 188), b''):
            self.parse_tspacket(block)
        return

    def parse_payload(self,payload):
        try: Splice(payload).show()
        except: pass
        
    def parse_tspacket(self, packet):
        '''
        parse a mpegts packet for SCTE 35 and/or PTS
        '''
        if packet[5] is not self.SCTE35_TID : return
        if packet[18] in self.SPLICE_CMD_TYPES: self.parse_payload(packet[5:])        
        return
