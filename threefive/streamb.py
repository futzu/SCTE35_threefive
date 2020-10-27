import sys

from bitn import BitBin
from .cue import Cue
from functools import partial
from .streamtype import stream_type_map


def show_cue(cue):
    cue.show()


class StreamB:
    '''
    streamb.StreamB(tsdata)

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
        self.pids=set()

    def find_start(self,pkt):
        if pkt[0] == 71: return pkt
        start=False
        sync_byte = b'G'
        while start != sync_byte:
            n = self.tsdata.read(1)
            if n == sync_byte:
                self.tsdata.read(187)
                if self.tsdata.read(1) == sync_byte:
                    return sync_byte +self.tsdata.read(187)
                    
    def decode(self,func = show_cue):
        '''
        reads MPEG-TS to find SCTE-35 packets
        '''
        for pkt in iter( partial(self.tsdata.read, self.packet_size), b''):
            pkt = self.find_start(pkt)
            cue = self.parser(pkt)
            if cue : func(cue)

    def decode_next(self):
        '''
        returns a threefive.Cue instance
        when a SCTE-35 packet is found
        '''
        for pkt in iter( partial(self.tsdata.read, self.packet_size), b''):
            pkt = self.find_start(pkt)
            cue = self.parser(pkt)
            if cue : return cue

    def decode_proxy(self,func = show_cue):
        '''
        reads an MPEG-TS stream
        and writes all ts packets to stdout
        and SCTE-35 data to stderr
        '''
        for pkt in iter( partial(self.tsdata.read, self.packet_size), b''):
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

    def pas(self,bitbin):
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
        pid = ((pkt[1] & 31) << 8 | pkt[2])
        self.pids.add(pid)
        if pid == 0:
            bitbin = BitBin(pkt[5:])
            self.pas(bitbin)
        if pid in self.pmt_pids:
            bitbin = BitBin(pkt[5:])
            self.pms(bitbin)
        if self.info:
            return False
        if pid in self.pid_prog.keys():
            if (pkt[1] >> 6) & 1 :
                self.parse_pusi(pkt[4:18],pid)
        if pid in self.scte35_pids:
            packet_data = self.mk_packet_data(pid)
            return Cue(pkt,packet_data)

    def parse_pts(self,pdata,pid):
        '''
        parse pts
        '''
        pts  = ((pdata[9]  >> 1) & 7) << 30
        pts |= (((pdata[10] << 7) | (pdata[11] >> 1)) << 15)
        pts |=  ((pdata[12] << 7) | (pdata[13] >> 1))
        pts /= 90000.0
        ppp = self.pid_prog[pid]
        self.PTS[ppp]=round(pts,6)

    def parse_pusi(self,pdata,pid):
        '''
        used to determine if pts data is available.
        '''
        if pdata[2] & 1:
            if (pdata[6] >> 6) & 2:
                if (pdata[7] >> 6) & 2:
                    if (pdata[9] >> 4) &2:
                        self.parse_pts(pdata,pid)

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

    def parse_program_streams(self,slib,bitbin,program_number,pcr_pid):
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
                print(f'\nProgram: {program_number} (pcr pid: {pcr_pid})')
            for s in pstreams:
                self.pid_prog[s[1]]=program_number
                if s[0] == '0x86':
                    self.scte35_pids.add(s[1])
                if self.info:
                    st = f'[{s[0]}] Reserved or Private'
                    if s[0] in stream_type_map.keys():
                        st =f'[{s[0]}] {stream_type_map[s[0]]}'
                    print(f'\t   {s[1]}: {st}')
        else:
            if self.info:
                sys.exit()

    def pms(self,bitbin):
        bitbin.forward(9)
        if bitbin.asflag(1):
            return
        bitbin.forward(2)
        slib = bitbin.asint(12) << 3
        program_number = bitbin.asint(16) # 16
        bitbin.forward(27) # 60
        pcr_pid = bitbin.asint(13)
        bitbin.forward(4)
        pilib = (bitbin.asint(12) << 3) # 72
        slib -= 72
        slib -= pilib # Skip descriptors
        bitbin.forward(pilib) # Skip descriptors
        self.parse_program_streams(slib,bitbin,program_number,pcr_pid)
