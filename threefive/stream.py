from .splice import Splice
from bitn import BitBin


class Stream:
    '''
    Parse mpegts files and streams for SCTE 35 packets
    '''
    PACKET_SIZE = 188
    PACKET_COUNT = 512
    SYNC_BYTE = 0x47
    NON_PTS_STREAM_IDS = [188, 190, 191, 240, 241, 242, 248]
    SCTE35_TID = 0xfc

    def __init__(self, tsfile = None, tsstream = None, show_null = False):
        self.SCTE35_PID = False
        self.PTS= False
        self.show_null = show_null
        if tsfile: self.parse_tsfile(tsfile) # for files
        if tsstream: self.parse_tsdata(tsstream) # for reading from stdin

    def parse_tsfile(self, tsfile):
        '''
        used only to open a local file
        '''
        with open(tsfile, 'rb') as tsdata:
            self.parse_tsdata(tsdata)
        return     

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
    
    def parse_pusi(self, packet):
        bitbin = BitBin(packet)
        self.verify_pusi(bitbin)
        return

    def has_sync_byte(self,first_byte):
        '''
        return True if first_byte
        is equal to self.SYNC_BYTE,
        
        '''
        return (first_byte == self.SYNC_BYTE)
    
    def next_two_bytes(self,two_bytes):
        '''
        returns the second and third
        header bytes as an int
        '''
        return int.from_bytes(two_bytes,byteorder='big')
        
    def packet_has_pusi(self,two_bytes):
        pusi = two_bytes >> 14 & 0x1
        return pusi
            
    def the_packet_pid(self,two_bytes):
        '''
        parse packet pid from two bytes
        of the header
        '''
        return two_bytes & 0x1fff
        
    def has_scte35_tid(self,byte5):
        '''
        byte 5 of a SCTE 35 packet must be
        self.SCTE35_TID to be valid
        '''
        return (byte5 == self.SCTE35_TID)

    def try_splice(self,payload,pid):
        try:
            tf = Splice(payload,pid=pid, pts=self.PTS)
            tf.show()
            return True
        except:
            return False
        
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
        if not self.try_splice(packet[5:],pid): return
        if not self.SCTE35_PID: self.SCTE35_PID = pid
        return
