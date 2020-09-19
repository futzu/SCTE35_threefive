from bitn import BitBin
from .splice import Splice
from .stream import Stream
from functools import partial
from struct import unpack

class StreamPlus(Stream):
    '''
    StreamPlus adds PID and PTS for the SCTE 35 packets
    to the Stream class.
    '''
    NON_PTS_STREAM_IDS = [188, 190, 191, 240, 241, 242, 248]

    def __init__(self, tsdata, show_null = False):
        self.PTS = False
        super().__init__(tsdata,show_null)

    def decode(self):
        '''
        StreamParser.parse reads a
        file handle object or from stdin
        to find SCTE-35 packets.
        '''
        pusi_count=0
        for packet in iter( partial(self.tsdata.read, self.packet_size), b''):
            two_bytes,one_byte = unpack('>HB', packet[:3])
            pusi = two_bytes >> 14 & 0x1
            pid = two_bytes & 0x1fff
            if pusi:
                pusi_count +=1
                if pusi_count == 10:
                    pusi_count = 0
                    self.parse_pusi(packet[4:20])
            self.packet_data = {'pid':pid,'pts':self.PTS}
            if packet[5] == 0xfc:
                if packet[6] == 48: 
                    if packet[8] == 0:
                        if packet[18] in self.cmd_types:
                            cuep = Splice(packet,self.packet_data)                            
                            if self.decodenext:
                                return cuep
                            cuep.show()
        
    def parse_pts(self,bitbin):
        '''
        This is the process described in the official
        Mpeg-ts specification.
        '''
        a = bitbin.asint(3) << 30
        b = bitbin.asint(15) << 15
        bitbin.forward(1)          
        c = bitbin.asint(15)
        d = (a+b+c)/90000.0
   # self.PTS is updated when we find a pts.
        self.PTS=round(d,6)
    
    def parse_pusi(self, packetdata):
        '''
        If the pusi data contains these markers,
        we can pull a PTS value..
        '''
        if packetdata[2] == 1: 
            if packetdata[3] not in self.NON_PTS_STREAM_IDS:
                if (packetdata[6] >> 6) == 2:
                    if (packetdata[7] >> 6) == 2:
                        if (packetdata[9] >> 4) == 2:
                            #print(packetdata[6],packetdata[7],packetdata[9])    
                            bitbin = BitBin(packetdata[9:])
                            bitbin.forward(4)
                            self.parse_pts(bitbin)


