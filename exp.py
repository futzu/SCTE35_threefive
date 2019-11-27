from struct import unpack
from time import sleep
import sys
import threefive
import bitstring

class TSPacket(object):
    def __init__(self, raw_data):
        self.sync, pid, count, payload = unpack('>BHB184s', raw_data)# switch to bitstring
        self.pid = pid & 8191
        if self.pid==0x135 and b'CUEI' in payload: 
            raw_data2=bitstring.BitStream(raw_data)
            print(raw_data2[40:])
            threefive.Splice(raw_data2[40:]).show()
 
if __name__ == '__main__': 
    input = open(sys.argv[1], 'rb')
    psize = 188 
    chunksize = 7

    while True:
        data = input.read(psize * chunksize)
        if not data: break
        # Chop off anything before the sync bit
        sync_offset = data.find(0x47)
        if sync_offset == -1:
            #print 'No sync bit in packet.'
            continue
        if sync_offset != 0:
            #print 'Resync'
            data = data[sync_offset:]

        for i in range(chunksize):
            packet = data[:psize]
            data = data[psize:]
            packet = TSPacket(packet)

