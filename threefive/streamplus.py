from bitn import BitBin
from .splice import Splice
from .stream import Stream


class StreamPlus(Stream):
    '''
    StreamPlus adds PID and PTS for the SCTE 35 packets
    to the Stream class.
    '''
    NON_PTS_STREAM_IDS = [188, 190, 191, 240, 241, 242, 248]

    def __init__(self, tsdata, show_null = False):
        self.PTS = False
        super().__init__(tsdata,show_null)

    def parse_pts(self,bitbin):
        '''
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
                            bitbin = BitBin(packetdata[9:])
                            bitbin.forward(4)
                            self.parse_pts(bitbin)

    def parse_packet(self,packet):
        two_bytes = int.from_bytes(packet[1:3],byteorder='big')
        pid = hex(two_bytes & 0x1fff)
        if (two_bytes >> 14 & 0x1):
            self.parse_pusi(packet[4:20])
        if self.chk_magic(packet[:20]):
            packet_data = {'pid':pid,'pts':self.PTS}
            Splice(packet,packet_data).show()
    
    def parse(self,packets):
        [self.parse_packet(packet) for packet in packets]
