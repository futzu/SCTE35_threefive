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
        if tsfile: self.parse_tsfile(tsfile)
        if tsstream: self.parse_tsdata(tsstream)

    def parse_tsfile(self, tsfile):
        with open(tsfile, 'rb') as tsdata:
            self.parse_tsdata(tsdata)

    def parse_tsdata(self, tsdata):
        while tsdata:
            packets = tsdata.read(self.PACKET_SIZE * 8)
            if not packets: break
            while packets:
                p, packets = packets[:188], packets[188:]
                if p[0] != self.SYNCBYTE: return
                self.parse_tspacket(p[1:])
            
        print(f'End @ \033[92m{self.PTS:.06f}\033[0m')

    def parse_pusi(self, packet):
        bitbin = BitBin(packet)
        if bitbin.asint(24) != 1: return
        if bitbin.asint(8) in self.NON_PTS_STREAM_IDS: return
        bitbin.forward(16)
        if bitbin.asint(2) != 2: return
        bitbin.forward(6)
        if bitbin.asint(2) != 2: return
        bitbin.forward(14)
        if bitbin.asint(4) != 2: return
        a = bitbin.asint(3) << 30
        bitbin.forward(1)
        b = bitbin.asint(15) << 15
        bitbin.forward(1)
        c = bitbin.asint(15)
        d = (a+b+c)/90000.0
        if not self.PTS: print(f'Start @ \033[92m{d:.06f}\033[0m')
        self.PTS=d
        return

    def parse_tspacket(self, packet):
        two_bytes = unpack('>H', packet[:2])[0]
        pusi = two_bytes >> 14 & 0x1
        pid = two_bytes & 0x1fff
        # No PTS times in pid 101
        if pid == 101: return
        # Here's where you find PTS
        if pusi: self.parse_pusi(packet[3:19])
        if self.PID and (pid != self.PID): return

        # SCTE35_TID (0xfc) is required .
        if packet[4] != self.SCTE35_TID: return
        #  If the SCTE 35 pid is known, the packet pid must match.
        #  Only show splice_null commands if self.show_null is True
        if not self.show_null:
            if packet[17] == 0: return
        try: tf = Splice(packet[4:])
        except: return
        print(f'SCTE 35 Packet @ \033[92m{self.PTS:.06f}\033[0m')
        tf.show()
        if not self.PID: self.PID = pid
        return
