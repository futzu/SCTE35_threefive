"""
Mpeg-TS Stream parsing class Stream
"""

import sys
from functools import partial
from .cue import Cue
from .streamtype import stream_type_map
from .tools import to_stderr


def show_cue(cue):
    """
    default function call for Stream.decode
    when a SCTE-35 packet is found.
    """
    cue.show()


class Stream:
    """
    Stream class for parsing MPEG-TS data.
    """

    _PACKET_SIZE = 188

    def __init__(self, tsdata, show_null=False):
        """
        tsdata is an open file handle
        set show_null=True to include Splice Nulls

        Use like...

        from threefive import Stream

        with open("vid.ts",'rb') as tsdata:
            strm = Stream(tsdata,show_null=True)
            strm.decode()

        """
        self._tsdata = tsdata
        self.show_null = show_null
        self._scte35_pids = set()
        self._pid_prog = {}
        self._prgm_pts = {}
        self._pmt_pids = set()
        self._programs = set()
        self.info = None
        self.the_program = None
        self.cue = None
        self.pat = None
        self.pmt = None

    def _find_start(self):
        """
        handles partial packets
        """
        sync_byte = b"G"
        while self._tsdata:
            one = self._tsdata.read(1)
            if not one:
                raise Exception("No Packets Found")
            if one == sync_byte:
                if self._tsdata.read(self._PACKET_SIZE - 1):
                    return True
        raise Exception("No Packets Found")

    def decode(self, func=show_cue):
        """
        Stream.decode reads self.tsdata to find SCTE35 packets.
        func can be set to a custom function that accepts
        a threefive.Cue instance as it's only argument.
        """
        self._find_start()
        for pkt in iter(partial(self._tsdata.read, self._PACKET_SIZE), b""):
            cue = self._parser(pkt)
            if cue:
                if not func:
                    return cue
                func(cue)

    def decode_next(self):
        """
        Stream.decode_next returns the next
        SCTE35 cue as a threefive.Cue instance.
        """
        cue = self.decode(func=False)
        if cue:
            return cue

    def decode_program(self, the_program, func=show_cue):
        """
        Stream.decode_program limits SCTE35 parsing
        to a specific MPEGTS program.
        """
        self.the_program = the_program
        self.decode(func)

    def decode_proxy(self, func=show_cue):
        """
        Stream.decode_proxy writes all ts packets are written to stdout
        for piping into another program like mplayer.
        threefive always prints messages and such to stderr.
        """
        self._find_start()
        for pkt in iter(partial(self._tsdata.read, self._PACKET_SIZE), b""):
            sys.stdout.buffer.write(pkt)
            cue = self._parser(pkt)
            if cue:
                func(cue)

    def show(self):
        """
        displays all programs and stream mappings
        """
        self.info = True
        self.decode()

    def _mk_packet_data(self, pid):
        """
        creates packet_data dict
        to pass to a threefive.Cue instance
        """
        packet_data = {}
        packet_data["pid"] = pid
        if pid in self._pid_prog:
            prgm = self._pid_prog[pid]
            packet_data["program"] = prgm
            if prgm in self._prgm_pts:
                pts = self._prgm_pts[prgm] / 90000.0
                packet_data["pts"] = round(pts, 6)
        return packet_data

    @staticmethod
    def _janky_parse(payload, marker, prefix):
        """
        _janky_parse splits payload on first marker
        and then joins prefix and everything after marker.
        """
        try:
            payload = b"".join([prefix, payload.split(marker, 1)[1]])
        except:
            payload = False
        return payload

    @staticmethod
    def _mk_payload(pkt):
        """
        _mk_payload checks if
        the adaptive field control flag is set
        and sets payload size accordingly
        """
        afc = (pkt[3] >> 5) & 1
        if afc:
            afl = pkt[4]
            payload = pkt[4 + afl :]
        else:
            payload = pkt[4:]
        return payload

    @staticmethod
    def _parse_pid(byte1, byte2):
        """
        parse a 13 bit pid value
        """
        return (byte1 << 8 | byte2) & 0x01FFF

    @staticmethod
    def _parse_length(byte1, byte2):
        """
        parse a 12 bit length value
        """
        return ((byte1 & 0xF) << 8) | byte2

    @staticmethod
    def _parse_program_number(byte1, byte2):
        """
        parse a 16 bit progrsm number value
        """
        return (byte1 << 8) | byte2

    def _parser(self, pkt):
        """
        parse pid from pkt and
        route it appropriately.
        """
        pid = self._parse_pid(pkt[1], pkt[2])
        payload = self._mk_payload(pkt)
        if pid == 0:
            self._program_association_table(payload)
            return None
        if pid in self._pmt_pids:
            self._program_map_table(payload, pid)
            return None
        if pid in self._scte35_pids:
            return self._parse_scte35(payload, pid)
        if pid in self._pid_prog:
            if (pkt[1] >> 6) & 1:
                self._parse_pusi(pkt, pid)
                return None
        return None

    def _parse_pts(self, pkt, pid):
        """
        parse pts and store by program key
        in the dict Stream._pid_pts
        """
        pts = ((pkt[13] >> 1) & 7) << 30
        pts |= ((pkt[14] << 7) | (pkt[15] >> 1)) << 15
        pts |= (pkt[16] << 7) | (pkt[17] >> 1)
        prgm = self._pid_prog[pid]
        self._prgm_pts[prgm] = pts

    def _parse_pusi(self, pkt, pid):
        """
        used to determine if pts data is available.
        """
        if pkt[6] & 1:
            if pkt[10] & 0x80:
                if pkt[11] & 0x80:
                    if pkt[13] & 0x20:
                        self._parse_pts(pkt, pid)

    def _parse_scte35(self, payload, pid):
        """
        parse a scte35 cue from one or more packets
        """
        if not self.cue:
            payload = self._janky_parse(payload, b"\xfc0", b"\xfc0")
            if not payload:
                self._scte35_pids.discard(pid)
                return None
            if (payload[13] == 0) and (not self.show_null):
                return None
            packet_data = self._mk_packet_data(pid)
            self.cue = Cue(payload[:14], packet_data)
            self.cue.mk_info_section(payload[:14])
            self.cue.bites += payload[14:]
        else:
            self.cue.bites += payload
        if (self.cue.info_section.section_length + 3) <= len(self.cue.bites):
            self.cue.decode()
            cue = self.cue
            self.cue = None
            return cue
        return None

    def _program_association_table(self, payload):
        """
        parse program association table ( pid 0 )
        to program to program table pid mappings.
        """
        if not self.pat:
            self.pat = {}
            self.pat["sectionlen"] = self._parse_length(payload[2], payload[3])
            self.pat["data"] = payload[9:]
        else:
            self.pat["data"] += payload
        if len(self.pat["data"]) < self.pat["sectionlen"]:
            return
        pat_data = self.pat["data"]
        sec_len = self.pat["sectionlen"]
        sec_len -= 5  # bytes not read
        sec_len -= 4  # skip CRC at the end
        chunk_size = 4  # 4 bytes per program -> pid mapping
        idx = 0
        while idx < sec_len:
            program_number = self._parse_program_number(
                pat_data[idx], pat_data[idx + 1]
            )
            a_pid = self._parse_pid(pat_data[idx + 2], pat_data[idx + 3])
            if program_number != 0:
                self._pmt_pids.add(a_pid)
            idx += chunk_size
        self.pat = None

    def _program_map_table(self, payload, pid):
        """
        parse program maps for streams
        """
        if self.pmt:
            # Handle PMT split over multiple packets
            tail = payload[: payload[0]]
            payload = self.pmt + tail
            self.pmt = None
        payload = self._janky_parse(payload, b"\x02", b"\x00\x02")
        if not payload:
            return None
        # table_id = payload[1]
        # section_syntax_indicator = payload[2] >> 7
        sectioninfolen = self._parse_length(payload[2], payload[3])
        if sectioninfolen + 4 > len(payload):
            self.pmt = payload
            return None
        program_number = self._parse_program_number(payload[4], payload[5])
        # version = payload[6] >> 1 & 31
        # current_next = payload[6] & 1
        if self.the_program and (program_number != self.the_program):
            return None
        # section_number = payload[7]
        # last_section_number = payload[8]
        pcr_pid = self._parse_pid(payload[9], payload[10])
        if self.info:
            if program_number not in self._programs:
                to_stderr(
                    f"\nProgram {program_number}\n\tPMT pid: {pid}\tPCR pid: {pcr_pid}"
                )
        proginfolen = self._parse_length(payload[11], payload[12])
        idx = 13
        idx += proginfolen
        si_len = sectioninfolen - 9
        si_len -= proginfolen  # Skip descriptors
        self._parse_program_streams(si_len, payload, idx, program_number)

    def _parse_program_streams(self, si_len, payload, idx, program_number):
        """
        parse the elementary streams
        from a program
        """
        if program_number not in self._programs:
            self._programs.add(program_number)
            chunk_size = 5  # 5 bytes for stream_type info
            end_idx = (idx + si_len) - chunk_size
            while idx < end_idx:
                stream_type, pid, ei_len = self._parse_stream_type(payload, idx)
                idx += chunk_size
                idx += ei_len
                self._pid_prog[pid] = program_number
                if self.info:
                    self._show_program_stream(pid, stream_type)
                self._chk_pid_stream_type(pid, stream_type)
        else:
            if self.info:
                # seek to end of stream
                self._tsdata.seek(0, 2)

    def _parse_stream_type(self, payload, idx):
        """
        extract stream pid and type
        """
        stream_type = hex(payload[idx])  # 1 byte
        el_pid = self._parse_pid(payload[idx + 1], payload[idx + 2])  # 2 bytes
        ei_len = self._parse_length(payload[idx + 3], payload[idx + 4])  # 2 bytes
        return stream_type, el_pid, ei_len

    @staticmethod
    def _show_program_stream(pid, stream_type):
        """
        print program -> stream mappings
        """
        streaminfo = f"[{stream_type}] Reserved or Private"
        if stream_type in stream_type_map:
            streaminfo = f"[{stream_type}] {stream_type_map[stream_type]}"
        to_stderr(f"\t{pid}: {streaminfo}")

    def _chk_pid_stream_type(self, pid, stream_type):
        """
        if stream_type is 0x06 or 0x86
        add it to self._scte35_pids.
        """
        if stream_type in ["0x6", "0x86"]:
            self._scte35_pids.add(pid)
