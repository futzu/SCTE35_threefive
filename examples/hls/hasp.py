import os
import sys
import urllib.request

import pyaes
import threefive


class Stanza:
    def __init__(self, lines, segment, start):
        self.lines = lines
        self.segment = segment
        self.start = start
        self.duration = 0
        self.cue = False

    def _aes_start(self, line):
        # #EXT-X-KEY:METHOD=AES-128,
        # URI="https://example.com/the.key
        # IV=0xD011E56BB500F70E18A59B42E496EE8E
        if line.startswith("#EXT-X-KEY:METHOD=AES-128"):
            self._aes_mode(line)
            self._aes_decrypt()

    def _aes_mode(self, line):
        self.key_uri = line.split("URI=")[1].split(",")[0]
        piv = (line.split("IV=")[1])[2:].split(",")[0]
        self.iv = bytes.fromhex(piv)
        self._aes_get_key()
        self.mode = pyaes.AESModeOfOperationCBC(self.key, iv=self.iv)

    def _aes_decrypt(self):
        tmp = self.segment.rsplit("/", 1)[1]
        with urllib.request.urlopen(self.segment) as infile:
            with open(tmp, "wb") as outfile:
                pyaes.decrypt_stream(self.mode, infile, outfile)
        self._get_pcr_start(tmp)

    def _aes_get_key(self):
        with urllib.request.urlopen(self.key_uri) as quay:
            self.key = quay.read()

    def _get_pcr_start(self, tmp):
        with open(tmp, "rb") as tsdata:
            strm = threefive.Stream(tsdata)
            self.start = strm.decode_start_time()
            # os.unlink(tmp)

    def _extinf(self, line):
        ##EXTINF:4.000000,
        if line.startswith("#EXTINF"):
            t = line.split(":")[1].split(",")[0]
            t = float(t)
            self.duration = round(t, 6)

    def _ext_x_scte35(self, line):
        # EXT-X-SCTE35:CUE=
        if line.startswith("#EXT-X-SCTE35"):
            self.cue = line.split("CUE=")[1].split(",")[0]
        if line.startswith("#EXT-OATCLS-SCTE35:"):
            self.cue = line.split("#EXT-OATCLS-SCTE35:")[1]

    def _ext_x_daterange(self, line):
        ##EXT-X-DATERANGE
        if line.startswith("#EXT-X-DATERANGE:"):
            for chunk in line.split(","):
                k, v = chunk.split("=")
                if k.startswith("SCTE35"):
                    self.cue = v

    def do_cue(self):
        print(f"Cue: {self.cue}")
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

    def _get_line(self):
        line = self.manifest.readline()
        if not line:
            return False
        if isinstance(line, bytes):
            line = line.decode()
        line = line.replace(" ", "").replace('"', "").replace("\n", "")
        return line

    def decode(self):

        while True:
            with urllib.request.urlopen(self.m3u8) as self.manifest:
                while self.manifest:
                    line = self._get_line()
                    if not line:
                        break
                    self.chunk.append(line)
                    if not (line.startswith("#")):
                        segment = self.base_uri + line
                        if segment not in self.seg_list:
                            self.seg_list.append(segment)
                            self.seg_list = self.seg_list[-200:]
                            stanza = Stanza(self.chunk, segment, self._start)
                            hold = stanza.decode()
                            if not self._start:
                                self.hls_time = self._start = hold
                            print(
                                f"\033[7m \033[1m{line}\033[00m\nStart: {round(self.hls_time,6)}\nDuration:{stanza.duration}"
                            )
                            if stanza.cue:
                                stanza.do_cue()
                            self.hls_time += stanza.duration
                            print()
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
    hasp = HASP(arg)
    hasp.decode()
