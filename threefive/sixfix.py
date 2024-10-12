"""
fixsix.py
"""

import io
import sys
from threefive.crc import crc32
from threefive.bitn import NBin
from threefive.stuff import print2
from threefive.stream import Stream


def passed(cue):
    """
    passed a no-op function
    """
    return cue


class PreFix(Stream):
    """
    PreFix is used to gather 06 Bin data pids with SCTE-35.
    """

    def decode(self, func=passed):
        super().decode(func=passed)
        fixsix = self.pids.maybe_scte35
        if fixsix:
            print("fixing these pids", fixsix)
        return fixsix


class SixFix(Stream):
    """
    FixSix fixes bin data streams with SCTE-35 to 0x86 SCTE-35 streams
    """

    CUEI_DESCRIPTOR = b"\x05\x04CUEI"

    def __init__(self, tsdata=None):
        super().__init__(tsdata)
        self.pmt_payload = None
        self.con_pids = set()
        self.out_file = "sixfixed-" + tsdata.rsplit("/")[-1]
        self.in_file = sys.stdin.buffer

    def _parse_by_pid(self, pkt, pid):
        if pid in self.pids.tables:
            self._parse_tables(pkt, pid)
        if pid in self.pids.pmt:
            if self.pmt_payload:
                pkt = pkt[:4] + self.pmt_payload
        return pkt

    def convert_pid(self):
        """
        Stream.decode_proxy writes all ts packets are written to stdout
        for piping into another program like mplayer.
        SCTE-35 cues are printed to stderr.
        """
        active = io.BytesIO()
        pkt_count = 0
        chunk_size = 2048
        if isinstance(self.out_file, str):
            self.out_file = open(self.out_file, "wb")
        with self.out_file as out_file:
            for pkt in self.iter_pkts():
                pid = self._parse_pid(pkt[1], pkt[2])
                pkt = self._parse_by_pid(pkt, pid)
                active.write(pkt)
                pkt_count = (pkt_count + 1) % chunk_size
                if not pkt_count:
                    out_file.write(active.getbuffer())
                    active = io.BytesIO()

    def _regen_pmt(self, n_seclen, pcr_pid, n_proginfolen, n_info_bites, n_streams):
        nbin = NBin()
        nbin.add_int(2, 8)  # 0x02
        nbin.add_int(1, 1)  # section Syntax indicator
        nbin.add_int(0, 1)  # 0
        nbin.add_int(3, 2)  # reserved
        nbin.add_int(n_seclen, 12)  # section length
        nbin.add_int(1, 16)  # program number
        nbin.add_int(3, 2)  # reserved
        nbin.add_int(0, 5)  # version
        nbin.add_int(1, 1)  # current_next_indicator
        nbin.add_int(0, 8)  # section number
        nbin.add_int(0, 8)  # last section number
        nbin.add_int(7, 3)  # res
        nbin.add_int(pcr_pid, 13)
        nbin.add_int(15, 4)  # res
        nbin.add_int(n_proginfolen, 12)
        nbin.add_bites(n_info_bites)
        nbin.add_bites(n_streams)
        a_crc = crc32(nbin.bites)
        nbin.add_int(a_crc, 32)
        n_payload = nbin.bites
        pad = 187 - (len(n_payload) + 4)
        pointer_field = b"\x00"
        if pad > 0:
            n_payload = pointer_field + n_payload + (b"\xff" * pad)
        self.pmt_payload = n_payload

    def _parse_pmt(self, pay, pid):
        """
        parse program maps for streams
        """
        pay = self._chk_partial(pay, pid, self._PMT_TID)
        if not pay:
            return False
        seclen = self._parse_length(pay[1], pay[2])
        n_seclen = seclen + 6
        if self._section_incomplete(pay, pid, seclen):
            return False
        program_number = self._parse_program(pay[3], pay[4])
        pcr_pid = self._parse_pid(pay[8], pay[9])
        self.pids.pcr.add(pcr_pid)
        self.maps.pid_prgm[pcr_pid] = program_number
        proginfolen = self._parse_length(pay[10], pay[11])
        idx = 12
        n_proginfolen = proginfolen + len(self.CUEI_DESCRIPTOR)
        end = idx + proginfolen
        info_bites = pay[idx:end]
        n_info_bites = info_bites + self.CUEI_DESCRIPTOR
        while idx < end:
            # d_type = pay[idx]
            idx += 1
            d_len = pay[idx]
            idx += 1
            # d_bytes = pay[idx - 2 : idx + d_len]
            idx += d_len
        si_len = seclen - 9
        si_len -= proginfolen
        n_streams = self._parse_program_streams(si_len, pay, idx, program_number)
        self._regen_pmt(n_seclen, pcr_pid, n_proginfolen, n_info_bites, n_streams)
        return True

    def _parse_program_streams(self, si_len, pay, idx, program_number):
        """
        parse the elementary streams
        from a program
        """
        chunk_size = 5
        end_idx = (idx + si_len) - 4
        start = idx
        while idx < end_idx:
            pay, stream_type, pid, ei_len = self._parse_stream_type(pay, idx)
            idx += chunk_size
            idx += ei_len
            self.maps.pid_prgm[pid] = program_number
            self._set_scte35_pids(pid, stream_type)
        streams = pay[start:end_idx]
        return streams

    def _parse_stream_type(self, pay, idx):
        """
        extract stream pid and type
        """
        npay = pay
        stream_type = pay[idx]
        el_pid = self._parse_pid(pay[idx + 1], pay[idx + 2])
        if el_pid in self.con_pids:
            if stream_type == 6:
                npay = pay[:idx] + b"\x86" + pay[idx + 1 :]
        ei_len = self._parse_length(pay[idx + 3], pay[idx + 4])
        return npay, stream_type, el_pid, ei_len


def sixfix(arg):
    """
    fixsix converts 0x6 bin data mpegts streams
    that contain SCTE-35 data to stream type 0x86
    """
    s1 = PreFix(arg)
    six2fix = s1.decode(func=passed)
    if not six2fix:
        print2("No bin data SCTE-35 streams were found.")
    else:
        s2 = SixFix(arg)
        s2.con_pids = six2fix
        s2.convert_pid()
        print2(f'Wrote: sixfixed-{arg.rsplit("/")[-1]}')


if __name__ == "__main__":
    sixfix(sys.argv[1])
