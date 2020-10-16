from bitn import BitBin

from .cue import Cue


class Header:
    '''
    The packet.Header class
    parses MPEG-TS packet header values.
    Packet.parse_header() creates an instance
    of Header as packet.header
    '''
    def __init__(self,four_bytes):
        self.tei = four_bytes[1] >> 7
        self.pusi = (four_bytes[1] >> 6) & 1
        self.ts_priority = (four_bytes[1] >> 5) & 1
        self.pid = (four_bytes[1] & 31) << 8
        self.pid += four_bytes[2]
        self.scramble = four_bytes[3] >> 6
        self.atc = (four_bytes[3] >> 4) & 3
        self.con_counter = four_bytes[3] & 15

    def __repr__(self):
        return str(self.get())

    def get(self):
        return vars(self)

        
class Packet:
    '''
    packet.Packet(raw)
    requires a 188 byte MPEG-TS packet as raw

    '''
    no_pts_stream_ids = [188, 190, 191, 240, 241, 242, 248]

    def __init__(self,raw):
        self.raw = raw
        self.header = False

    def parse_header(self):
        '''
        Packet.parse_header()
        creates an instance of Header
        as Packet.header
        if Packet.header doesn't exist.
        '''
        if not self.header:
            self.header = Header(self.raw[0:4])
                    
    def parse_scte35(self):
        '''
        Packet.parse_scte35()
        does fast SCTE-35 packet detection
        and returns splice command type
        as the int Packet.scte35_cmd or -1
        if SCTE-35 data is not found.
        '''
        self.scte35_cmd = -1
        if self.raw[5] == 0xfc:
            if self.raw[6] == 48: 
                if self.raw[8] == 0:
                    if self.raw[15] == 255:
                        self.scte35_cmd = self.raw[18]
        if self.scte35_cmd > -1:
            self.parse_header()
            self.cue = Cue(self.raw,vars(self.header))
        return self.scte35_cmd

    def parse_pusi(self):
        '''
        Packet.parse_pusi()
        If the pusi data contains these markers,
        we can pull a PTS value..
        '''
        self.parse_header()
        if self.header.pusi == 0: return False
        pusidata = self.raw[4:20]
        if pusidata[2] == 1: 
            if pusidata[3] not in self.no_pts_stream_ids:
                if (pusidata[6] >> 6) == 2:
                    if (pusidata[7] >> 6) == 2:
                        return (pusidata[9] >> 4) == 2
   
    def parse_pts(self):
        '''
        Packet.parse_pts(bitbin)
        This is the process described in the official
        Mpeg-ts specification.
        '''
        if self.parse_pusi():
            bitbin = BitBin(self.raw[13:20])
            bitbin.forward(4)
            a = bitbin.asint(3) << 30
            bitbin.forward(1)          
            b = bitbin.asint(15) << 15
            bitbin.forward(1)          
            c = bitbin.asint(15)
            d = (a+b+c)/90000.0
            # self.header.pts is updated when we find a pts.
            self.header.pts=round(d,6)
            return self.header.pts

    def __repr__(self):
        return str(self.get())

    def get(self):
        return vars(self)

    
