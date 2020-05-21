from .splice import Splice
from bitn import BitBin
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
        a = bitbin.asint(3) << 30   # read 3 bits as unsigned int and left shift 30
        bitbin.forward(1)           
        b = bitbin.asint(15) << 15  # read 15 bits as unsigned int and left shift 15
        bitbin.forward(1)          
        c = bitbin.asint(15)        # read 15 bits as unsigned int
        d = (a+b+c)/90000.0
        # self.PTS is updated when we find a pts.
        self.PTS=round(d,6)
        return
    
    def parse_pusi(self, packetdata):
        '''
        If the pusi data contains these markers,
        we can pull a PTS value..
        '''
        if packetdata[2] != 1: return False
        if packetdata[3] in self.NON_PTS_STREAM_IDS: return False 
        if (packetdata[6] >> 6) != 2: return False
        if (packetdata[7] >> 6) != 2: return False
        if (packetdata[9] >> 4) != 2: return False
        bitbin = BitBin(packetdata[9:])
        bitbin.forward(4)
        self.parse_pts(bitbin)
        return

    def parse_packet(self,packet):
        two_bytes = int.from_bytes(packet[1:3],byteorder='big')
        pid = two_bytes & 0x1fff
        pusi = two_bytes >> 14 & 0x1
        if pusi: 
            self.parse_pusi(packet[4:20])
        if self.chk_tid(packet):
            if self.chk_type(packet[:20]):
                Splice(packet, pid = pid, pts = self.PTS).show() 
    
    def parse_packets(self):
        [self.parse_packet(packet) for packet in self.packets]
