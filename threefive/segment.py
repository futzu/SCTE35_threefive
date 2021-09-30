"""
The threefive.Segment class
"""

import urllib

import pyaes

from .stream import Stream


class Segment:
    """
    The Segment class is used to process
    hls mpegts segments for segment start time
    and SCTE35 cues.
    local and http(s) segments are supported
    aes encoded segments are decrypted.
    Segment.start is the first timestamp found
    in the segment.
    Segment.cues is a list of Base64 encoded
    SCTE35 cues found in the segment.
    """

    def __init__(self, seg_uri, key_uri=None, iv=None):
        self.seg_uri = seg_uri
        self.seg_bites = None
        self.key_uri = key_uri
        self.key = None
        self.iv = None
        if iv:
            self.iv = bytes.fromhex(iv)
        if self.key_uri:
            self._aes_get_key()
            self._aes_decrypt()
        self.cues = []
        self.start = None

    @staticmethod
    def _reader(uri):
        if uri.startswith("http"):
            return urllib.request.urlopen(uri)
        return open(uri, "rb")

    def _aes_get_key(self):
        with self._reader(self.key_uri) as quay:
            self.key = quay.read()

    def _aes_decrypt(self):
        mode = pyaes.AESModeOfOperationCBC(self.key, iv=self.iv)
        tmp = "tmp"
        with open(tmp, "wb") as outfile:
            with self._reader(self.seg_uri) as infile:
                pyaes.decrypt_stream(mode, infile, outfile)
            self.seg_uri = tmp

    def add_cue(self, cue):
        """
        add_cue is passed to a Stream instance
        to collect SCTE35 cues.
        """
        self.cues.append(cue.encode())

    def decode(self):
        """
        decode a mpegts hls segment for start time
        and scte35 cues.
        """
        with self._reader(self.seg_uri) as seg:
            strm = Stream(seg)
            self.start = strm.decode_start_time()
            strm.show_start = False
            strm.decode(func=self.add_cue)
