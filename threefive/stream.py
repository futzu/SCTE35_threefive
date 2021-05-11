"""
Mpeg-TS Stream parsing class Stream
"""

import sys
from functools import partial
from .cue import Cue


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
        tsdata is an open file handle
        set show_null=False to exclude Splice Nulls

        Use like...

        from threefive import Stream

        with open("vid.ts",'rb') as tsdata:
            strm = Stream(tsdata,show_null=False)
            strm.decode()

        """
        self._tsdata = tsdata
        self.show_null = show_null
        self.info = None
        self.the_program = None
        self._pids = {"ignore": set(), "pmt": set(), "scte35": set()}
        self._pid_prog = {}
        self._prgm_pts = {}
        self._cue = None
        self._last_pat = b""
        self._pmt = {}
        self._last_pmt = {}

    def __repr__(self):
        return str(vars(self))

    def _find_start(self):
        """
        handles partial packets
        """
        sync_byte = b"G"
        while self._tsdata:
            one = self._tsdata.read(1)
            if not one:
                return False
            if one == sync_byte:
                if self._tsdata.read(self._PACKET_SIZE - 1):
                    return True
        return False

    def fu(self, func=show_cue):
        number_of_pkts = 1000
        pkt_count = self._PACKET_SIZE * number_of_pkts
        if not self._find_start():
            return False
        for chunk in iter(partial(self._tsdata.read, pkt_count), b""):
            clist = [
                self._parser(chunk[i : i + self._PACKET_SIZE])
                for i in range(0, len(chunk), self._PACKET_SIZE)
            ]
            # if not func:
            #   return [ cue for cue in clist if cue]
            [func(cue) for cue in clist if cue]

    def decode(self, func=show_cue):
        """
        Stream.decode reads self.tsdata to find SCTE35 packets.
        func can be set to a custom function that accepts
        a threefive.Cue instance as it's only argument.
        """
        if not self._find_start():
            return False
        for pkt in iter(partial(self._tsdata.read, self._PACKET_SIZE), b""):
            cue = self._parser(pkt)
            if cue:
                if not func:
                    return cue
                func(cue)
        return

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
        threefive always prints messages and such to stderr.
        """
        if not self._find_start():
            return False
        for pkt in iter(partial(self._tsdata.read, self._PACKET_SIZE), b""):
            sys.stdout.buffer.write(pkt)
            cue = self._parser(pkt)
            if cue:
                func(cue)
        return

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
        prgm = self._pid_prog[pid]
        packet_data = {"pid": hex(pid), "program": prgm}
        if prgm in self._prgm_pts:
            pts = round((self._prgm_pts[prgm] / 90000.0), 6)
            packet_data["pts"] = pts
        return packet_data

    @staticmethod
    def _split_by_idx(payload, marker):
        """
        _split_by_idx splits payload at
        first index of marker.
        """
        try:
            return payload[payload.index(marker) :]
        except:
            return False

    @staticmethod
    def _parse_payload(pkt):
        """
        _parse_payload checks if
        the adaptive field control flag is set
        and sets payload size accordingly
        """
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
    def _parse_program_number(byte1, byte2):
        """
        parse a 16 bit program number value
        """
        return (byte1 << 8) | byte2

    @staticmethod
    def _parse_pusi(pkt):
        """
        check if Pusi is set on packet.
        """
        return (pkt[1] >> 6) & 1

    def _parser(self, pkt):
        """
        parse pid from pkt and
        route it appropriately.
        """
        pid = self._parse_pid(pkt[1], pkt[2])
        if pid in self._pids["ignore"]:
            return None
        if pid == 0:
            return self._chk_pat_payload(pkt)
        if pid in self._pids["pmt"]:
            return self._chk_pmt_payload(pkt, pid)
        if self.info:
            return None
        if pid in self._pids["scte35"]:
            return self._parse_scte35(pkt, pid)
        # for PTS
        if pid in self._pid_prog:
            return self._parse_pts(pkt, pid)

    def _chk_pat_payload(self, pkt):
        """
        Compare PAT packet payload
        to the last PAT packet payload
        before parsing
        """
        payload = self._parse_payload(pkt)
        if payload == self._last_pat:
            return None
        self._last_pat = payload
        self._program_association_table(payload)
        return None

    def _chk_pmt_payload(self, pkt, pid):
        """
        Use pid to compare PMT packet payloads
        to the last PMT packet payload
        before parsing
        """
        payload = self._parse_payload(pkt)
        if pid in self._last_pmt:
            if payload == self._last_pmt[pid]:
                return None
        self._last_pmt[pid] = payload
        self._program_map_table(payload, pid)
        return None

    def _parse_pts(self, pkt, pid):
        """
        parse pts and store by program key
        in the dict Stream._pid_pts
        """
        if self._parse_pusi(pkt):
            pts = ((pkt[13] >> 1) & 7) << 30
            pts |= ((pkt[14] << 7) | (pkt[15] >> 1)) << 15
            pts |= (pkt[16] << 7) | (pkt[17] >> 1)
            prgm = self._pid_prog[pid]
            self._prgm_pts[prgm] = pts

    def _parse_scte35(self, pkt, pid):
        """
        parse a scte35 cue from one or more packets
        """
        payload = self._parse_payload(pkt)
        if not self._cue:
            payload = self._split_by_idx(payload, b"\xfc0")
            if not payload:
                self._pids["scte35"].discard(pid)
                self._pids["ignore"].add(pid)
                return None
            if (payload[13] == 0) and (not self.show_null):
                return None
            packet_data = self._mk_packet_data(pid)
            self._cue = Cue(payload, packet_data)
            self._cue.info_section.decode(payload)
            self._cue.bites = payload
        else:
            self._cue.bites += payload
        # + 3 for the bytes before section starts
        if (self._cue.info_section.section_length + 3) > len(self._cue.bites):
            return None
        self._cue.decode()
        cue, self._cue = self._cue, None
        return cue

    def _program_association_table(self, payload):
        """
        parse program association table ( pid 0 )
        for program to pmt_pid mappings.
        """
        # pointer_field = payload[0]
        # table_id  = payload[1]
        section_length = self._parse_length(payload[2], payload[3])
        section_length -= 5  # payload bytes 4,5,6,7,8
        idx = 9
        chunk_size = 4
        while section_length > 4:  #  4 bytes for crc
            program_number = self._parse_program_number(payload[idx], payload[idx + 1])
            if program_number > 0:
                pmt_pid = self._parse_pid(payload[idx + 2], payload[idx + 3])
                self._pids["pmt"].add(pmt_pid)
            section_length -= chunk_size
            idx += chunk_size

    def _program_map_table(self, payload, pid):
        """
        parse program maps for streams
        """
        if pid in self._pmt:
            # Handle PMT split over multiple packets
            payload = self._pmt[pid] + payload
        payload = self._split_by_idx(payload, b"\x02")
        if not payload:
            return
        # table_id = payload[0]
        sectioninfolen = self._parse_length(payload[1], payload[2])
        if sectioninfolen + 3 > len(payload):  # +3 for bytes before sectioninfolen
            self._pmt[pid] = payload
            return
        program_number = self._parse_program_number(payload[3], payload[4])
        if self.the_program and (program_number != self.the_program):
            return
        if self.info:
            print(f"\nProgram:{program_number}")
        pcr_pid = self._parse_pid(payload[8], payload[9])
        self._pids["ignore"].add(pcr_pid)
        proginfolen = self._parse_length(payload[10], payload[11])
        idx = 12
        idx += proginfolen
        si_len = sectioninfolen - 9
        si_len -= proginfolen
        self._parse_program_streams(si_len, payload, idx, program_number)
        return

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
            self._pid_prog[pid] = program_number
            self._chk_pid_stream_type(pid, stream_type)

    def _parse_stream_type(self, payload, idx):
        """
        extract stream pid and type
        """
        stream_type = hex(payload[idx])  # 1 byte
        el_pid = self._parse_pid(payload[idx + 1], payload[idx + 2])  # 2 bytes
        ei_len = self._parse_length(payload[idx + 3], payload[idx + 4])  # 2 bytes
        return stream_type, el_pid, ei_len

    def _chk_pid_stream_type(self, pid, stream_type):
        """
        if stream_type is 0x06 or 0x86
        add it to self._scte35_pids.
        """
        if stream_type in ["0x6", "0x86"]:
            self._pids["scte35"].add(pid)
            if pid in self._pids["ignore"]:
                self._pids["ignore"].discard(pid)
            if self.info:
                if stream_type == "0x86":
                    print(f"\tPID: {pid}({hex(pid)}) Type: {stream_type} SCTE35")
                else:
                    print(f"\tPID: {pid}({hex(pid)}) Type: {stream_type}")
