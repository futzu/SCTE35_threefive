'''
parse scte35 from mpegts binary files
'''
import sys, threefive
from struct import unpack

PACKET_SIZE=188
PID=0x135
SYNC_BYTE=0x47

def parse_tsfile(tsfile):
    with open(tsfile,'rb') as tsdata: parse_tsdata(tsdata)

def parse_tsdata(tsdata):
    while tsdata:
        data = tsdata.read(PACKET_SIZE)
        if not data: break
        sync_offset = data.find(SYNC_BYTE)
        if sync_offset != 0: data = data[sync_offset:]
        sync,pid =unpack('>BH', data[:3])
        pid=pid & 8191
        if pid==PID: parse_tspacket(data[3:])

def parse_tspacket(tspacket):
    _, payload = unpack('>H183s', tspacket)
    threefive.Splice(payload).show()
 
if __name__ == '__main__': 
    parse_tsfile(sys.argv[1])
 
