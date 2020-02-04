import sys
import threefive

'''
This is proof of concept for SCTE35 HLS support.

Do not use this for any purpose.

this is not stable or complete, or supported.

'''


def do(cue):
   # print( f'cue string: {cue}')
    tf=threefive.Splice(cue)
    tf.show_info_section()
    tf.show_command()
    tf.show_descriptors()

class HlsM3u8:
    def __init__(self):
        self.hls_time=0
        self.duration=0
        self.cue_out=0
        self.cue_in=0
        self.parse_manifest()

    def chk_vars(self):
        if not (self.cue_in > self.hls_time):
            self.duration = self.cue_out = self.cue_in = 0 

    def parse_manifest(self):
        with open(sys.argv[1],'r') as manifest:
            while manifest:
                l=manifest.readline()
                if not l: break
                self.show_segment(l)
                self.parse_cue_out(l)
                self.parse_extinf(l)
                self.parse_x_scte35(l)
                self.parse_oatcls_scte35(l)
                self.parse_x_daterange(l)     
                self.chk_vars()

    def show_segment(self,aline):
        if not aline.startswith('#'):
            seg= aline[:-1]
            if self.cue_in > self.hls_time:
                print(f'{seg} hls time: {self.hls_time} time remaining: {self.cue_in - self.hls_time}')
            else:
                print(f'{seg} hls time: {self.hls_time }')   
                
    def parse_cue_out(self,aline):
        if not aline.startswith("#EXT-X-CUE-OUT:"):
            return
        self.cue_out=self.hls_time
        self.duration=float(aline.split(":")[1])
        self.cue_in=self.hls_time+self.duration
        print(f'{vars(self)}')
       
    def parse_extinf(self,aline):
        ##EXTINF:4.000000,
        if not aline.startswith("#EXTINF:"):
            return
        t=aline.split(":")[1].split(',')[0]
        t=float(t)
        self.hls_time+=t
        # print(f' hls time: {self.hls_time}')
 
            #print(f'{vars(self)}')

            
    def parse_x_scte35(self,aline):          
        if not aline.startswith('#EXT-X-SCTE35'):
            return 
        cue=aline.split('CUE=')[1]
        do(cue)
  
    def parse_oatcls_scte35(self,aline):                
        if not aline.startswith('#EXT-OATCLS-SCTE35:'):
            return
        cue=aline.split('#EXT-OATCLS-SCTE35:')[1]
        do(cue)
   
    def parse_x_daterange(self,aline):         
        ##EXT-X-DATERANGE:ID="splice-6FFFFFF0",START-DATE="2014-03-05T11:15:00Z",PLANNED-DURATION=59.993,SCTE35-OUT=0xFC002F0000000000FF000014056FFFFFF000E011622DCAFF000052636200000000000A000829896F50000008700000000
        if not aline.startswith('#EXT-X-DATERANGE:'):
            return
        values={}
        for chunk in line.split(','):
            k,v=chunk.split('=')
            if k.startswith('SCTE35'):
                v=threefive.Splice(v).show()
              
                  

manifest = HlsM3u8()
