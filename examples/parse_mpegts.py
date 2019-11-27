'''
parse scte35 from mpegts binary files
'''


import sys, threefive
from struct import unpack

def parse_packet(packet):
        sync, pid, count, payload = unpack('>BHB184s', packet)
        pid = pid & 8191
        if pid==0x135 and b'CUEI' in payload: 
            cue=payload[1:]
            threefive.Splice(cue).show()
 
if __name__ == '__main__': 
    psize = 188  
    with open(sys.argv[1],'rb') as tsfile:
        while tsfile:
            data = tsfile.read(psize)
            if not data: break
            sync_offset = data.find(0x47)
            if sync_offset != 0: data = data[sync_offset:]
            packet,data = data[:psize], data[psize:]
            parse_packet(packet)

