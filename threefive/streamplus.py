from .splice import Splice
from bitn import BitBin
from .stream import Stream
from struct import unpack

class StreamPlus(Stream):
    '''
    StreamPlus adds PID and PTS for the SCTE 35 packets
    to the Stream class.
    '''
    SYNC_BYTE = b'G'
    NON_PTS_STREAM_IDS = [188, 190, 191, 240, 241, 242, 248]

    def __init__(self, tsdata, show_null = False):
        self.SCTE35_PID = False
        self.PTS= False
        super().__init__(tsdata,show_null)
  
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
        return unpack('>H', two_bytes)[0]
        #return int.from_bytes(two_bytes,byteorder='big')
  
    def the_packet_pid(self,two_bytes):
        '''
        parse packet pid from two bytes
        of the header
        '''
        return two_bytes & 0x1fff

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
        '''
        If the pusi data contains these markers,
        we can pull a PTS value..
        '''
        if  packetdata[2] != 1: return False
        if packetdata[3] in self.NON_PTS_STREAM_IDS: return False 
        if (packetdata[6]>>6) != (packetdata[7]>>6): return False
        if packetdata[9] >> 4 != 2: return False
        bitbin = BitBin(packetdata[9:])
        bitbin.forward(4)
        self.parse_pts(bitbin)
        return


    def parse_payload(self,payload,pid):
        '''
        Override this method to customize output
        '''
        try:
            tf = Splice(payload,pid=pid, pts=self.PTS)
            tf.show()
        except: pass
        
    def parse_tspacket(self, packet):
        '''
        parse a mpegts packet for SCTE 35 and/or PTS
        '''
        two_bytes=unpack('>H', packet[1:3])[0]
        pid = two_bytes & 0x1fff
        pusi = two_bytes >> 14 & 0x1
        if pusi: self.parse_pusi(packet[4:20])
        if packet[5] is not self.SCTE35_TID : return  False
        if packet[18] not in self.SPLICE_CMD_TYPES: return False
        self.parse_payload(packet[5:],pid)
        return
