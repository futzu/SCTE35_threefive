from .splice import Splice
from bitn import BitBin

class Stream:
    '''
    Parse mpegts files and streams for SCTE 35 packets
    '''
    PACKET_SIZE = 188
    PACKET_COUNT = 256
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

    def parse_tsdata(self, tsdata):
        '''
         split tsdata into packets for parsing
        '''
        while tsdata:
            chunky = tsdata.read(self.PACKET_SIZE * self.PACKET_COUNT)
            packets= [chunky[i:i+self.PACKET_SIZE] for i in range(0, len(chunky), self.PACKET_SIZE)]
            if not packets: break
            [self.parse_tspacket(packet) for packet in packets]
       # print(f'End @ \033[92m{self.PTS:.06f}\033[0m')           
      
    def parse_pusi(self, packet):
        bitbin = BitBin(packet)  # bitn.BitBin see https://github.com/futzu/bitn
        if bitbin.asint(24) != 1: return
        if bitbin.asint(8) in self.NON_PTS_STREAM_IDS: return
        bitbin.forward(16)
        if bitbin.asint(2) != 2: return
        bitbin.forward(6)
        if bitbin.asint(2) != 2: return
        bitbin.forward(14)
        if bitbin.asint(4) != 2: return
        a = bitbin.asint(3) << 30   # read 3 bits as unsigned int and left shift 30
        bitbin.forward(1)           
        b = bitbin.asint(15) << 15  # read 15 bits as unsigned int and left shift 15
        bitbin.forward(1)          
        c = bitbin.asint(15)        # read 15 bits as unsigned int
        d = (a+b+c)/90000.0         
        # if not self.PTS: print(f'Start @ \033[92m{d:.06f}\033[0m')
        self.PTS=round(d,6)
        return

    def parse_tspacket(self, packet):
        '''
        parse a mpegts packet for SCTE 35 and/or PTS
        '''
        if packet[0] != self.SYNC_BYTE: return
        packet = packet[1:]
        two_bytes= int.from_bytes(packet[:2],byteorder='big')
        pusi = two_bytes >> 14 & 0x1
        pid = two_bytes & 0x1fff
        # No PTS times in pid 101
        if pid == 101: return
        # Here's where you find PTS
        if pusi: self.parse_pusi(packet[3:19])
        # If self.PID is set, drop other packets. 
        if self.SCTE35_PID and (pid != self.SCTE35_PID): return
        if packet[4] != self.SCTE35_TID: return
        #  Only show splice_null commands if self.show_null is True
        if not self.show_null:
            if packet[17] == 0: return
        try: tf = Splice(packet[4:],pid=pid, pts=self.PTS)
        except: return 
        
        #print(f'PID \033[92m{hex(pid)}\033[0m SCTE 35 Packet @ \033[92m{self.PTS:.06f}\033[0m')
        tf.show()
        if not self.SCTE35_PID: self.SCTE35_PID = pid
        return
