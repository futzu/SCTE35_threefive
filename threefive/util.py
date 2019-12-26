import base64
import bitstring


def grab_bits(data,start_bit,bit_count):
    return (data >> (start_bit+1-bit_count)) & ~(~0 << bit_count)


def hex_decode(k):
    try: return bytearray.fromhex(hex(k)[2:]).decode()
    except: return k

def kv_print(obj):
    print(f'\t{vars(obj)}')
 
def mk_bits(s):
    if type(s) in [bitstring.BitStream,bitstring.ConstBitStream]: return s
    try: return bitstring.ConstBitStream(bytes=base64.b64decode(s))
    except: return bitstring.ConstBitStream(s)

def reserved(bb,bst):
    bb.bitpos+=bst

def time_90k(k):
    t= k/90000.0    
    return f'{t :.6f}'







