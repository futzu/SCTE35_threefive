import json
import sys

from functools import partial
from .cue import Cue


class Stream:
    '''
    threefive.Stream(tsdata, show_null = False)
    fast mpegts stream parsing for SCTE 35 packets.
    
    Example:
        import threefive
        with open('vid.ts','rb') as tsdata:
            st =threefive.Stream(tsdata)
            st.decode()
    '''
    no_pts_stream_ids = [188, 190, 191, 240, 241, 242, 248]
    cmd_types = [4,5,6,7,255] # splice command types
    packet_size = 188
    def __init__(self, tsdata, show_null = False):
        '''
        Stream.__init__(tsdata, show_null = False)
        tsdata should be a _io.BufferedReader instance:
        show_null = True to parse splice null packets
        '''
        if show_null: self.cmd_types.append(0)
        self.tsdata = tsdata
        self.until_found = False
        self.PTS = None
        
    def chk_scte35(self,pkt):
        '''
        Stream.chk_scte35(pkt) is
        fast SCTE-35 packet detection.
        '''
        if pkt[5] == 0xfc: # table id
            if pkt[6] == 48: # byte value
                if pkt[8] == 0: # protocol version
                    if pkt[15] == 255: # cw_index
                        return pkt[18] in self.cmd_types

    def decode(self):
        '''
        Stream.decode() reads MPEG-TS
        to find SCTE-35 packets.
        ''' 
        for pkt in iter( partial(self.tsdata.read, self.packet_size), b''):
            packet_data = self.parse_header(pkt)
            if self.chk_scte35(pkt):
                cue = Cue(pkt,packet_data)
                if self.until_found: return cue
                cue.show()

    def decode_fast(self):
        '''
        Stream.decode_fast() reads MPEG_TS
        to find SCTE-35 packets.
        pid and pts are not parsed.
        '''
        for pkt in iter( partial(self.tsdata.read, self.packet_size), b''):
            if self.chk_scte35(pkt):
                cue = Cue(pkt)
                cue.show()

    def decode_until_found(self):
        '''
        Stream.decode_until_found()
        reads MPEG-TS to find a SCTE-35 packet
        and returns the packet when found.
        ''' 
        self.until_found = True
        cue = self.decode()
        if cue: return cue

    def parse_header(self,pkt):
        '''
        Stream.parse_header(pkt) parses the MPEG-TS packet header.
        '''
        packet_data = {}
        if (pkt[1] >> 6) & 1 : self.parse_pusi(pkt[4:])
        packet_data['pid'] = ((pkt[1] & 31) << 8) + pkt[2] 
        packet_data['pts'] = self.PTS
        return packet_data
                        
    def parse_pts(self,bites):
        '''
        Stream.parse_pts(bites) parses pts from bites.  
        '''
        pts  =  ((bites[0] >> 1) & 7) << 30
        pts += (((bites[1] << 7) + (bites[2] >> 1)) <<15)
        pts +=   (bites[3] << 7) + (bites[4] >> 1) 
        pts /= 90000.0
        self.PTS=round(pts,6)
      
    def parse_pusi(self, pdata):
        '''
        Stream.parse_pusi(pdata) is used to determine
        if pts data is available in the packet.
        '''
        if pdata[2] == 1: 
            if pdata[3] not in self.no_pts_stream_ids:  
                if (pdata[6] >> 6) == 2: 
                    if (pdata[7] >> 6) == 2:
                        if (pdata[9] >> 4) == 2: 
                            self.parse_pts(pdata[9:])
                            
    def proxy(self,func = None):
        '''
        Stream.proxy(func = None) reads MPEG-TS
        writes all packets to sys.stdout and scte35 data to sys.stderr.
        The optional func arg allows a function
        the function should match the interface func(cue)
        Where cue is an instance of threefive.Cue
        If func is not set, threefive.Cue.get() is printed to stderr.
        '''        
        for pkt in iter( partial(self.tsdata.read, self.packet_size), b''):
            sys.stdout.buffer.write(pkt)
            if self.chk_scte35(pkt):
                packet_data = self.parse_header(pkt)
                cue = Cue(pkt,packet_data)
                if not func:
                    print(f'\033[92m{json.dumps(cue.get(),indent=2)}\033[00m', file=sys.stderr)
                else:
                    func(cue)
