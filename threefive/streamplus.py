from .splice import Splice
from .stream import Stream
from bitn import BitBin


class StreamPlus(Stream):
    '''
    Subclass of the Stream Class
    that also parses the PTS
    for the SCTE 35 packet.
    '''
    NON_PTS_STREAM_IDS = [188, 190, 191, 240, 241, 242, 248]

    def __init__(self, tsdata, show_null = False):
        super().__init__(tsdata, show_null)
        self.PTS= False

    def verify_pusi(self,bitbin):
        '''
        If the pusi data contains these markers,
        we can pull a PTS value..
        '''
        if bitbin.asint(24) != 1: return False
        if bitbin.asint(8) in self.NON_PTS_STREAM_IDS: return False 
        bitbin. forward(16) 
        if bitbin.asint(2) != 2: return False
        bitbin.forward(6)
        if bitbin.asint(2) != 2: return False 
        bitbin.forward(14) 
        if bitbin.asint(4) != 2: return False 
        self.parse_pts(bitbin)
        return

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
        bitbin = BitBin(packetdata)
        self.verify_pusi(bitbin)
        return
    
    def packet_has_pusi(self,two_bytes):
        '''
        check for pusi in header
        '''
        pusi = two_bytes >> 14 & 0x1
        return pusi

    def parse_payload(self,payload,pid):
        '''
        Override this method to customize output
        '''
        try:
            tf = Splice(payload,pid=pid, pts=self.PTS)
            tf.show()
            return tf
        except: return False
        
    def parse_tspacket(self, packet):
        '''
        parse a mpegts packet for SCTE 35 and/or PTS
        '''
        if not self.has_sync_byte(packet[0]):return
        two_bytes=self.next_two_bytes(packet[1:3])
        pid = self.the_packet_pid(two_bytes)
        # No PTS times in pid 101
        if pid == 101: return
        if self.packet_has_pusi(two_bytes):
            self.parse_pusi(packet[4:20])
        if not self.has_scte35_tid(packet[5]) : return 
        if self.SCTE35_PID and (pid != self.SCTE35_PID): return
        if not self.show_null:
            if packet[18] == 0: return
        tf = self.parse_payload(packet[5:],pid)
        if tf:
            if not self.SCTE35_PID:
                self.SCTE35_PID = pid
        tf = False
        return
