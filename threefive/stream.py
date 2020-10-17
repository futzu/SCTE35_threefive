import sys
from functools import partial
from .cue import Cue


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
    cmd_types = [4,5,6,7,255] # splice command types
    packet_size = 188
    
    def __init__(self, tsdata, show_null = False):
        # set show_null to parse splice null packets
        if show_null: self.cmd_types.append(0)
        self.tsdata = tsdata
        self.until_found = False
        
    def chk_scte35(self,pkt):
        '''
        Fast SCTE-35 packet detection
        '''
        if pkt[5] == 0xfc: # table id
            if pkt[6] == 48: # byte value
                if pkt[8] == 0: # protocol version
                    if pkt[15] == 255: # cw_index
                        return pkt[18] in self.cmd_types 

    def get_pid(self,byte1,byte2):
        '''
        Parse pid from byte[1] and byte[2]
        of an MPEG-TS packet
        '''
        # read last 5 bits of byte1 and left shift 8 
        five_bits = (byte1 & 31) << 8
        return five_bits + byte2 # pid
                    
    def decode(self):
        '''
        Stream.decode() reads MPEG-TS
        to find SCTE-35 packets.
        ''' 
        for pkt in iter( partial(self.tsdata.read, self.packet_size), b''):
            if self.chk_scte35(pkt):
                pid = self.get_pid(pkt[1],pkt[2])
                cue = Cue(pkt,{'pid':pid})
                if self.until_found: return cue
                cue.show()
            
    def decode_until_found(self):
        '''
        Stream.decode_until_found() reads MPEG-TS
        to find a SCTE-35 packet and returns the packet
        when found.
        ''' 
        self.until_found = True
        cue = self.decode()
        if cue: return cue

    def proxy(self,func = None):
        '''
        Stream.proxy(func = None) reads MPEG-TS
        writes all packets to sys.stdout.
        writes scte35 data to sys.stderr.
        The optional func arg allows a function
        to be used for custom handling of the SCTE-35
        cue instance.
        the function should match the interface
            func(cue)
        Where cue is an instance of threefive.Cue
        If func is not set, threefive.Cue.show() is called.
        '''        
        for pkt in iter( partial(self.tsdata.read, self.packet_size), b''):
            sys.stdout.buffer.write(pkt)
            if self.chk_scte35(pkt):
                pid = self.get_pid(pkt[1],pkt[2])
                cue = Cue(pkt,{'pid':pid})
                if not func:
                    sys.stderr.buffer.write(cue.get())
                else:
                    func(cue)
