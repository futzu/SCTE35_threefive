from .splice import Splice
from bitn import BitBin
from multiprocessing import Pool


class Stream:
    '''
    threefive.Decode uses a threefive.Stream instance to handle files and streams. 
    On creation, threefive.Stream parses mpegts for SCTE 35 packets. 
    For each packet, a threefive.Splice instance is created to parse the packet payload.
    threefive.Stream stores splices instances in a list, threefive.Stream.splices.
    '''
    
    PACKET_SIZE = 188
    SYNC_BYTE = b"\x47"
    SCTE35_TID = 0xFC
    
    def __init__(self, tsfile=None, tsstream=None, show_null=False):
        self.splices = []
        self.PID = False
        self.show_null = show_null
        if tsfile:
            self.parse_tsfile(tsfile)
        if tsstream:
            self.parse_tsdata(tsstream)

    def parse_tsfile(self, tsfile):
        with open(tsfile, "rb") as tsdata:
            self.parse_tsdata(tsdata)

    def parse_tsdata(self, tsdata):
        while tsdata:
            if tsdata.read(1) == self.SYNC_BYTE:
                packet = tsdata.read(self.PACKET_SIZE - 1)
                if packet:
                    self.parse_tspacket(packet)
                else:
                    break
            else:
                return

    def parse_tspacket(self, packet):
        if packet[4] != self.SCTE35_TID:
            return
        three_bytes = BitBin(packet[:3])
        tei = three_bytes.asflag(1)
        pusi = three_bytes.asflag(1)
        ts_priority = three_bytes.asflag(1)
        pid = three_bytes.asint(13)
        if self.PID and (pid != self.PID):
            return
        scramble = three_bytes.asint(2)
        afc = three_bytes.asint(2)
        count = three_bytes.asint(4)
        cue = packet[4:]
        try:
            tf = Splice(cue)
        except BaseException:
            return
        if not self.PID:
            self.PID = pid
        if not self.show_null and (cue[13] == 0):
            return
        tf.show()
        self.splices.append(tf)
        return

    def show(self):
        for s in self.splices:
            print(f"\n[ Splice {self.splices.index(s)} ]")
            s.show()
