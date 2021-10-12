"""
streamedit.py

An example of how to edit SCTE35 data
in MPEGTS packets on the fly and pass
the modifiied stream to stdout.

Example use:

pypy3 streamedit.py https://futzu.com/xaa.ts | pypy3 -c 'import threefive; threefive.decode()'

"""


from functools import partial
import sys

from threefive import Stream


class Stream2(Stream):
    """
    Stream2 is a subclass of threefive.Stream
    to demonstrate editing SCTE35 Cues in a MPEGTS stream.
    """

    _PAD = b"\xff"

    @staticmethod
    def edit_cue(cue):
        """
        edit_cue sets cue.info_section.pts_adjustment
        and then re-encodes the SCTE35 Cue.
        """
        print("BEFORE:", file=sys.stderr)
        cue.to_stderr()
        cue.info_section.pts_adjustment = 109.55
        cue.encode()
        print("AFTER:", file=sys.stderr)

    def repack_pkt(self, pkt, cue):
        """
        repack_pkt recreates the SCTE35 packet
        with the edited SCTE35 Cue as the payload
        adds padding as needed and then
        writes the new_packet to stdout
        """
        pay_idx = pkt.index(cue.bites)
        header = pkt[:pay_idx]
        self.edit_cue(cue)
        new_payload = cue.bites
        new_pkt = header + new_payload
        new_pkt += (self._PACKET_SIZE - len(new_pkt)) * self._PAD
        sys.stdout.buffer.write(new_pkt)

    def edit_scte35(self):
        """
        edit_scte35 applies Stream2.edit_cue(cue)
        on SCTE35 data before writing all packets
        to stdout.
        """
        if self._find_start():
            for pkt in iter(partial(self._tsdata.read, self._PACKET_SIZE), b""):
                cue = self._parse(pkt)
                if cue:
                    self.repack_pkt(pkt, cue)
                else:
                    sys.stdout.buffer.write(pkt)
        self._tsdata.close()


if __name__ == "__main__":
    args = sys.argv[1:]
    for arg in args:
        strm = Stream2(arg)
        strm.edit_scte35()
