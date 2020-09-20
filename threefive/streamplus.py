from bitn import BitBin
from .splice import Splice
from .stream import Stream
from functools import partial
from struct import unpack

class StreamPlus(Stream):
    '''
    StreamPlus adds PTS for the SCTE 35 packets
    to the Stream class.
    '''
    NON_PTS_STREAM_IDS = [188, 190, 191, 240, 241, 242, 248]

    def __init__(self, tsdata, show_null = False):
        self.PTS = False
        super().__init__(tsdata,show_null)

    def decode(self):
        '''
        StreamParser.decode() reads MPEG-TS
        to find SCTE-35 packets.
        ''' 
        for packet in iter( partial(self.tsdata.read, self.packet_size), b''):
            # parse all packets headers first
            self.parse_header(packet) 
            if self.chk_magic(packet):
                cuep = Splice(packet,self.packet_data)                            
                if self.decodenext:
                    return cuep
                cuep.show()
                
    def parse_header(self,packet):
        '''
        StreamParser.parse_header(packet)
        reads a MPEG-TS packet header
        for pid and/or pusi.
        '''
        two_bytes, = unpack('>H', packet[1:3])
        pid = two_bytes & 0x1fff
        pusi = two_bytes >> 14 & 0x1
        if pusi:
                self.parse_pusi(packet[4:20])
        self.packet_data = {'pid':pid,'pts':self.PTS}
      
    def parse_pts(self,bitbin):
        '''
        StreamPlus.parse_pts(bitbin)
        This is the process described in the official
        Mpeg-ts specification.
        '''
        a = bitbin.asint(3) << 30
        bitbin.forward(1)          
        b = bitbin.asint(15) << 15
        bitbin.forward(1)          
        c = bitbin.asint(15)
        d = (a+b+c)/90000.0
        # self.PTS is updated when we find a pts.
        self.PTS=round(d,6)
    
    def parse_pusi(self, pusidata):
        '''
        StreamPlus.parse_pusi(pusidata)
        If the pusi data contains these markers,
        we can pull a PTS value..
        '''
        if pusidata[2] == 1: 
            if pusidata[3] not in self.NON_PTS_STREAM_IDS:
                if (pusidata[6] >> 6) == 2:
                    if (pusidata[7] >> 6) == 2:
                        if (pusidata[9] >> 4) == 2:
                            bitbin = BitBin(pusidata[9:])
                            bitbin.forward(4)
                            self.parse_pts(bitbin)
