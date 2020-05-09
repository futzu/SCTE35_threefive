import sys
from threefive import Splice,StreamPlus

'''
Subclassing example
'''

class StreamStats(StreamPlus):
    '''
    monitor a live video stream
    '''
    def __init__(self, tsdata, show_null = False):
        super().__init__(tsdata, show_null)

    def parse_payload(self,payload,pid):
        '''
        Override this method to customize output
        '''
        try:
            tf = Splice(payload,pid=pid, pts=self.PTS)
            print(f'\033[92mSCTE35\033[0m {tf.command.name} @ \033[92m{self.PTS:0.3f}\033[0m')
            tf.show_command()
            print('\n')
        except: pass
        
    def parse_tspacket(self, packet):
        '''
        parse a mpegts packet for SCTE 35 and/or PTS
        '''
        print(f'PTS: \033[92m{self.PTS:0.3f}\033[0m',end = '\r')
        super().parse_tspacket(packet)
        return
       
if __name__ == '__main__':
    # pipe the video in 
    StreamStats(sys.stdin.buffer)
