import sys

from bitn import BitBin
from .cue import Cue
from functools import partial
from .streamtype import stream_type_map


def show_cue(cue):
    cue.show()


class Stream:
    '''
    A Stream class
    With MPEG-TS program awareness.
    Accurate pts for streams with
    more than one program containing
    SCTE-35 streams.

    '''
    cmd_types = [4,5,6,7,255] # splice command types
    packet_size = 188
    def __init__(self, tsdata, show_null = False):
        self.tsdata = tsdata
        if show_null: self.cmd_types.append(0)
        self.scte35_pids = set()
        self.pid_prog = {}
        self.pmt_pids = set()
        self.programs = set()
        self.PTS = {}
        self.info =False
        self.the_program = False

    def find_start(self,pkt):
        '''
        handles partial packets
        '''
        if pkt[0] == 71: return pkt
        sync_byte = b'G'
        while self.tsdata:
            n = self.tsdata.read(1)
            if not n:
                sys.exit()
            if n == sync_byte:
                self.tsdata.read(self.packet_size -1)
                if self.tsdata.read(1) == sync_byte:
                    return sync_byte +self.tsdata.read(self.packet_size -1)
                    
    def decode(self,func = show_cue):
        '''
        reads MPEG-TS to find SCTE-35 packets
        '''
        for pkt in iter(partial(self.tsdata.read, self.packet_size), b''):
            pkt = self.find_start(pkt)
            cue = self.parser(pkt)
            if cue : func(cue)

    def decode_next(self):
        '''
        returns a threefive.Cue instance
        when a SCTE-35 packet is found
        '''
        for pkt in iter(partial(self.tsdata.read, self.packet_size), b''):
            pkt = self.find_start(pkt)
            cue = self.parser(pkt)
            if cue : return cue

    def decode_program(self,the_program,func = show_cue):
        '''
        returns a threefive.Cue instance
        when a SCTE-35 packet is found
        '''
        self.the_program = the_program
        self.decode(func)
            
    def decode_proxy(self,func = show_cue):
        '''
        reads an MPEG-TS stream
        and writes all ts packets to stdout
        and SCTE-35 data to stderr
        '''
        for pkt in iter(partial(self.tsdata.read, self.packet_size), b''):
            pkt = self.find_start(pkt)
            sys.stdout.buffer.write(pkt)
            cue = self.parser(pkt)
            if cue : func(cue)

    def show(self):
        '''
        displays program stream mappings
        '''
        self.info = True
        self.decode()

    def mk_packet_data(self,pid):
        '''
        creates packet_data dict
        to pass to a threefive.Cue instance
        '''
        packet_data = {}
        packet_data['pid'] = pid
        packet_data['program'] = self.pid_prog[pid]
        packet_data['pts']= self.PTS[self.pid_prog[pid]]
        return packet_data

    def pas(self,pkt):
        bitbin = BitBin(pkt[5:])
        bitbin.forward(12)
        section_length = bitbin.asint(12)
        slib = (section_length << 3)
        bitbin.forward(40)
        slib -= 40
        while slib> 40:
            program_number = bitbin.asint(16)
            bitbin.forward(3)
            if program_number == 0:
                bitbin.forward(13)
            else:
                pmap_pid = bitbin.asint(13)
                self.pmt_pids.add(pmap_pid)
            slib -= 32
        bitbin.forward(32)

    def parser(self,pkt):
        '''
        parse pid from pkt and
        route it appropriately
        '''
        pid = self.parse_pid(pkt[1],pkt[2])
        if pid == 0: self.pas(pkt)
        if pid in self.pmt_pids: self.pms(pkt)
        if self.info: return False
        if pid in self.pid_prog.keys(): self.parse_pusi(pkt,pid)
        if pid in self.scte35_pids: return self.parse_scte35(pkt,pid)

    def parse_pid(self,one,two):
         return ((one & 31) << 8 | two)

    def parse_pts(self,pkt,pid):
        '''
        parse pts
        '''
        pts  = ((pkt[13]  >> 1) & 7) << 30
        pts |= (((pkt[14] << 7) | (pkt[15] >> 1)) << 15)
        pts |=  ((pkt[16] << 7) | (pkt[17] >> 1))
        pts /= 90000.0
        ppp = self.pid_prog[pid]
        self.PTS[ppp]=round(pts,6)

    def parse_pusi(self,pkt,pid):
        '''
        used to determine if pts data is available.
        '''
        if (pkt[1] >> 6) & 1 :
            if pkt[6] & 1:
                if (pkt[10] >> 6) & 2:
                    if (pkt[11] >> 6) & 2:
                        if (pkt[13] >> 4) &2:
                            self.parse_pts(pkt,pid)

    def parse_scte35(self,pkt,pid):
        packet_data = self.mk_packet_data(pid)
        # handle older scte-35 packets
        pkt = pkt[:5]+b'\xfc0' +pkt.split(b'\x00\xfc0')[1]
        # check splice command type
        if pkt[18] in self.cmd_types:     
            return Cue(pkt,packet_data)
        
    def parse_stream_type(self,bitbin,program_number):
        '''
        extract stream pid and type
        '''
        stream_type = bitbin.ashex(8) # 8
        bitbin.forward(3) # 11
        el_PID = bitbin.asint(13) # 24
        bitbin.forward(4) # 28
        eilib = bitbin.asint(12) <<3 # 40
        bitbin.forward(eilib)
        minus = 40 + eilib
        return minus,[stream_type,el_PID]

    def parse_program_streams(self,slib,bitbin,program_number):
        '''
        parse the elementary streams
        from a program
        '''
        pstreams=[]
        while slib > 32:
            minus,pstream = self.parse_stream_type(bitbin,program_number)
            slib -= minus
            pstreams.append(pstream)
        if program_number not in self.programs:
            self.programs.add(program_number)
            if self.info:
                self.show_program_streams(program_number,pstreams)       
            for s in pstreams:
                self.pid_prog[s[1]]=program_number
                if s[0] == '0x86':
                    self.scte35_pids.add(s[1])
        else:
            if self.info:
                sys.exit()

    def show_program_streams(self,program_number,pstreams):
        print(f'\nProgram: {program_number}')
        for s in pstreams:
            st = f'[{s[0]}] Reserved or Private'
            if s[0] in stream_type_map.keys():
                st =f'[{s[0]}] {stream_type_map[s[0]]}'
            print(f'\t   {s[1]}: {st}')

    def pms(self,pkt):
        bitbin = BitBin(pkt[5:])
        bitbin.forward(9)
        if bitbin.asflag(1):
            return
        bitbin.forward(2)
        slib = bitbin.asint(12) << 3
        program_number = bitbin.asint(16)
        if self.the_program and (program_number != self.the_program):
            return
        #pcr_pid = bitbin.asint(13)
        bitbin.forward(44)
        pilib = (bitbin.asint(12) << 3)
        slib -= 72
        slib -= pilib # Skip descriptors
        bitbin.forward(pilib) # Skip descriptors
        self.parse_program_streams(slib,bitbin,program_number)
