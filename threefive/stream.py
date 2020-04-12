from .splice import Splice
from bitn import BitBin
from struct import unpack


class Stream:
    '''
    Parse mpegts files and streams for SCTE 35 packets
    '''
    PACKET_SIZE = 188
    SYNCBYTE = 0x47
    NON_PTS_STREAM_IDS = [188, 190, 191, 240, 241, 242, 248]
    SCTE35_TID = 0xfc

    def __init__(self, tsfile = None, tsstream = None, show_null = False):
        self.PID = False
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
            pcount=256
            chunky = tsdata.read(self.PACKET_SIZE * pcount)
            packets= [chunky[i:i+self.PACKET_SIZE] for i in range(0, len(chunky), self.PACKET_SIZE)]
            if not packets: break
            [self.parse_tspacket(packet) for packet in packets]
        print(f'End @ \033[92m{self.PTS:.06f}\033[0m')           
      
        
    def parse_pusi(self, packet):
        bitbin = BitBin(packet)  # bitn.BitBin see https://github.com/futzu/bitn
        # read 24 bits as unsigned int and return if it is not 1
        if bitbin.asint(24) != 1: return
        # read 8 bits as unsigned int and check if it is in self.NON_PTS_STREAM_IDS
        if bitbin.asint(8) in self.NON_PTS_STREAM_IDS: return
        # skip next 16 bits
        bitbin.forward(16)
        if bitbin.asint(2) != 2: return
        # skip 6 bits
        bitbin.forward(6)
        # read 2 bits as unsigned int it should equal 2
        if bitbin.asint(2) != 2: return
        # skip 14 bits
        bitbin.forward(14)
        # read 4 bits as unsigned int it should equal 2
        if bitbin.asint(4) != 2: return
        a = bitbin.asint(3) << 30   # read 3 bits as unsigned int and left shift 30
        bitbin.forward(1)           # skip a bit
        b = bitbin.asint(15) << 15  # read 15 bits as unsigned int and left shift 15
        bitbin.forward(1)           # skip a bit
        c = bitbin.asint(15)        # read 15 bits as unsigned int
        d = (a+b+c)/90000.0         # 90k clock
        # print start time
        if not self.PTS: print(f'Start @ \033[92m{d:.06f}\033[0m')
        self.PTS=d
        return

    def parse_tspacket(self, packet):
        '''
        parse a mpegts packet.
        check for pusi, 
        parse pid, 
        if pusi, parse pusi for PTS,
        check if it's a scte 35 packet,
        parse it if it is scte 35
        set self.PID to the scte35 pid.
        '''
        if packet[0] != self.SYNCBYTE: return
        packet = packet[1:]
        # unpack two bytes or 16 bits

        #two_bytes = unpack('>H', packet[:2])[0]
        two_bytes= int.from_bytes(packet[:2],byteorder='big')
        # bit 15 is the Payload unit start indicator or pusi.
        # if pusi, parse for pts
        pusi = two_bytes >> 14 & 0x1
        # last 13 bits are the pid
        pid = two_bytes & 0x1fff
        # No PTS times in pid 101
        if pid == 101: return
        # Here's where you find PTS
        if pusi: self.parse_pusi(packet[3:19])
        # If self.PID is set, that is the scte35 pid, drop other packets. 
        if self.PID and (pid != self.PID): return
        # SCTE35_TID (0xfc) is required .
        if packet[4] != self.SCTE35_TID: return
        #  Only show splice_null commands if self.show_null is True
        if not self.show_null:
            if packet[17] == 0: return
        # this will fail on non scte 35 packets
        try: tf = Splice(packet[4:])
        except: return
        # print PTS time of scte35 packet
        print(f'PID {hex(pid)} SCTE 35 Packet @ \033[92m{self.PTS:.06f}\033[0m')
        # show scte 35 data 
        tf.show()
        # Set self.PID if not set yet, this is the scte35 pid 
        if not self.PID: self.PID = pid
        return
