"""
SCTE35 DTMF Descriptor Example

Usage:
    pypy3 Dtmf_Descriptor.py

"""


from threefive import decode

if __name__ == "__main__":
    DTMF = "/DAsAAAAAAAAAP/wDwUAAABef0/+zPACTQAAAAAADAEKQ1VFSbGfMTIxIxGolm0="
    decode(DTMF)
