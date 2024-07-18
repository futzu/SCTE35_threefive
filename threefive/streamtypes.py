"""

streamtypes.py

    Used by threefive.Stream
    On import stream_types generates a complete streamtype_map.

        from .streamtypes import streamtype_map

"""

streamtype_map = {
    0x00: "Reserved",
    0x01: "ISO/IEC 11172-2 (MPEG-1 video)",
    0x02: "ITU-T Rec. H.262 and ISO/IEC 13818-2 (MPEG-2 higher rate interlaced video)",
    0x03: "ISO/IEC 11172-3 (MPEG-1 audio)",
    0x04: "ISO/IEC 13818-3 (MPEG-2 halved sample rate audio)",
    0x05: "ITU-T Rec. H.222 and ISO/IEC 13818-1 (MPEG-2 tabled data)",
    0x06: "ITU-T Rec. H.222 and ISO/IEC 13818-1 (MPEG-2 packetized data)",
    0x07: "ISO/IEC 13522 (MHEG)",
    0x08: "ITU-T Rec. H.222 and ISO/IEC 13818-1 DSM CC",
    0x09: "ITU-T Rec. H.222 and ISO/IEC 13818-1/11172-1 auxiliary data",
    0x0A: "ISO/IEC 13818-6 DSM CC multiprotocol encapsulation",
    0x0B: "ISO/IEC 13818-6 DSM CC U-N messages",
    0x0C: "ISO/IEC 13818-6 DSM CC stream descriptors",
    0x0D: "ISO/IEC 13818-6 DSM CC tabled data",
    0x0E: "ISO/IEC 13818-1 auxiliary data",
    0x0F: "ISO/IEC 13818-7 ADTS AAC (MPEG-2 lower bit-rate audio)",
    0x10: "ISO/IEC 14496-2 (MPEG-4 H.263 based video)",
    0x11: "ISO/IEC 14496-3 (MPEG-4 LOAS multi-format framed audio)",
    0x12: "ISO/IEC 14496-1 (MPEG-4 FlexMux)",
    0x13: "ISO/IEC 14496-1 (MPEG-4 FlexMux)",
    0x14: "ISO/IEC 13818-6 DSM CC synchronized download protocol",
    0x15: "Packetized metadata",
    0x16: "Sectioned metadata",
    0x17: "ISO/IEC 13818-6 DSM CC Data Carousel metadata",
    0x18: "ISO/IEC 13818-6 DSM CC Object Carousel metadata",
    0x19: "ISO/IEC 13818-6 Synchronized Download Protocol metadata",
    0x1A: "ISO/IEC 13818-11 IPMP",
    0x1B: "ITU-T Rec. H.264 and ISO/IEC 14496-10 (lower bit-rate video)",
    0x1C: "ISO/IEC 14496-3 (MPEG-4 raw audio)",
    0x1D: "ISO/IEC 14496-17 (MPEG-4 text)",
    0x1E: "ISO/IEC 23002-3 (MPEG-4 auxiliary video)",
    0x1F: "ISO/IEC 14496-10 SVC (MPEG-4 AVC sub-bitstream)",
    0x20: "ISO/IEC 14496-10 MVC (MPEG-4 AVC sub-bitstream)",
    0x21: "ITU-T Rec. T.800 and ISO/IEC 15444 (JPEG 2000 video)",
    # 0x22 - 0x23:"Reserved.",
    0x24: "ITU-T Rec. H.265 and ISO/IEC 23008-2 (Ultra HD video)",
    # 0x25 - 0x41:"Reserved.",
    0x42: "Chinese Video Standard",
    # 0x43 - 0x7e:"Reserved.",
    0x7F: "ISO/IEC 13818-11 IPMP (DRM)",
    0x80: "ITU-T Rec. H.262 and ISO/IEC 13818-2 with DES-64-CBC encryption for DigiCipher II",
    0x81: "Dolby Digital (AC-3) up to six channel audio for ATSC and Blu-ray",
    0x82: "SCTE subtitle",
    0x83: "Dolby TrueHD lossless audio for Blu-ray",
    0x84: "Dolby Digital Plus (enhanced AC-3) up to 16 channel audio for Blu-ray",
    0x85: "DTS 8 channel audio for Blu-ray",
    0x86: "SCTE-35[5] digital program insertion cue message",
    0x87: "Dolby Digital Plus (enhanced AC-3) up to 16 channel audio for ATSC",
    # 0x88 - 0x89:"Privately defined.",
    0x90: "Blu-ray Presentation Graphic Stream (subtitling)",
    0x91: "ATSC DSM CC Network Resources table",
    # 0x92 - 0xBF:"Privately defined.",
    0xC0: "DigiCipher II text",
    0xC1: "Dolby Digital (AC-3) up to six channel audio with AES-128-CBC data encryption",
    0xC2: "ATSC DSM CC synchronous data",
    # 0xC3 - 0xCE:"Privately defined.",
    0xCF: "ISO/IEC 13818-7 ADTS AAC with AES-128-CBC frame encryption",
    0xD0: "Privately defined.",
    0xD1: "BBC Dirac (Ultra HD video)",
    0xD2: "Audio Video Standard AVS2 (Ultra HD video)",
    0xD3: "Audio Video Standard AVS3 Audio",
    0xD4: "Audio Video Standard AVS3 Video (Ultra HD video)",
    # 0xD5 - 0xDA:"Privately defined.",
    0xDB: "ITU-T Rec. H.264 and ISO/IEC 14496-10 with AES-128-CBC slice encryption",
    # 0xDC - 0xE9:"Privately defined.",
    0xEA: "Microsoft Windows Media Video 9 (lower bit-rate video)",
    # 0xEB - 0xFF:"Privately defined.",
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
    + list(range(0xEB, 0xFF)),
}


def hex_literal(integer):
    return int(hex(integer), base=16)


def add_stream_types(alist, streamtype):
    for i in alist:
        j = hex_literal(i)
        streamtype_map[j] = streamtype


def mk_streamtype_map(others):
    for k, v in others.items():
        add_stream_types(v, k)
    keys = list(streamtype_map.keys())
    keys.sort()


mk_streamtype_map(others)
