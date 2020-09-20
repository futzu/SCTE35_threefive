from .splice import Splice
from functools import partial
from struct import unpack

class Stream:
    '''
    threefive.Stream(tsdata, show_null = False)
    Fast parse mpegts files and streams
    for SCTE 35 packets
    
    tsdata should be a _io.BufferedReader instance:
    example:
        import threefive
        with open('vid.ts','rb') as tsdata:
            threefive.Stream(tsdata)
            
    SCTE-35 Splice null packets are ignored by default. 
    Set show_null = True to show splice null. 

    '''
    cmd_types = [4,5,6,7,255] # splice command types
    packet_size = 188
    def __init__(self,tsdata, show_null = False):
        # set show_null to parse splice null packets
        if show_null:
            self.cmd_types.append(0)
        self.tsdata = tsdata 
        self.decodenext = False
        self.next = self.decode_until_found

    def decode(self):
        '''
        Stream.decode() reads MPEG-TS
        to find SCTE-35 packets.
        ''' 
        for packet in iter( partial(self.tsdata.read, self.packet_size), b''):
            if self.chk_magic(packet):
                # Only parse headers on SCTE-35 packets
                self.parse_header(packet)
                cuep = Splice(packet,self.packet_data)                            
                if self.decodenext:
                    return cuep
                cuep.show()

    def decode_until_found(self):
        '''
        Stream.decode_until_found() reads MPEG-TS
        to find a SCTE-35 packet and returns the packet
        when found.
        ''' 
        self.decodenext = True
        cuep = self.decode()
        if cuep:
            return cuep
        return False

    def parse_header(self,packet):
        '''
        Stream.parse_header(packet)
        reads a MPEG-TS packet header
        for a pid.
        '''
        two_bytes, = unpack('>H', packet[1:3])
        pid = two_bytes & 0x1fff
        self.packet_data ={'pid':pid}

    def chk_magic(self,packet):
        '''
        Stream.chk_magic(packet)
        does fast SCTE-35 packet detection
        '''
        if packet[5] == 0xfc:
            if packet[6] == 48: 
                if packet[8] == 0:
                    if packet[15] == 255:
                        return packet[18] in self.cmd_types
