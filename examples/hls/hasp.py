import os
import sys
import urllib.request

import pyaes
import threefive


class HASP:
    """
    HASP stands for HLS AES SCTE-35 Parser
    HASP decodes AES encrypted segments for the
    start time of the first segment read.
    Try it with a stream like this

    python3 hasp.py https://turnerlive.warnermediacdn.com/hls/live/586495/cnngo/cnn_slate/VIDEO_2_1964000.m3u8

    """

    def __init__(self, arg):
        self.last_time = 0
        self.hls_time = 0
        self.seg_list = []
        self.cue_list = []
        self.start = False
        if arg.startswith("http"):
            self.base_uri = arg[: arg.rindex("/") + 1]
        self.manifest = None

    def _get_line(self):
        line = self.manifest.readline()
        if not line:
            return False
        if isinstance(line, bytes):
            line = line.decode()
        line = line.replace(" ", "").replace('"', "")
        return line

    def decode(self, manifest):
        self.manifest = manifest
        while self.manifest:
            line = self._get_line()
            if not line:
                break
            if not self.start:
                print(line)
                self._aes_start(line)
            else:
                self._extinf(line)
                self._ext_x_scte35(line)
                self._ext_x_daterange(line)

    def _aes_start(self, line):
        # #EXT-X-KEY:METHOD=AES-128,
        # URI="https://example.com/the.key
        # IV=0xD011E56BB500F70E18A59B42E496EE8E
        if line.startswith("#EXT-X-KEY:METHOD=AES-128"):
            next_seg = self._extinf(self._get_line())
            if next_seg:
                mode = self._aes_mode(line)
                vid_uri = self.base_uri + next_seg
                self._aes_decrypt(mode, vid_uri)

    def _aes_mode(self, line):
        key_uri = line.split("URI=")[1].split(",")[0]
        piv = (line.split("IV=")[1])[2:].split(",")[0]
        iv = bytes.fromhex(piv)
        key = self._aes_get_key(key_uri)
        mode = pyaes.AESModeOfOperationCBC(key, iv=iv)
        return mode

    def _aes_decrypt(self, mode, vid_uri):
        tmp = "tmp.ts"
        with urllib.request.urlopen(vid_uri) as infile:
            with open(tmp, "wb") as outfile:
                pyaes.decrypt_stream(mode, infile, outfile)
        self._get_pcr_start(tmp)

    def _aes_get_key(self, key_uri):
        with urllib.request.urlopen(key_uri) as quay:
            key = quay.read()
            return key

    def _get_pcr_start(self, tmp):
        with open(tmp, "rb") as tsdata:
            strm = threefive.Stream(tsdata)
            self.start = strm.decode_start_time()
            self.hls_time += self.start
            os.unlink(tmp)

    def _extinf(self, line):
        ##EXTINF:4.000000,
        if line.startswith("#EXTINF"):
            t = line.split(":")[1].split(",")[0]
            t = float(t)
            next_segment = self._get_line()[:-1]
            if next_segment not in self.seg_list:
                print(f"Segment:  {next_segment} @ {self.hls_time}")  # , end = '\r')
                self.seg_list.append(next_segment)
                self.seg_list = self.seg_list[-500:]
                self.hls_time += t
                return next_segment

    def _ext_x_scte35(self, line):
        # EXT-X-SCTE35:CUE=
        if line.startswith("#EXT-X-SCTE35"):
            mesg = line.split("CUE=")[1].split(",")[0]
            self._do_cue(f"{mesg}")
        if line.startswith("#EXT-OATCLS-SCTE35:"):
            mesg = line.split("#EXT-OATCLS-SCTE35:")[1]
            self._do_cue(f"{mesg}")

    def _ext_x_daterange(self, line):
        ##EXT-X-DATERANGE
        if line.startswith("#EXT-X-DATERANGE:"):
            for chunk in line.split(","):
                k, v = chunk.split("=")
                if k.startswith("SCTE35"):
                    self._do_cue(v)

    def _do_cue(self, mesg):
        if mesg not in self.cue_list:
            print(f"cue: {mesg}")
            self.cue_list.append(mesg)
            self.cue_list = self.cue_list[-10:]
            tf = threefive.Cue(mesg)
            tf.decode()
            tf.show()


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
    while True:
        with urllib.request.urlopen(arg) as manifest:
            hasp.decode(manifest)
