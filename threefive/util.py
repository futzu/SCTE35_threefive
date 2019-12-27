import base64

def bitslice(data,bit_idx,num_bits):
    if type(data) == bytes: data=int.from_bytes(data,byteorder='big')
    return (data >> (bit_idx+1-num_bits)) & ~(~0 << num_bits)


def hex_decode(k):
    try: return bytearray.fromhex(hex(k)[2:]).decode()
    except: return k

def kv_print(obj):
    print(f'\t{vars(obj)}')
 
def mk_bits(s):
    if s[:2].lower()=='0x': s=s[2:]
    if s[:2].lower()=='fc': return bytes.fromhex(s)
    try: return base64.b64decode(s)
    except: return s

def time_90k(k):
    t= k/90000.0    
    return f'{t :.6f}'




