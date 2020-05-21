import sys
from threefive import Splice,StreamPlus

'''
Subclassing example

Usage: python3 streamstats.py < video.ts

'''

class StreamStats(StreamPlus):
    '''
    monitor a live video stream
    '''

    def parse_packet(self,packet):
        two_bytes = int.from_bytes(packet[1:3],byteorder='big')
        pid = two_bytes & 0x1fff
        pusi = two_bytes >> 14 & 0x1
        if pusi: 
            self.parse_pusi(packet[4:20])
        if self.chk_tid(packet):
            if self.chk_type(packet[:20]):
                Splice(packet, pid = pid, pts = self.PTS).show() 
                print(f'\033[92mSCTE35\033[0m {tf.command.name} @ \033[92m{self.PTS:0.3f}\033[0m')
                tf.show_command()
                print('\n')

if __name__ == '__main__':
    # pipe the video in 
    StreamStats(sys.stdin.buffer)
