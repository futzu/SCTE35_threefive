"""
streamtype.py

stream_type_map is a dict
mapping MPEG-TS stream_types to stream descriptions.
"""


stream_type_map = {
    "0x0": "ITU-T | ISO/IEC Reserved",
    "0x1": "ISO/IEC 11172 Video",
    "0x2": "ITU-T Rec. H.262 | ISO/IEC 13818-2 or ISO/IEC 11172-2 Video",
    "0x3": "ISO/IEC 11172 Audio",
    "0x4": "ISO/IEC 13818-3 Audio",
    "0x5": "ITU-T Rec. H.222.0 | ISO/IEC 13818-1 private sections",
    "0x6": "SO/IEC 13818-1 PES packets- private data",
    "0x7": "ISO/IEC 13522 MHEG",
    "0x8": "ITU-T Rec. H.222.0 | ISO/IEC 13818-1 Annex A DSM-CC",
    "0x9": "ITU-T Rec. H.222.1",
    "0xA": "ISO/IEC 13818-6 type A",
    "0xB": "ISO/IEC 13818-6 type B",
    "0xC": "ISO/IEC 13818-6 type C",
    "0xD": "ISO/IEC 13818-6 type D",
    "0xE": "ITU-T Rec. H.222.0 | ISO/IEC 13818-1 auxiliary",
    "0xF": "ISO/IEC 13818-7 Audio with ADTS transport syntax",
    "0x10": "ISO/IEC 14496-2 Visual",
    "0x11": "ISO/IEC 14496-3 Audio - LATM transport ISO/IEC 14496-3 / AMD 1",
    "0x12": "ISO/IEC 14496-1 or FlexMux in PES packets",
    "0x13": "ISO/IEC 14496-1 or FlexMux in ISO/IEC14496 sections",
    "0x14": "ISO/IEC 13818-6 Synchronized Download Protocol",
    "0x1b": "Video",
    "0x86": "SCTE 35",
}
