"""
The threefive.Segment class
"""
import os

import pyaes

from .reader import reader
from .stream import Stream


class Segment(Stream):
    """
    The Segment class is a Sub Class of threefive.Stream
    made for small, fixed size MPEGTS files,like HLS segments.

    Segment Class Specific Features:

    * Decryption of AES Encrypted MPEGTS.

    * Segment.cues  a list of SCTE35 cues found in the segment.


    Example:

        from threefive import Segment

        >>>> uri = "https://example.com/1.ts"
        >>>> seg = Segment(uri)
        >>>> seg.decode()
        >>>> [cue.encode() for cue in cues]
        ['/DARAAAAAAAAAP/wAAAAAHpPv/8=',
        '/DAvAAAAAAAAAP/wFAUAAAKWf+//4WoauH4BTFYgAAEAAAAKAAhDVUVJAAAAAOv1oqc=']

        # For aes encrypted files

        >>>> key = "https://example.com/aes.key"
        >>>> IV=0x998C575D24F514AEC84EDC5CABCCDB81
        >>>> uri = "https://example.com/aes-1.ts"

        >>>> seg = Segment(uri,key_uri=key, iv=IV)
        >>>> seg.decode()
        >>>> {cue.packet_data.pcr:cue.encode() for cue in seg.cues}

       { 89718.451333: '/DARAAAAAAAAAP/wAAAAAHpPv/8=',
       89730.281789: '/DAvAAAAAAAAAP/wFAUAAAKWf+//4WoauH4BTFYgAAEAAAAKAAhDVUVJAAAAAOv1oqc='}

    """

    def __init__(self, seg_uri, key_uri=None, iv=None):
        self.seg_uri = seg_uri
        self.key_uri = key_uri
        self.key = None
        self.iv = None
        self.cues = []
        self.start = None
        self.tmp = None
        if iv:
            self.iv = int.to_bytes(int(iv), 16, byteorder="big")
        if self.key_uri:
            self._aes_get_key()
            self._aes_decrypt()
        super().__init__(self.seg_uri)

    def __repr__(self):
        return str(self.__dict__)

    def _mk_tmp(self):
        self.tmp = "tf-"
        self.tmp += self.seg_uri.rsplit("/", 1)[-1]

    def _aes_get_key(self):
        with reader(self.key_uri) as quay:
            self.key = quay.read()

    def _aes_decrypt(self):
        mode = pyaes.AESModeOfOperationCBC(self.key, iv=self.iv)
        self._mk_tmp()
        with open(self.tmp, "wb") as outfile:
            with reader(self.seg_uri) as infile:
                pyaes.decrypt_stream(mode, infile, outfile)
            self.seg_uri = self.tmp

    def add_cue(self, cue):
        """
        add_cue is passed to a Stream instance
        to collect SCTE35 cues.
        """
        self.cues.append(cue)

    def show_cue(self, cue):
        """
        show_cue prints SCTE35 Cue data
        and calls add_cue to append the cue to
        the Segment,cues list.
        """
        cue.show()
        self.add_cue(cue)

    def decode(self):
        """
        decode a mpegts segment.
        """
        super().decode(func=self.show_cue)
        if self.tmp:
            os.unlink(self.tmp)
