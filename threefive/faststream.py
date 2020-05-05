from .splice import Splice

class FastStream:
    '''
    Parse mpegts files and streams for SCTE 35 packets
    '''
    SYNC_BYTE = 0x47
    SCTE35_TID = 0xfc
    PACKET_SIZE = 188
    PACKET_COUNT = 386
    SPLICE_CMD_TYPES = [4,5,6,7,255]
    
    def __init__(self, tsdata):
        self.parse_tsdata(tsdata)

    def parse_tsdata(self, tsdata):
        '''
         split tsdata into packets for parsing
        '''
        while tsdata:
            chunky = tsdata.read(self.PACKET_SIZE * self.PACKET_COUNT)
            if not chunky: break
            [self.parse_tspacket(chunky[i:i+self.PACKET_SIZE] )
                     for i in range(0, len(chunky), self.PACKET_SIZE)]
        return

    def parse_payload(self,payload):
        try: Splice(payload).show()
        except: pass
        
    def parse_tspacket(self, packet):
        '''
        parse a mpegts packet for SCTE 35 and/or PTS
        '''
        if packet[5] == self.SCTE35_TID : 
            if packet[18] in self.SPLICE_CMD_TYPES:
                self.parse_payload(packet[5:])
        return
