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

    def __init__(self, tsfile=None, tsstream=None, show_null=False):
        self.PID = False
        self.show_null = show_null
        self.tf = False
        self.fpts = None
        if tsfile:
            self.parse_tsfile(tsfile)
        if tsstream:
            self.parse_tsdata(tsstream)

    def parse_tsfile(self, tsfile):
        with open(tsfile, 'rb') as tsdata:
            self.parse_tsdata(tsdata)

    def parse_tsdata(self, tsdata):
        while tsdata:
            packets = tsdata.read(self.PACKET_SIZE * 5)
            if not packets:
                break
            while packets:
                p, packets = packets[:188], packets[188:]
                if p[0] == self.SYNCBYTE:
                    self.parse_tspacket(p[1:])

    def parse_pusi(self, packet):
        bitbin = BitBin(packet)
        if bitbin.asint(24) == 1 and bitbin.asint(8) not in self.NON_PTS_STREAM_IDS:
            # PES_packet_length =
            bitbin.forward(16)
            if bitbin.asint(2) == 2:
                bitbin.forward(6)
                '''
                PES_scramble_control = bitbin.asint(2)
                PES_priority = bitbin.asint(1)
                data_align_ind = bitbin.asint(1)
                copyright = bitbin.asint(1)
                orig_or_copy = bitbin.asint(1)
                '''
                if bitbin.asint(2) == 2:
                    bitbin.forward(14)
                    if bitbin.asint(4) == 2:
                        a = bitbin.asint(3) << 30
                        bitbin.asflag(1)
                        b = bitbin.asint(15) << 15
                        bitbin.asflag(1)
                        c = bitbin.asint(15)
                        d = (a+b+c)/90000.0
                        self.fpts = f'PTS \033[92m{d:.3f}\033[0m '
                        print(f'\r{self.fpts}', end="\r")

    def parse_tspacket(self, packet):
        two_bytes = unpack('>H', packet[:2])[0]
       # tei = two_bytes >> 15
        pusi = two_bytes >> 14 & 0x1
        #ts_priority = two_bytes >>13 & 0x1
        pid = two_bytes & 0x1fff
        #scramble = one_byte >>6
        #afc = (one_byte & 48) >> 4
        #count = one_byte & 15
        if pid == 101:
            return
        if pusi:
            self.parse_pusi(packet[3:19])
        if packet[4] != 0xfc:
            return
        if not self.show_null:
            if packet[17] == 0:
                return
        if self.PID and (pid != self.PID):
            return
        try:
            self.tf = Splice(packet[4:])
        except:
            return
        print()
        # print(f'\r{self.fpts}', end = "\r")
        self.tf.show()
        if not self.PID:
            self.PID = pid
        return
