import sys

from functools import partial
from .cue import Cue


def show_cue(cue):
    cue.show()

class Stream:
    '''
    threefive.Stream(tsdata, show_null = False)
    fast mpegts stream parsing for SCTE 35 packets.
    
    tsdata should be a _io.BufferedReader instance.
    show_null = True to parse splice null packets

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
        if show_null: self.cmd_types.append(0)
        self.tsdata = tsdata
        self.PTS = None
        self.packet_data = {}
        
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
  
    def decode(self,func = show_cue):
        '''
        Stream.decode() reads MPEG-TS
        to find SCTE-35 packets.
        ''' 
        for pkt in iter( partial(self.tsdata.read, self.packet_size), b''):
            self.parse_header(pkt)
            if self.chk_scte35(pkt):
                func(Cue(pkt,self.packet_data))
            
    def decode_pid(self,the_pid, func = show_cue):
        '''
        Stream.decode_pid() reads MPEG_TS
        to find SCTE-35 packets by the_pid.
        '''
        for pkt in iter( partial(self.tsdata.read, self.packet_size), b''):
            self.parse_header(pkt)
            if self.packet_data['pid'] == the_pid:
                func(Cue(pkt,packet_data))

    def decode_proxy(self,func = show_cue):
        '''
        Stream.decode_proxy() reads an MPEG-TS stream
        and writes all ts packets to stdout
        and SCTE-35 data to stderr. 
        '''        
        for pkt in iter( partial(self.tsdata.read, self.packet_size), b''):
            sys.stdout.buffer.write(pkt)
            self.parse_header(pkt)
            if self.chk_scte35(pkt):
                func(Cue(pkt,self.packet_data))

    def decode_next(self):
        '''
        Stream.decode_next() returns a threefive.Cue instance
        when a SCTE-35 packet is found
        '''
        for pkt in iter( partial(self.tsdata.read, self.packet_size), b''):
            self.parse_header(pkt)
            if self.chk_scte35(pkt):
                return Cue(pkt,self.packet_data)
    
    def parse_header(self,pkt):
        '''
        Stream.parse_header(pkt) parses the MPEG-TS packet header.
        '''
        self.packet_data = {}
        self.parse_pid(pkt[1],pkt[2])
        if (pkt[1] >> 6) & 1 :
            self.parse_pusi(pkt[4:18])
        self.packet_data['pts'] = self.PTS

    def parse_pid(self,byte1,byte2):
        '''
        Stream.parse_pid(byte1,byte2)
        uses byte1 and byte2 to determine
        the pid of the packet.
        '''
        self.packet_data['pid'] = ((byte1 & 31) << 8) + byte2 

    def parse_pts(self,pdata):
        '''
        Stream.parse_pts(pdata) parses pts from pdata.  
        '''
        pts  = ((pdata[9] >> 1) & 7) << 30
        pts += (((pdata[10] << 7) + (pdata[11] >> 1)) << 15)
        pts += (pdata[12] << 7) + (pdata[13] >> 1)
        pts /= 90000.0 
        self.PTS=round(pts,6)
        
    def parse_pusi(self, pdata):
        '''
        Stream.parse_pusi(pdata) is used to determine
        if pts data is available.
        '''
        if pdata[2] & 1: 
            if (pdata[6] >> 6) & 2: 
                if (pdata[7] >> 6) & 2:
                    if (pdata[9] >> 4) &2:
                        self.parse_pts(pdata)
