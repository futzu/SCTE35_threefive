import base64
import bitstring
try: import threefive.tables as tables
except: import tables

PACKET_SIZE=188

def hex_decode(k):
    try: return bytearray.fromhex(hex(k)[2:]).decode()
    except: return k

def kv_print(obj):
    dotdot=' : '
    for k,v in vars(obj).items(): print(f'{k}{dotdot}{v}')
 
def mk_bits(s):
    if type(s) in [bitstring.BitStream,bitstring.ConstBitStream]: return s
    try: return bitstring.ConstBitStream(bytes=base64.b64decode(s))
    except: return bitstring.ConstBitStream(s)

def reserved(bb,bst):
    bb.bitpos+=bst

def time_90k(k):
    t= k/90000.0    
    return f'{t :.6f}'



