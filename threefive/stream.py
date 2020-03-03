from .splice import Splice
from bitn import BitBin
from struct import unpack
from .afc import adaptation_fields

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
        self.show_null = show_null
        self.tf = False
        if tsfile: self.parse_tsfile(tsfile)
        if tsstream: self.parse_tsdata(tsstream)

    def parse_tsfile(self, tsfile):
        with open(tsfile, 'rb') as tsdata:
            self.parse_tsdata(tsdata)

    def parse_tsdata(self, tsdata):
        while tsdata:
            packets = tsdata.read(self.PACKET_SIZE * 3)
            if not packets: break
            while packets:
                p, packets = packets[:188], packets[188:]
                if p[0] != self.SYNCBYTE: return
                self.parse_tspacket(p[1:])

    def parse_pusi(self, packet):
        bitbin = BitBin(packet)
        if bitbin.asint(24) != 1: return
        if bitbin.asint(8) in self.NON_PTS_STREAM_IDS: return
        # PES_packet_length =
        bitbin.forward(16)
        if bitbin.asint(2) != 2: return
        bitbin.forward(6)
        '''
        PES_scramble_control = bitbin.asint(2)
        PES_priority = bitbin.asint(1)
        data_align_ind = bitbin.asint(1)
        copyright = bitbin.asint(1)
        orig_or_copy = bitbin.asint(1)
        '''
        if bitbin.asint(2) != 2: return
        bitbin.forward(14)
        if bitbin.asint(4) != 2: return
        a = bitbin.asint(3) << 30
        bitbin.forward(1)
        b = bitbin.asint(15) << 15
        bitbin.forward(1)
        c = bitbin.asint(15)
        d = (a+b+c)/90000.0
        fpts = f'PTS \033[92m{d:.3f}\033[0m '
        print(f'\r{fpts}', end="\r")
        return

    def parse_tspacket(self, packet):
        two_bytes,one_byte = unpack('>HB', packet[:3])
        # tei = two_bytes >> 15
        pusi = two_bytes >> 14 & 0x1
        # ts_priority = two_bytes >>13 & 0x1
        pid = two_bytes & 0x1fff
        # scramble = one_byte >>6
        afc = (one_byte & 48) >> 4
        # count = 0
        if afc in [2,3]:
            afcl=unpack('>B',packet[4:5])[0]
            afcl += 12
            fu = packet[4:afcl]
            bitbin = BitBin(fu)
            adaptation_fields(bitbin)
            return
        # No PTS times in pid 101
        if pid == 101: return
        # Here's where you find PTS
        if pusi: self.parse_pusi(packet[3:19])
        # SCTE35_TID (0xfc) is required .
        if packet[4] != self.SCTE35_TID: return
        #  If the SCTE 35 pid is known, the packet pid must match.
        if self.PID and (pid != self.PID): return
        #  Only show splice_null commands if self.show_null is True
        if not self.show_null:
            if packet[17] == 0: return
        try: tf = Splice(packet[4:])
        except: return
        print()
        tf.show()
        if not self.PID: self.PID = pid
        return
