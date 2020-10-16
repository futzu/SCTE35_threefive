import sys
from functools import partial
from .packet import Packet


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
    cmd_types = [0,4,5,6,7,255] # splice command types
    packet_size = 188
    
    def __init__(self, tsdata, show_null = False):
        # set show_null to parse splice null packets
        if show_null: self.cmd_types.append(0)
        self.tsdata = tsdata
        self.until_found = False

    def decode(self):
        '''
        StreamPlus.decode() reads MPEG-TS
        to find SCTE-35 packets.
        ''' 
        for pkt in iter( partial(self.tsdata.read, self.packet_size), b''):
            packet = Packet(pkt)
            if packet.parse_scte35() in self.cmd_types:
                if self.until_found: return packet.cue
                packet.cue.show()
            
    def decode_until_found(self):
        '''
        Stream.decode_until_found() reads MPEG-TS
        to find a SCTE-35 packet and returns the packet
        when found.
        ''' 
        self.until_found = True
        pcue = self.decode()
        if pcue: return pcue
        return False

    def proxy(self,func = None):
        '''
        Stream.proxy(func = None) reads MPEG-TS
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
        for pkt in iter( partial(self.tsdata.read, self.packet_size), b''):
            sys.stdout.buffer.write(pkt)
            packet = Packet(pkt)
            if packet.parse_scte35() in self.cmd_types:  
                if not func:
                    sys.stderr.buffer.write(packet.cue.get())
                else:
                    func(packet.cue)
