"""
Mpeg-TS Stream parsing class Stream
"""

import sys
from functools import partial
import urllib
from .cue import Cue
from .packetdata import PacketData


def show_cue(cue):
    """
    default function call for Stream.decode
    when a SCTE-35 packet is found.
    """
    cue.show()


def show_cue_stderr(cue):
    """
    print cue data to sys.stderr
    for Stream.decode_proxy
    """
    cue.to_stderr()


class Stream:
    """
    Stream class for parsing MPEG-TS data.
    """

    _PACKET_SIZE = 188

    def __init__(self, tsdata, show_null=True):
        """
        tsdata is an file or http/https url
        set show_null=False to exclude Splice Nulls

        Use like...

        from threefive import Stream
        strm = Stream("vid.ts",show_null=False)
        strm.decode()

        """
        if isinstance(tsdata, str):
            self._tsdata = self._reader(tsdata)
        else:
            self._tsdata = tsdata
        self.show_null = show_null
        self.show_start = False
        self.info = None
        self.the_program = None
        self._pids = {"pcr": set(), "pmt": set(), "scte35": set()}
        self._pid_prgm = {}
        self._prgm_pcr = {}
        self._prgm_pts = {}
        self._cue = None
        self._partial = {}
        self._last = {}

    def __repr__(self):
        return str(vars(self))

    @staticmethod
    def _reader(uri):
        if uri.startswith("http"):
            return urllib.request.urlopen(uri)
        return open(uri, "rb")

    def _find_start(self):
        sync_byte = 0x47
        while self._tsdata:
            one = self._tsdata.read(1)
            if not one:
                return False
            if one[0] == sync_byte:
                if self._tsdata.read(self._PACKET_SIZE - 1):
                    return True
        return False

    def decode(self, func=show_cue):
        """
        Stream.decode reads self.tsdata to find SCTE35 packets.
        func can be set to a custom function that accepts
        a threefive.Cue instance as it's only argument.
        """
        if self._find_start():
            for pkt in iter(partial(self._tsdata.read, self._PACKET_SIZE), b""):
                cue = self._parse(pkt)
                if cue:
                    if not func:
                        return cue
                    func(cue)
        self._tsdata.close()
        return None

    def _mk_pkts(self, chunk):
        return [
            self._parse(chunk[i : i + self._PACKET_SIZE])
            for i in range(0, len(chunk), self._PACKET_SIZE)
        ]

    def decode_fu(self, func=show_cue):
        """
        Stream.decode_fu decodes
        1384 packets at a time.
        """
        pkts = 1384
        if self._find_start():
            for chunk in iter(
                partial(self._tsdata.read, (self._PACKET_SIZE * pkts)), b""
            ):
                [func(cue) for cue in self._mk_pkts(chunk) if cue]
        self._tsdata.close()

    def decode_next(self):
        """
        Stream.decode_next returns the next
        SCTE35 cue as a threefive.Cue instance.
        """
        cue = self.decode(func=False)
        if cue:
            return cue
        return None

    def decode_program(self, the_program, func=show_cue):
        """
        Stream.decode_program limits SCTE35 parsing
        to a specific MPEGTS program.
        """
        self.the_program = the_program
        return self.decode(func)

    def decode_proxy(self, func=show_cue_stderr):
        """
        Stream.decode_proxy writes all ts packets are written to stdout
        for piping into another program like mplayer.
        SCTE-35 cues are printed to stderr.
        """
        if self._find_start():
            for pkt in iter(partial(self._tsdata.read, self._PACKET_SIZE), b""):
                cue = self._parse(pkt)
                if cue:
                    func(cue)
                sys.stdout.buffer.write(pkt)
        self._tsdata.close()

    def strip_scte35(self, func=show_cue_stderr):
        """
        Stream.strip_scte35 works just likle Stream.decode_proxy,
        MPEGTS packets, ( Except the SCTE-35 packets) ,
        are written to stdout after being parsed.
        SCTE-35 cues are printed to stderr.
        """
        if self._find_start():
            for pkt in iter(partial(self._tsdata.read, self._PACKET_SIZE), b""):
                cue = self._parse(pkt)
                if cue:
                    func(cue)
                else:
                    sys.stdout.buffer.write(pkt)
        self._tsdata.close()

    def show(self):
        """
        displays streams that will be
        parsed for SCTE-35.
        """
        self.info = True
        self.decode(func=False)

    def decode_start_time(self):
        """
        displays streams that will be
        parsed for SCTE-35.
        """
        self.show_start = True
        start = self.decode(func=False)
        if start:
            return start
        return None

    def _mk_packet_data(self, pid):
        prgm = self._pid_prgm[pid]
        pdata = PacketData(pid, prgm)
        pdata.mk_pcr(self._prgm_pcr)
        pdata.mk_pts(self._prgm_pts)
        return pdata

    @staticmethod
    def _split_by_idx(payload, marker):
        try:
            return payload[payload.index(marker) :]
        except (LookupError, TypeError, ValueError):
            return False

    @staticmethod
    def _parse_payload(pkt):
        head_size = 4
        afc = (pkt[3] >> 5) & 1
        if afc:
            afl = pkt[4]
            head_size += afl + 1  # +1 for afl byte
        return pkt[head_size:]

    @staticmethod
    def _parse_length(byte1, byte2):
        """
        parse a 12 bit length value
        """
        return ((byte1 & 0xF) << 8) | byte2

    @staticmethod
    def _parse_pid(byte1, byte2):
        """
        parse a 13 bit pid value
        """
        return (byte1 << 8 | byte2) & 0x01FFF

    @staticmethod
    def _parse_program(byte1, byte2):
        """
        parse a 16 bit program number value
        """
        return (byte1 << 8) | byte2

    @staticmethod
    def _parse_pusi(byte1):
        """
        used to determine if pts data is available.
        """
        return (byte1 >> 6) & 1

    def _parse_pts(self, pkt, pid):
        """
        parse pts and store by program key
        in the dict Stream._pid_pts
        """
        if self._parse_pusi(pkt[1]):
            if pkt[6] & 1:
                pts = ((pkt[13] >> 1) & 7) << 30
                pts |= pkt[14] << 22
                pts |= (pkt[15] >> 1) << 15
                pts |= pkt[16] << 7
                pts |= pkt[17] >> 1
                prgm = self._pid_prgm[pid]
                self._prgm_pts[prgm] = pts

    def _parse_pcr(self, pkt, pid):
        """
        Parse PCR base and ext from
        PCR PID packets
        """
        if (pkt[3] >> 5) & 1:
            if (pkt[5] >> 4) & 1:
                pcr = pkt[6] << 25
                pcr |= pkt[7] << 17
                pcr |= pkt[8] << 9
                pcr |= pkt[9] << 1
                pcr |= pkt[10] >> 7
                prgm = self._pid_prgm[pid]
                self._prgm_pcr[prgm] = pcr
                if self.show_start:
                    return round((pcr / 90000.0), 6)

    def _parse(self, pkt):
        pid = self._parse_pid(pkt[1], pkt[2])
        if pid == 0:
            self._chk_pat_payload(pkt, pid)
        if pid in self._pids["pmt"]:
            self._chk_pmt_payload(pkt, pid)
        if pid in self._pid_prgm:
            pcr = self._parse_pcr(pkt, pid)
            if pcr:
                return pcr
            self._parse_pts(pkt, pid)
            if pid in self._pids["scte35"]:
                return self._parse_scte35(pkt, pid)

    def _chk_partial(self, payload, pid):
        if pid in self._partial:
            payload = self._partial.pop(pid) + payload
        return payload

    def _chk_last(self, payload, pid):
        if pid in self._last:
            return payload == self._last[pid]
        self._last[pid] = payload
        return False

    def _chk_pat_payload(self, pkt, pid):
        payload = self._parse_payload(pkt)
        if not self._chk_last(payload, pid):
            self._program_association_table(payload)

    def _chk_pmt_payload(self, pkt, pid):
        payload = self._parse_payload(pkt)
        if not self._chk_last(payload, pid):
            self._program_map_table(payload, pid)

    def _parse_cue(self, payload, pid):
        packet_data = self._mk_packet_data(pid)
        self._cue = Cue(payload, packet_data)
        self._cue.info_section.decode(payload)
        self._cue.bites = payload

    def _parse_scte35(self, pkt, pid):
        """
        parse a scte35 cue from one or more packets
        """
        payload = self._parse_payload(pkt)
        if not self._cue:
            payload = self._split_by_idx(payload, b"\xfc0")
            if not payload:
                self._pids["scte35"].remove(pid)
                return None
            if payload[13] == self.show_null:
                return None
            self._parse_cue(payload, pid)
        else:
            self._cue.bites = self._chk_partial(payload, pid)
        # + 3 for the bytes before section starts
        if (self._cue.info_section.section_length + 3) > len(self._cue.bites):
            self._partial[pid] = payload
            return None
        if not self._cue.decode():
            self._pids["scte35"].remove(pid)
            return None
        cue, self._cue = self._cue, None
        return cue

    def _program_association_table(self, payload):
        """
        parse program association table ( pid 0 )
        for program to pmt_pid mappings.
        """
        pid = 0
        payload = self._chk_partial(payload, pid)
        section_length = self._parse_length(payload[2], payload[3])
        if section_length + 3 > len(payload):
            self._partial[pid] = payload
            return None
        section_length -= 5  # payload bytes 4,5,6,7,8
        idx = 9
        chunk_size = 4
        while section_length > 4:  #  4 bytes for crc
            program_number = self._parse_program(payload[idx], payload[idx + 1])
            if program_number > 0:
                pmt_pid = self._parse_pid(payload[idx + 2], payload[idx + 3])
                self._pids["pmt"].add(pmt_pid)
            section_length -= chunk_size
            idx += chunk_size

    def _program_map_table(self, payload, pid):
        """
        parse program maps for streams
        """
        payload = self._chk_partial(payload, pid)
        payload = self._split_by_idx(payload, b"\x02")
        if not payload:
            return
        sectioninfolen = self._parse_length(payload[1], payload[2])
        if sectioninfolen + 3 > len(payload):
            self._partial[pid] = payload
            return
        program_number = self._parse_program(payload[3], payload[4])
        if self.the_program and (program_number != self.the_program):
            return
        pcr_pid = self._parse_pid(payload[8], payload[9])
        if self.info:
            print(f"\nProgram:{program_number}\n")
        self._pids["pcr"].add(pcr_pid)
        proginfolen = self._parse_length(payload[10], payload[11])
        idx = 12
        idx += proginfolen
        si_len = sectioninfolen - 9
        si_len -= proginfolen
        self._parse_program_streams(si_len, payload, idx, program_number)

    def _parse_program_streams(self, si_len, payload, idx, program_number):
        """
        parse the elementary streams
        from a program
        """
        # 5 bytes for stream_type info
        chunk_size = 5
        end_idx = (idx + si_len) - chunk_size
        while idx < end_idx:
            stream_type, pid, ei_len = self._parse_stream_type(payload, idx)
            idx += chunk_size
            idx += ei_len
            self._pid_prgm[pid] = program_number
            self._chk_pid_stream_type(pid, stream_type)

    def _parse_stream_type(self, payload, idx):
        """
        extract stream pid and type
        """
        stream_type = hex(payload[idx])
        el_pid = self._parse_pid(payload[idx + 1], payload[idx + 2])
        ei_len = self._parse_length(payload[idx + 3], payload[idx + 4])
        return stream_type, el_pid, ei_len

    def _chk_pid_stream_type(self, pid, stream_type):
        """
        if stream_type is 0x06 or 0x86
        add it to self._scte35_pids.
        """
        if stream_type in ["0x6", "0x86"]:
            self._pids["scte35"].add(pid)
        if self.info:
            stream_stuff = ""
            if stream_type == "0x86":
                stream_stuff += " SCTE35 "
            if pid in self._pids["pcr"]:
                stream_stuff += " PCR "
            print(f"   {pid} [{hex(pid)}] Type: {stream_type}  {stream_stuff}")
