iimport base64


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




