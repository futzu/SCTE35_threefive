"""
hasp.py  take three.

"""


import os
import sys
import urllib.request
import pyaes
import threefive


class Stanza:
    """
    The Stanza class represents a segment
    and associated data

    ex.

    #EXT-X-KEY:METHOD=AES-128,URI="example.com/keys/027a0d992ff6a49a484e6d9b58cfcd0531df924d.key",IV=0x92B99B3F257801E616D08261E3078B19
    #EXT-X-ASSET:CAID=0x00000000381B85CE
    #EXT-X-CUE-OUT:250.133
    #EXT-X-SCTE35:CUE="/DA2AAAAAAAAAAAABQaAUH4T/gAgAh5DVUVJQAVCawDAAAFXgYsICAAAAAA4G4XONAAAAADqLWsS",ID="1074086507"
    #EXTINF:6.006,
    1630520255_video_480p-30fps-1836kbps/video_185222.ts

    """

    def __init__(self, lines, segment, start):
        self.lines = lines
        self.segment = segment
        self.start = start
        self.duration = 0
        self.cue = False
        self.iv = None
        self.key = None
        self.key_uri = None
        self.mode = None

    def _aes_start(self, line):
        if line.startswith("#EXT-X-KEY:METHOD=AES-128"):
            try:
                self._aes_mode(line)
                self._aes_decrypt()
            except:
                self.start = 0.0

    def _aes_mode(self, line):
        self.key_uri = line.split("URI=")[1].split(",")[0]
        piv = (line.split("IV=")[1])[2:].split(",")[0]
        self.iv = bytes.fromhex(piv)
        self._aes_get_key()
        self.mode = pyaes.AESModeOfOperationCBC(self.key, iv=self.iv)

    def _aes_decrypt(self):
        tmp = self.segment.rsplit("/", 1)[1]
        with threefive.reader(self.segment) as infile:
            with open(tmp, "wb") as outfile:
                pyaes.decrypt_stream(self.mode, infile, outfile)
        self._get_pcr_start(tmp)

    def _aes_get_key(self):
        with threefive.reader(self.key_uri) as quay:
            self.key = quay.read()

    def _get_pcr_start(self, tmp):
        strm = threefive.Stream(tmp)
        self.start = strm.decode_start_time()
        os.unlink(tmp)

    def _extinf(self, line):
        if line.startswith("#EXTINF"):
            t = line.split(":")[1].split(",")[0]
            t = float(t)
            self.duration = round(t, 6)

    def _ext_x_scte35(self, line):
        if line.startswith("#EXT-X-SCTE35"):
            self.cue = line.split("CUE=")[1].split(",")[0]
        if line.startswith("#EXT-OATCLS-SCTE35:"):
            self.cue = line.split("#EXT-OATCLS-SCTE35:")[1]

    def _ext_x_daterange(self, line):
        if line.startswith("#EXT-X-DATERANGE:"):
            for chunk in line.split(","):
                k, v = chunk.split("=")
                if k.startswith("SCTE35"):
                    self.cue = v

    def do_cue(self):
        """
        do_cue parses a SCTE-35 encoded string
        via the threefive.Cue class
        """
        if self.cue:
            tf = threefive.Cue(self.cue)
            tf.decode()
            tf.show()

    def decode(self):
        for line in self.lines:
            if not self.start:
                self._aes_start(line)
            self._ext_x_scte35(line)
            self._extinf(line)
            self._ext_x_daterange(line)
        return self.start


class HASP:
    """
    HASP stands for HLS AES SCTE-35 Parser
    HASP decodes AES encrypted segments for the
    start time of the first segment read.
    Try it with a stream like this

    python3 hasp.py https://turnerlive.warnermediacdn.com/hls/live/586495/cnngo/cnn_slate/VIDEO_2_1964000.m3u8

    """

    def __init__(self, arg):
        self.m3u8 = arg
        self.hls_time = 0
        self.seg_list = []
        self._start = False
        self.chunk = []
        if arg.startswith("http"):
            self.base_uri = arg[: arg.rindex("/") + 1]
        self.manifest = None

    @staticmethod
    def _clean_line(line):
        if isinstance(line, bytes):
            line = line.decode()
        line = line.replace(" ", "").replace('"', "").replace("\n", "")
        return line

    def decode(self):
        rev_text = "\033[7m \033[1m"
        reset_text = "\033[00m"
        pre = rev_text
        while True:
            with threefive.reader(self.m3u8) as self.manifest:
                while self.manifest:
                    line = self.manifest.readline()
                    if not line:
                        break
                    line = self._clean_line(line)
                    self.chunk.append(line)
                    if not (line.startswith("#")):
                        segment = line
                        if not (line.startswith("http")):
                            segment = self.base_uri + line
                        if segment not in self.seg_list:
                            self.seg_list.append(segment)
                            self.seg_list = self.seg_list[-200:]
                            stanza = Stanza(self.chunk, segment, self._start)
                            self._start = stanza.decode()
                            tail = ""
                            if stanza.cue:
                                tail = f"{rev_text}Cue:{reset_text} {stanza.cue}"
                            effed = f"{line}\t{rev_text}Start:{reset_text} {round(self.hls_time,6)}\t{rev_text}Duration:{reset_text} {stanza.duration}\n{tail}"
                            print(effed)
                            if stanza.cue:
                                stanza.do_cue()
                            self.hls_time += stanza.duration
                        self.chunk = []


def chk_version():
    min_version = 2300
    vn = int(threefive.version().replace(".", ""))
    if vn < min_version:
        print(f"this script requires threefive.version {min_version} or higher. ")

        sys.exit()


if __name__ == "__main__":
    chk_version()
    arg = sys.argv[1]
    HASP(arg).decode()
