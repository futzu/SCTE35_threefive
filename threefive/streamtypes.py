"""

streamtypes.py

    Used by threefive.Stream
    On import stream_types generates a complete streamtype_map.

        from .streamtypes import streamtype_map

"""

streamtype_map = {
    0x00: "Reserved",
    0x01: "MPEG-1 video",
    0x02: "H.262  video",
    0x03: "MPEG-2 audio",
    0x04: "MPEG-2 halved sample rate audio",
    0x05: "MPEG-2 tabled data",
    0x06: "MPEG-2 binary data",
    0x07: "ISO/IEC 13522 (MHEG)",
    0x08: "H.222 and  DSM CC",
    0x09: "H.222 and auxiliary data",
    0x0A: "DSM CC multiprotocol encapsulation",
    0x0B: "DSM CC U-N messages",
    0x0C: "DSM CC stream descriptors",
    0x0D: "DSM CC tabled data",
    0x0E: "auxiliary data",
    0x0F: "ADTS AAC ",
    0x10: "MPEG-4 H.263 based video",
    0x11: "MPEG-4 LOAS multi-format framed audio",
    0x12: "MPEG-4 FlexMux",
    0x13: "MPEG-4 FlexMux",
    0x14: "DSM CC ",
    0x15: "ID3",
    0x16: "Sectioned metadata",
    0x17: "DSM CC Data Carousel metadata",
    0x18: "DSM CC Object Carousel metadata",
    0x19: "Synchronized Download Protocol metadata",
    0x1A: "IPMP",
    0x1B: "H.264",
    0x1C: "MPEG-4 raw audio)",
    0x1D: "MPEG-4 text",
    0x1E: "MPEG-4 auxiliary video",
    0x1F: "SVC (MPEG-4 AVC sub-bitstream)",
    0x20: "MVC (MPEG-4 AVC sub-bitstream)",
    0x21: "JPEG 2000 video",
    # 0x22 - 0x23:"Reserved.",
    0x24: " H.265",
    # 0x25 - 0x41:"Reserved.",
    0x42: "Chinese Video Standard",
    # 0x43 - 0x7e:"Reserved.",
    0x7F: " DRM Trash",
    0x80: "H.262 with DES-64-CBC ",
    0x81: "AC-3",
    0x82: "SCTE subtitle",
    0x83: "Dolby TrueHD audio ",
    0x84: "AC-3",
    0x85: "DTS 8 channel audio for Blu-ray",
    0x86: "SCTE-35",
    0x87: "AC-3 up to 16 channel audio for ATSC",
    # 0x88 - 0x89:"Privately defined.",
    0x90: "Blu-ray Presentation Graphic Stream (subtitling)",
    0x91: "ATSC DSM CC Network Resources table",
    # 0x92 - 0xBF:"Privately defined.",
    0xC0: "DigiCipher II text",
    0xC1: "AC-3  with AES-128-CBC ",
    0xC2: "ATSC DSM CC synchronous data",
    # 0xC3 - 0xCE:"Privately defined.",
    0xCF: "ADTS AAC with AES-128-CBC frame encryption",
    0xD0: "Privately defined.",
    0xD1: "BBC Dirac ",
    0xD2: "AVS2 ",
    0xD3: "AVS3 Audio",
    0xD4: "AVS3 Video ",
    # 0xD5 - 0xDA:"Privately defined.",
    0xDB: " H.264 with AES-128-CBC slice encryption",
    # 0xDC - 0xE9:"Privately defined.",
    0xEA: "Windows janky media v9",
    # 0xEB - 0xFB:"Privately defined.",
    0xFC: "KLV",
}


others = {
    "Reserved": list(range(0x22, 0x23))
    + list(range(0x25, 0x41))
    + list(range(0x43, 0x7E)),
    "Private": list(range(0x88, 0x89))
    + list(range(0x92, 0xBF))
    + list(range(0xC3, 0xCE))
    + list(range(0xD5, 0xDA))
    + list(range(0xDC, 0xE9))
    + list(range(0xEB, 0xFB))
    + list(range(0xFD,0xFF)),
}


def hex_literal(integer):
    """
    Return hex literal
    """
    return int(hex(integer), base=16)


def add_stream_types(alist, streamtype):
    """
    add_stream_types dynamically
    adds a range of a stream type,
    like "Reserved",to streamtype_map
    """
    for i in alist:
        j = hex_literal(i)
        streamtype_map[j] = streamtype


def mk_streamtype_map(others):
    """
    mk_streamtype_map dynamically adds
    stream types to streamtype_map
    """
    for k, v in others.items():
        add_stream_types(v, k)
    keys = list(streamtype_map.keys())
    keys.sort()


mk_streamtype_map(others)
