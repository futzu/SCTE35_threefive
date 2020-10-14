import sys
from bitn import BitBin
from .cue import Cue
from functools import partial


class Stream:
    '''
    threefive.Stream(tsdata, show_null = False)
    Fast parse mpegts files and streams
    for SCTE 35 packets
    
    tsdata should be a _io.BufferedReader instance:
    example:
        import threefive
        with open('vid.ts','rb') as tsdata:
            threefive.Stream(tsdata)
            
    SCTE-35 Splice null packets are ignored by default. 
    Set show_null = True to show splice null. 

    '''
    no_pts_stream_ids = [188, 190, 191, 240, 241, 242, 248]
    cmd_types = [4,5,6,7,255] # splice command types
    packet_size = 188
    
    def __init__(self, tsdata, show_null = False):
        # set show_null to parse splice null packets
        if show_null:
            self.cmd_types.append(0)
        self.tsdata = tsdata
        self.PTS = False
        self.until_found = False

    def decode(self):
        '''
        StreamPlus.decode() reads MPEG-TS
        to find SCTE-35 packets.
        ''' 
        for packet in iter( partial(self.tsdata.read, self.packet_size), b''):
            # parse all packets headers first
            self.parse_header(packet) 
            if self.chk_magic(packet):
                cuep = Cue(packet,self.packet_data)                            
                if self.until_found:
                    return cuep
                cuep.show()

    def decode_until_found(self):
        '''
        Stream.decode_until_found() reads MPEG-TS
        to find a SCTE-35 packet and returns the packet
        when found.
        ''' 
        self.until_found = True
        cuep = self.decode()
        if cuep:
            return cuep
        return False

    def proxy(self,func = None):
        '''
        StreamProxy.decode() reads MPEG-TS
        writes all packets to sys.stdout.
        writes scte35 data to sys.stderr.
        The optional func arg allows a function
        to be used for custom handling of the SCTE-35
        cue instance.
        the function should match the interface
            func(cuep)
        Where cuep is an instance of threefive.Cue
        If func is not set, threefive.Cue.show() is called.
        '''
        for packet in iter( partial(self.tsdata.read, self.packet_size), b''):
            # Write every packet to stdout
            sys.stdout.buffer.write(packet)
            self.parse_header(packet) 
            if self.chk_magic(packet):
                cuep = Cue(packet,self.packet_data)
                if not func:
                    sys.stderr.buffer.write(cuep.get())
                else:
                    func(cuep)
                    
    def chk_magic(self,packet):
        '''
        Stream.chk_magic(packet)
        does fast SCTE-35 packet detection
        '''
        if packet[0] == 0x47:
            if packet[5] == 0xfc:
                if packet[6] == 48: 
                    if packet[8] == 0:
                        if packet[15] == 255:
                            return packet[18] in self.cmd_types
            
    def parse_header(self,packet):
        '''
        Stream.parse_header(packet)
        reads a MPEG-TS packet header
        for pid and/or pusi.
        '''
        # tei = packet[1] >> 7
        pusi = packet[1] >> 6 & 1
        if pusi:
            pusidata = packet[4:20]
            self.parse_pusi(pusidata)
        # ts_priority = packet[1] >>5 & 0x1
        pid = (packet[1] & 31) << 8
        pid += packet[2]
        # scramble = packet[2] >>6
        # afc = (packet[2] & 48) >> 4
        # count = packet[2] & 15
        self.packet_data = {'pid':pid,'pts':self.PTS}
      
    def parse_pts(self,bitbin):
        '''
        Stream.parse_pts(bitbin)
        This is the process described in the official
        Mpeg-ts specification.
        '''
        a = bitbin.asint(3) << 30
        bitbin.forward(1)          
        b = bitbin.asint(15) << 15
        bitbin.forward(1)          
        c = bitbin.asint(15)
        d = (a+b+c)/90000.0
        # self.PTS is updated when we find a pts.
        self.PTS=round(d,6)
    
    def parse_pusi(self, pusidata):
        '''
        Stream.parse_pusi(pusidata)
        If the pusi data contains these markers,
        we can pull a PTS value..
        '''
        if pusidata[2] == 1: 
            if pusidata[3] not in self.no_pts_stream_ids:
                if (pusidata[6] >> 6) == 2:
                    if (pusidata[7] >> 6) == 2:
                        if (pusidata[9] >> 4) == 2:
                            bitbin = BitBin(pusidata[9:])
                            bitbin.forward(4)
                            self.parse_pts(bitbin)
