from .splice import Splice
import sys
from functools import partial

class Stream:
    '''
    Fast parse mpegts files and streams
    for SCTE 35 packets
    '''
    cmd_types = [4,5,6,7,255] # splice command types
    sync_byte = b'G'
    packet_size = 188
    def __init__(self,tsdata, show_null = False):
        if show_null:
            self.cmd_types.append(0)
        self.tsdata = tsdata
        self.decodenext = False

    def parse_packet(self,packet):
        two_bytes = int.from_bytes(packet[1:3],byteorder='big')
        pid = hex(two_bytes & 0x1fff)
        self.packet_data ={'pid':pid}

    def decode(self):
        '''
        StreamParser.parse reads a
        file handle object or from stdin
        to find SCTE-35 packets.
        '''
        
        for packet in iter( partial(self.tsdata.read, self.packet_size), b''):
            if packet[5] == 0xfc:
                if packet[6] == 48: 
                    if packet[8] == 0:
                        if packet[18] in self.cmd_types:
                            self.parse_packet(packet)
                            cuep = Splice(packet,self.packet_data)                            
                            if self.decodenext:
                                return cuep
                            cuep.show()

    def decode_until_found(self):
        self.decodenext = True
        cuep = self.decode()
        if cuep:
            return cuep
        return False


        
    


                            
