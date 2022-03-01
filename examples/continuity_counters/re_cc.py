import sys
from functools import partial

from threefive import Stream


class ResetCC(Stream):
    def re_cc(self, proxy=True):
        """
        Stream.re_,,,cc resets the continuity counters.
        MPEGTS packets are written to stdout for piping.
        """
        if not self._find_start():
            return False
        pcount = 600
        outfile = sys.stdout.buffer
        if not proxy:
            outfile = open("re_cc.ts", "wb+")
        for chunk in iter(partial(self._tsdata.read, self._PACKET_SIZE * pcount), b""):
            chunky = memoryview(bytearray(chunk))
            chunks = [
                self._set_cc(chunky[i : i + self._PACKET_SIZE])
                for i in range(0, len(chunky), self._PACKET_SIZE)
            ]
            outfile.write(b"".join(chunks))
            chunky.release()
        self._tsdata.close()
        if not proxy:
            outfile.close()
        return True

    def re_cc_file(self):
        return self.re_cc(proxy=False)

    def _set_cc(self, pkt):
        pid = self._parse_pid(pkt[1], pkt[2])
        if pid == 0x1FFF:
            return pkt
        new_cc = 0
        if pid in self._pid_cc:
            last_cc = self._pid_cc[pid]
            if last_cc != 15:
                new_cc = last_cc + 1
        pkt[3] &= 0xF0
        pkt[3] += new_cc
        self._pid_cc[pid] = new_cc
        return pkt


if __name__ == "__main__":

    arg = sys.argv[1]

    resetter = ResetCC(arg)
    resetter.re_cc_file()
