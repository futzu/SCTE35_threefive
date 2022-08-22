"""
hasp.py

    HASP stands for HLS AES SCTE-35 Parser
    HASP decodes AES encrypted segments for the
    start time of the first segment read.

    Try it with a stream like this:

    pypy3 hasp.py https://phls-vod.cdn.turner.com/cnnngtv/cnn/hls/2018/12/03/urn:ngtv-show:115615/index_1.m3u8


"""


import os
import sys
import pyaes
import threefive
from new_reader import reader


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
        self.clean_segment()
        self.decoded_seg = None
        self.pts = None
        self.start = start
        self.duration = 0
        self.cue = False
        self.iv = None
        self.key = None
        self.key_uri = None
        self.mode = None

    def clean_segment(self):
        if self.segment.startswith("http"):
            ss = self.segment.split("/")
            while ".." in ss:
                i = ss.index("..")
                del ss[i]
                del ss[i - 1]
            self.segment = "/".join(ss)

    def _aes_start(self, line):
        if line.startswith("#EXT-X-KEY:METHOD=AES-128"):
            try:
                self._aes_mode(line)
                self._aes_decrypt()
                return True
            except:
                return False

    def _aes_mode(self, line):
        self.key_uri = line.split("URI=")[1].split(",")[0]
        piv = (line.split("IV=")[1])[2:].split(",")[0]
        self.iv = bytes.fromhex(piv)
        self._aes_get_key()
        self.mode = pyaes.AESModeOfOperationCBC(self.key, iv=self.iv)

    def _aes_decrypt(self):
        try:
            tmp = self.segment.rsplit("/", 1)[1]
            with threefive.reader(self.segment) as infile:
                with open(tmp, "wb") as outfile:
                    pyaes.decrypt_stream(self.mode, infile, outfile)
                    self._get_pts_start(tmp)
            os.unlink(tmp)
        except:
            pass

    def _aes_get_key(self):
        if not self.key_uri.startswith("http"):
            head = self.segment[: self.segment.rindex("/") + 1]
            self.key_uri = head + self.key_uri
        with threefive.reader(self.key_uri) as quay:
            self.key = quay.read()

    def _get_pts_start(self, seg):
        if not self.start:
            pts_start = 0.0
            try:
                strm = threefive.Stream(seg)
                strm.decode()
                if len(strm.start.values()) > 0:
                    pts_start = strm.start.popitem()[1]
                self.pts = round(pts_start / 90000.0, 6)
            except:
                pass
        self.start = self.pts

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

            print(line)
            self._ext_x_scte35(line)
            self._extinf(line)
            self._ext_x_daterange(line)
            if not self.pts:
                self._get_pts_start(self.segment)
                self.start = self.pts
        if not self.start:
            self.start = 0.0
        return self.start


class HASP:
    """
    HASP stands for HLS AES SCTE-35 Parser
    HASP decodes AES encrypted segments for the
    start time of the first segment read.
    Try it with a stream like this

    python3 hasp.py https://phls-vod.cdn.turner.com/cnnngtv/cnn/hls/2018/12/03/urn:ngtv-show:115615/index_1.m3u8
    """

    def __init__(self, arg):
        self.m3u8 = arg
        self.hls_time = 0.0
        self.seg_list = []
        self._start = None
        self.chunk = []
        self.base_uri = ""
        if arg.startswith("http"):
            self.base_uri = arg[: arg.rindex("/") + 1]
        self.manifest = None
        self.target_duration = 0
        self.next_expected = 0

    @staticmethod
    def _clean_line(line):
        if isinstance(line, bytes):
            line = line.decode(errors="ignore")
        line = (
            line.replace(" ", "").replace('"', "").replace("\n", "").replace("\r", "")
        )
        return line

    def show_segment_times(self, stanza):
        print(f"Segment: {stanza.segment}")
        print(f"Segment Duration  : {stanza.duration}")
        print(f"Segment Start   :{round(self.next_expected,6)}")
        print(f"HLS Time: {round(self.hls_time,6)}")
        #   + f"Segment Duration  : {stanza.duration}"
        # )
        # if stanza.pts:
        #   print(f"{rev_text}pts Time        :{reset_text} {stanza.pts}\n")
        if stanza.cue:
            # print(f"Cue:\n")
            # stanza.do_cue()
            print("\n")

    def do_segment(self, line):
        segment = line
        if not line.startswith("http"):
            segment = self.base_uri + line
        if segment not in self.seg_list:
            self.seg_list.append(segment)
            self.seg_list = self.seg_list[-101:]
            stanza = Stanza(self.chunk, segment, self._start)
            stanza.decode()
            if not self._start:
                self._start = stanza.start
            self.next_expected = self._start + self.hls_time
            self.show_segment_times(stanza)
            self.next_expected += round(stanza.duration, 6)
            self.hls_time += stanza.duration
        self.chunk = []

    def decode(self):
        while True:
            with reader(self.m3u8) as self.manifest:
                while self.manifest:
                    line = self.manifest.readline()
                    if not line:
                        break
                    line = self._clean_line(line)
                    if "ENDLIST" in line:
                        return False
                    if "TARGETDURATION" in line:
                        self.target_duration = int(line.split(":")[1]) >> 1
                    self.chunk.append(line)
                    if not line.startswith("#"):
                        self.do_segment(line)


def chk_version():
    min_version = 2305
    vn = int(threefive.version().replace(".", ""))
    if vn < min_version:
        print(f"this script requires threefive.version {min_version} or higher. ")

        sys.exit()


if __name__ == "__main__":
    chk_version()
    arg = sys.argv[1]
    HASP(arg).decode()
