import base64
import bitstring


def bitslice(data,bit_idx,num_bits):
    if type(data) == bytes: data=int.from_bytes(data,byteorder='big')
    return (data >> (bit_idx+1-num_bits)) & ~(~0 << num_bits)


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


