import sys

from bitn import BitBin
from .cue import Cue
from functools import partial
from .streamtype import stream_type_map


def show_cue(cue):
    cue.show()


class Stream:
    '''
    Stream class
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

    def find_start(self):
        '''
        handles partial packets
        '''
        pkt= self.tsdata.read(self.packet_size)
        if pkt[0] == 71: return
        sync_byte = b'G'
        while self.tsdata:
            n = self.tsdata.read(1)
            if not n: sys.exit()
            if n == sync_byte:
                self.tsdata.read(self.packet_size -1)
                if self.tsdata.read(1) == sync_byte:
                    self.tsdata.read(self.packet_size -1)
                    return
                
    def decode(self,func = show_cue):
        '''
        reads MPEG-TS to find SCTE-35 packets
        '''
        self.find_start()
        for pkt in iter(partial(self.tsdata.read, self.packet_size), b''):
             cue = self.parser(pkt)
             if cue : func(cue)
            

    def decode_next(self):
        '''
        returns a threefive.Cue instance
        when a SCTE-35 packet is found
        '''
        self.find_start()
        for pkt in iter(partial(self.tsdata.read, self.packet_size), b''):
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
        self.find_start()
        for pkt in iter(partial(self.tsdata.read, self.packet_size), b''):
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
        prgm = self.pid_prog[pid]
        packet_data['program'] = prgm
        packet_data['pts'] = round(self.PTS[prgm],6)
        return packet_data

    def program_association_table(self,pkt):
        sectionlen =(pkt[6] & 15 << 8) | pkt[7]
        pkt = pkt[13:sectionlen + 5]
        bitbin = BitBin(pkt)
        slib = sectionlen <<3
        slib -= 40
        while slib> 32:
            program_number = bitbin.asint(16)
            bitbin.forward(3)
            if program_number == 0:
                bitbin.forward(13)
            else:
                self.pmt_pids.add(bitbin.asint(13))
            slib -= 32
        bitbin.forward(32)

    def parser(self,pkt):
        '''
        parse pid from pkt and
        route it appropriately
        '''
        pid =(pkt[1]& 31) << 8 | pkt[2]
        if pid == 0:
            self.program_association_table(pkt)
        if pid in self.pmt_pids:
            self.program_map_section(pkt)
        if self.info:
            return
        if pid in self.scte35_pids:
            return self.parse_scte35(pkt,pid)
        
        if pid in self.pid_prog.keys():
            if (pkt[1] >> 6) & 1 :
                pkt = pkt[0:18]
                self.parse_pusi(pkt,pid)
                return
        
        
    def parse_pts(self,pkt,pid):
        '''
        parse pts
        '''

        pts  = ((pkt[13]  >> 1) & 7) << 30
        pts |= (((pkt[14] << 7) | (pkt[15] >> 1)) << 15)
        pts |=  ((pkt[16] << 7) | (pkt[17] >> 1))
        pts /= 90000.0
        ppp = self.pid_prog[pid]
        self.PTS[ppp]=pts

    def parse_pusi(self,pkt,pid):
        '''
        used to determine if pts data is available.
        '''
        if pkt[6] & 1:
            if (pkt[10] >> 6) & 2:
                if (pkt[11] >> 6) & 2:
                    if (pkt[13] >> 4) in [2]:
                        self.parse_pts(pkt,pid)

    def parse_scte35(self,pkt,pid):
        packet_data = self.mk_packet_data(pid)
        # handle older scte-35 packets
        try:
            pkt = pkt[:5]+b'\xfc0' +pkt.split(b'\x00\xfc0')[1]
        except:
            print(pkt)
        # check splice command type
        if pkt[18] in self.cmd_types:     
            return Cue(pkt,packet_data)
        
    def parse_stream_type(self,bitbin):
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
        if program_number not in self.programs:
            self.programs.add(program_number)
            if self.info:
                print(f'\nProgram: {program_number}')    
            while slib > 32:
                minus,pstream = self.parse_stream_type(bitbin)
                slib -= minus
                stream_type = pstream[0]
                pid = pstream[1]
                self.pid_prog[pid] = program_number
                if self.info:
                    self.show_program_stream(pid,stream_type)  
                if stream_type == '0x86':
                    self.scte35_pids.add(pid)
        else:
            if self.info:
                sys.exit()

    def show_program_stream(self,pid,stream_type):
        streaminfo = f'[{stream_type}] Reserved or Private'
        if stream_type in stream_type_map.keys():
            streaminfo =f'[{stream_type}] {stream_type_map[stream_type]}'
        print(f'\t   {pid}: {streaminfo}')

    def program_map_section(self,pkt):
        #table_id = pkt[5]
        sectioninfolen = (pkt[6] & 15 << 8) | pkt[7]
        slib = sectioninfolen << 3
        program_number = (pkt[8] << 8) | pkt[9]
        #version = pkt[10] >> 1 & 31
        #current_next = pkt[10] & 1
        if self.the_program and (program_number != self.the_program):
            return
        #section_number = pkt[11]
        #last_section_number = pkt[12]
        #pcr_pid = (pkt[13]& 31) << 8 | pkt[14]
        proginfolen = (pkt[15] & 15 << 8) | pkt[16]
        pkt = pkt[17+proginfolen:slib+9]
        bitbin =BitBin(pkt)
        pilib= proginfolen << 3
        slib -= 72
        slib -= pilib # Skip descriptors
        self.parse_program_streams(slib,bitbin,program_number)
