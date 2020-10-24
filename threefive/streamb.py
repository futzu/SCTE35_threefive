import sys

from bitn import BitBin
from .cue import Cue
from functools import partial

 
class StreamB:
    '''
    streamb.StreamB(tsdata)

    This is a very rough draft,
    don't expect it to all work.
    
    The Stream class
    With MPEG-TS program awareness.
    Accurate pts for streams with
    more than one program containing
    SCTE-35 streams.

    '''
    def __init__(self,tsdata):
        self.tsdata = tsdata
        self.scte35_pids = []
        self.pid_prog = {}
        self.pmt_pids = set()
        self.called_pas = False
        self.PTS = {}
        
    def decode(self):
        for pkt in iter( partial(self.tsdata.read, 188), b''):
            self.parser(pkt)
        print(self.pid_prog)
            
    def pms(self,bitbin,pid):
        bitbin.forward(9)
        if bitbin.asflag(1):
            return
        bitbin.forward(14)
        program_number = bitbin.asint(16)
        bitbin.forward(44)
        program_info_length = bitbin.asint(12)
        N = (program_info_length << 3)
        while N > 32:
            descriptor_tag = bitbin.asint(8)
            N -= 8 
            if descriptor_tag == 5:
                descriptor_length = bitbin.asint(8)
                N -= 8
                # identifier =bitbin.asint(descriptor_length*8)
                bitbin.forward(descriptor_length << 3)
                N -= (descriptor_length << 3)
                i = 4
                while i:
                    i -= 1
                    try:
                        stream_type = bitbin.ashex(8)
                        bitbin.forward(3)
                        elementary_PID = bitbin.asint(13)
                        N -= 24
                        self.pid_prog[elementary_PID]=program_number
                        if stream_type == '0x86':
                            if elementary_PID not in self.scte35_pids:
                                self.scte35_pids.append(elementary_PID)
                        reserved = bitbin.forward(4)
                        ES_info_length = bitbin.asint(12)
                        N -= 16
                        bitbin.forward(ES_info_length << 3)
                        N -= (ES_info_length <<3)
                    except:
                        continue

    def pas(self,bitbin):
        bitbin.forward(9)
        if bitbin.asflag(1):
            return    
        bitbin.forward(2)
        section_length = bitbin.asint(12)     
        sl = (section_length << 3) 
        bitbin.forward(40)
        sl -= 40
        while sl> 40:
            program_number = bitbin.asint(16)
            bitbin.forward(3)
            if program_number == 0:
                bitbin.forward(13)
            else:
                pmap_pid = bitbin.asint(13)
                self.pmt_pids.add(pmap_pid)
            sl -= 32
        bitbin.forward(32)
        
    def parse_pts(self,pdata,pid):
        pts  = ((pdata[9] >> 1) & 7) << 30
        pts += (((pdata[10] << 7) + (pdata[11] >> 1)) << 15)
        pts += (pdata[12] << 7) + (pdata[13] >> 1)
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

    def parser(self,pkt):
        pid = (pkt[1] & 31) << 8
        pid += pkt[2]
        if pid == 0:
            if not self.called_pas:
                bitbin = BitBin(pkt[5:])
                self.pas(bitbin)
                self.pmt_pids.add(None)
                self.called_pas = True       

        elif pid in self.pmt_pids:
            bitbin = BitBin(pkt[5:])
            self.pms(bitbin,pid)
            
        elif pid in self.pid_prog.keys():
            if (pkt[1] >> 6) & 1 : self.parse_pusi(pkt[4:18],pid)
              
        if pid in self.scte35_pids:
            packet_data = {}
            packet_data['pid'] = pid
            packet_data['program'] = self.pid_prog[pid]
            packet_data['pts']= self.PTS[self.pid_prog[pid]]
            cue = Cue(pkt,packet_data)
            cue.show()
        
