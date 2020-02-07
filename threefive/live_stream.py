from .splice import Splice
from bitn import BitBin

PACKET_SIZE=188
SYNC_BYTE=b'\x47'
NON_PTS_STREAM_IDS=[188,190,191,240,241,242,248]

class LiveStream:
    def __init__(self,tsfile=None,tsstream=None,show_null=True):
        self.splices=[]
        self.PID=False
        self.show_null=show_null
        self.packetnum=0
        self.next_scte35=self.tf=False
        print('\n\n')
        if tsfile: self.parse_tsfile(tsfile)
        if tsstream: self.parse_tsdata(tsstream)
        print('\n\n')
        self.show()

    def parse_tsfile(self,tsfile):
        with open(tsfile,'rb') as tsdata:
            self.parse_tsdata(tsdata)


    def parse_tsdata(self,tsdata):
        while tsdata:
            if tsdata.read(1)==SYNC_BYTE: 
                packet =tsdata.read(PACKET_SIZE - 1)
                if packet: self.parse_tspacket(packet)
                else: break
            else: return 


    def parse_tspacket(self,packet):
        self.packetnum+=1
        three_bytes=BitBin(packet[:3])
        tei=three_bytes.asflag(1)
        pusi=three_bytes.asflag(1)
        ts_priority=three_bytes.asflag(1)
        pid=three_bytes.asint(13)
        if pusi: 
            bs=BitBin(packet[3:])
            if bs.asint(24)==1 and bs.asint(8) not in NON_PTS_STREAM_IDS :
                PES_packet_length=bs.asint(16)
                if bs.asint(2)==2:
                    PES_scramble_control=bs.asint(2)
                    PES_priority=bs.asint(1)
                    data_align_ind=bs.asint(1)
                    copyright=bs.asint(1)
                    orig_or_copy=bs.asint(1)
                    if bs.asint(2)==2:
                        bs.asint(14)
                        if bs.asint(4) ==2:
                            a=bs.asint(3)<<30
                            bs.asflag(1)
                            b=bs.asint(15) << 15
                            bs.asflag(1)
                            c=bs.asint(15)
                            d=(a+b+c)/90000
                            fpts=f'PTS \033[92m{d:.6f}\033[0m '
                            if not self.next_scte35: 
                                out =fpts
                            else:
                                fcmd=f'{self.tf.command.name}@\033[92m {self.next_scte35}\033[0m '
                                if self.tf.command.out_of_network_indicator:
                                    fbd=f'Duration: \033[92m{self.tf.command.break_duration}\033[92m '
                                    out=f'{fpts}{fcmd}{fbd}'
                                else: out=f'{fpts}{fcmd}'
                                if self.tf.command.splice_event_id:
                                    out = f'{out}\033[0mEvent: \033[92m{self.tf.command.splice_event_id} \033[0m'   
                            print(f'\r{out}', end="\r")
            
            
                                                       
        scramble=three_bytes.asint(2)
        afc=three_bytes.asint(2)
        count=three_bytes.asint(4)
        cue=packet[4:]
        '''
        if afc in [2,3]:
            #print('pid',hex(pid),'afc',afc)
            bs=Slicer9k(cue)
            adaptation_fields(bs)
            return
        '''
        if packet[4] !=0xfc: return            
        if self.PID and (pid !=self.PID): return
        try:
            tf=Splice(cue)
        except: 
            return 
        try:
            self.next_scte35  =tf.command.pts_time
            self.tf=tf
            print()
        except: pass
        if not self.PID: 
           self.PID=pid
        self.splices.append(tf)       
        return

    def show(self):
        for s in self.splices:
            #print( f'\n[ Splice {self.splices.index(s)} ]')
            s.show()
