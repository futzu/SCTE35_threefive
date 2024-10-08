"""
Mpeg-TS Stream parsing class Stream
"""

import sys

from functools import partial
from new_reader import reader
from .stuff import print2
from .cue import Cue
from .packetdata import PacketData
from .streamtypes import streamtype_map


def no_op(cue):
    """
    no_op is just a dummy func to pass to Stream.decode()
    to suppress output.
    """
    return cue


def show_cue(cue):
    """
    default function call for Stream.decode
    when a SCTE-35 packet is found.
    """
    cue.show()


def show_cue_stderr(cue):
    """
    print2 cue data to sys.stderr
    for Stream.decode_proxy
    """
    cue.to_stderr()


class ProgramInfo:
    """
    ProgramInfo is a class to
    hold Program information
    for use with Stream.show()
    """

    def __init__(self, pid=None, pcr_pid=None):
        self.pid = pid
        self.pcr_pid = pcr_pid
        self.provider = b""
        self.service = b""
        self.streams = {}  # pid to stream_type mapping

    def show(self):
        """
        show print2 the Program Infomation
        in a familiar format.
        """
        serv = self.service.decode(errors="ignore")
        prov = self.provider.decode(errors="ignore")
        print2("")
        print2(f"\tService:  {serv}")
        print2(f"\tProvider: {prov}")
        print2(f"\tPid:      {self.pid}")
        print2(f"\tPcr Pid:  {self.pcr_pid}")
        print2("\tStreams:")
        # sorted_dict = {k:my_dict[k] for k in sorted(my_dict)})
        keys = sorted(self.streams)
        print2("\t  Pid\t\tType")
        for k in keys:
            vee = int(self.streams[k], base=16)
            if vee in streamtype_map:
                vee = f"{hex(vee)}\t{streamtype_map[vee]}"
            else:
                vee = f"{vee} Unknown"
            print2(f"\t  {k} [{hex(k)}]\t{vee}")


class Pids:
    """
    Pids holds sets of pids for pat,pcr,pmt, and scte35
    """

    SDT_PID = 0x11
    PAT_PID = 0x00

    def __init__(self):
        self.pcr = set()
        self.pmt = set()
        self.scte35 = set()
        self.maybe_scte35 = set()
        self.tables = set()
        self.tables.add(self.PAT_PID)
        self.tables.add(self.SDT_PID)


class Maps:
    """
    Maps holds mappings
    pids mapped to continuity_counters,
    programs, partial tables and last payload.

    programs mapped to pcr and pts

    """

    def __init__(self):
        self.pid_cc = {}
        self.pid_prgm = {}
        self.prgm_pcr = {}
        self.prgm_pts = {}
        self.prgm = {}
        self.partial = {}
        self.last = {}


class Stream:
    """
    Stream class for parsing MPEG-TS data.
    """

    # the _CONST are deprecated
    # please switch to CONST

    _PACKET_SIZE = PACKET_SIZE = 188
    _SYNC_BYTE = SYNC_BYTE = 0x47

    # tids

    _PMT_TID = PMT_TID = b"\x02"
    _SCTE35_TID = SCTE35_TID = b"\xfc"
    _SDT_TID = SDT_TID = b"\x42"
    ROLLOVER = 8589934591  # 95443.717678
    ROLLOVER9K = 95443.717678
    SCTE35_PES_START = b"\x00\x00\x01\xfc"

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
            self._tsdata = reader(tsdata)
        else:
            self._tsdata = tsdata
        self.show_null = show_null
        self.start = {}
        self.info = False
        self.the_program = None
        self.the_scte35_pids = []
        self.pids = Pids()
        self.maps = Maps()

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def as_90k(ticks):
        """
        as_90k returns ticks as 90k clock time
        """
        return round((ticks / 90000.0), 6)

    @staticmethod
    def _pusi_flag(pkt):
        return pkt[1] & 0x40

    @staticmethod
    def _afc_flag(pkt3):
        return pkt3 & 0x20

    @staticmethod
    def _pcr_flag(pkt):
        return pkt[5] & 0x10

    @staticmethod
    def _spi_flag(pkt):
        return pkt[5] & 0x20

    @staticmethod
    def _pts_flag(pay):
        # uses pay not pkt
        return pay[7] & 0x80

    @staticmethod
    def _parse_length(byte1, byte2):
        """
        parse a 12 bit length value
        """
        return (byte1 & 0xF) << 8 | byte2

    @staticmethod
    def _parse_pid(byte1, byte2):
        """
        parse a 13 bit pid value
        """
        pid = (byte1 & 0x1F) << 8 | byte2
        return pid

    @staticmethod
    def _parse_program(byte1, byte2):
        """
        parse a 16 bit program number value
        """
        return (byte1 << 8) | byte2

    @staticmethod
    def _split_by_idx(pay, marker):
        try:
            return pay[pay.index(marker) :]
        except:
            return False

    def _find_start(self):
        """
        _find_start locates the first SYNC_BYTE
        parses 1 packet and returns True
        if SYNC_BYTE is found.
        """
        while self._tsdata:
            one = self._tsdata.read(1)
            if not one:
                print2("\nNo Stream Found. \n")
                return False
            if one[0] == self.SYNC_BYTE:
                tail = self._tsdata.read(self.PACKET_SIZE - 1)
                if tail:
                    self._parse(one + tail)
                    return True
        return False

    def iter_pkts(self, num_pkts=1):
        """
        iter_pkts iterates a mpegts stream into packets
        """
        return iter(partial(self._tsdata.read, self.PACKET_SIZE * num_pkts), b"")

    def _mk_pkts(self, chunk):
        return [
            self._parse(chunk[i : i + self.PACKET_SIZE])
            for i in range(0, len(chunk), self.PACKET_SIZE)
        ]

    def decode(self, func=show_cue):
        """
        Stream.decode reads self.tsdata to find SCTE35 packets.
        func can be set to a custom function that accepts
        a threefive.Cue instance as it's only argument.
        """
        if not self._find_start():
            return False
        for pkt in self.iter_pkts():
            cue = self._parse(pkt)
            if cue:
                func(cue)
        return False

    def decode_fu(self, func=show_cue):
        """
        Stream.decode_fu decodes
        num_pkts packets at a time.
        Super Fast with pypy3.
        """
        if self._find_start():
            num_pkts = 3000
            for chunk in self.iter_pkts(num_pkts=num_pkts):
                _ = [func(cue) for cue in self._mk_pkts(chunk) if cue]
                del _
        return False

    def decode_next(self):
        """
        Stream.decode_next returns the next
        SCTE35 cue as a threefive.Cue instance.
        """
        if not self._find_start():
            return False
        for pkt in self.iter_pkts():
            cue = self._parse(pkt)
            if cue:
                return cue
        return False

    def decode_program(self, the_program, func=show_cue):
        """
        Stream.decode_program limits SCTE35 parsing
        to a specific MPEGTS program.
        """
        self.the_program = the_program
        return self.decode(func)

    def decode_pids(self, scte35_pids=[], func=show_cue):
        """
        Stream.decode_pids takes a list of SCTE-35 Pids parse
        and an optional call back function to run when a Cue is found.
        if scte35_pids is not set, all scte35 pids will be parsed.
        """
        self.the_scte35_pids = scte35_pids
        return self.decode(func)

    def decode_start_time(self):
        """
        decode_start_time
        """
        self.decode(func=no_op)
        if len(self.start.values()) > 0:
            return self.start.popitem()[1]
        return False

    def proxy(self, func=show_cue_stderr):
        """
        Stream.decode_proxy writes all ts packets are written to stdout
        for piping into another program like mplayer.
        SCTE-35 cues are print2`ed to stderr.
        """
        if not self._find_start():
            return False
        for pkt in self.iter_pkts():
            cue = self._parse(pkt)
            if cue:
                func(cue)
            sys.stdout.buffer.write(pkt)
        return False

    def show(self):
        """
        displays streams that will be
        parsed for SCTE-35.
        """
        pkt_count = 0
        self.info = True
        while True:
            for pkt in self.iter_pkts():
                pkt_count += 1
                self._parse_info(pkt)
            if self.maps.prgm.keys():
                print2(f"Read {pkt_count} packets")
                sopro = sorted(self.maps.prgm.items())
                for k, vee in sopro:
                    if len(vee.streams.items()) > 0:
                        print2(f"\nProgram: {k}")
                        vee.show()
                return True

    def show_pts(self):
        """
        show_pts displays current pts by pid.
        """
        if self._find_start():
            print2("\tPID\tPTS")
            for pkt in self.iter_pkts():
                pid = self._parse_info(pkt)
                if self._pusi_flag(pkt) and pid != 0:
                    self._parse_pts(pkt, pid)
                    print(f"\t{pid}\t{self.pid2pts(pid)}", end="\r")

    def pts(self):
        """
        pts returns a dict of  program:pts
        """
        return self.maps.prgm_pts

    def pid2prgm(self, pid):
        """
        pid2prgm takes a pid,
        returns the program
        """
        prgm = 1
        if pid in self.maps.pid_prgm:
            prgm = self.maps.pid_prgm[pid]
        return prgm

    def pid2pts(self, pid):
        """
        pid2pts takes a pid
        returns the current pts
        """
        prgm = self.pid2prgm(pid)
        if prgm not in self.maps.prgm_pts:
            return False
        return self.as_90k(self.maps.prgm_pts[prgm])

    def pid2pcr(self, pid):
        """
        pid2pcr takes a pid
        returns the current pcr
        """
        prgm = self.pid2prgm(pid)
        if prgm not in self.maps.prgm_pcr:
            return False
        return self.as_90k(self.maps.prgm_pcr[prgm])

    def _unpad_afc(self, pkt):
        if self._afc_flag(pkt[3]):
            pkt = pkt[:4] + self._unpad(pkt[4:])
        return pkt

    def _unpad(self, bites):
        pad = 255
        one = 1
        if not bites:
            return b""
        if bites[0] in [pad]:
            self._unpad(bites[one:])
        return bites

    def _mk_packet_data(self, pid):
        prgm = self.maps.pid_prgm[pid]
        pdata = PacketData(pid, prgm)
        pdata.mk_pcr(self.maps.prgm_pcr)
        pdata.mk_pts(self.maps.prgm_pts)
        return pdata

    def _parse_cc(self, pkt, pid):
        last_cc = None
        c_c = pkt[3] & 0xF
        if pid in self.maps.pid_cc:
            last_cc = self.maps.pid_cc[pid]
            good = (last_cc, ((last_cc + 1) % 16))
            if c_c not in good:
                print2(f" # BAD --> pid:\t{hex(pid)}\tlast cc:\t{last_cc}\tcc:\t{c_c}")
        self.maps.pid_cc[pid] = c_c

    def _parse_pts(self, pkt, pid):
        """
        parse pts and store by program key
        in the dict Stream._pid_pts
        """
        payload = self._parse_payload(pkt)
        if len(payload) > 13:
            if self._pts_flag(payload):
                pts = (payload[9] & 14) << 29
                pts |= payload[10] << 22
                pts |= (payload[11] >> 1) << 15
                pts |= payload[12] << 7
                pts |= payload[13] >> 1
                prgm = self.pid2prgm(pid)
                self.maps.prgm_pts[prgm] = pts
                if prgm not in self.start:
                    self.start[prgm] = pts

    def _parse_pcr(self, pkt, pid):
        if self._afc_flag(pkt[3]):
            pcr = pkt[6] << 25
            pcr |= pkt[7] << 17
            pcr |= pkt[8] << 9
            pcr |= pkt[9] << 1
            pcr |= pkt[10] >> 7
            prgm = self.pid2prgm(pid)
            self.maps.prgm_pcr[prgm] = pcr

    def _parse_payload(self, pkt):
        """
        _parse_payload returns the packet payload
        """
        head_size = 4
        if self._afc_flag(pkt[3]):
            pkt = self._unpad_afc(pkt)
            afl = pkt[4]
            head_size += afl + 1  # +1 for afl byte
        return pkt[head_size:]

    def _parse_tables(self, pkt, pid):
        """
        _parse_tables parse for
        PAT, PMT,  and SDT tables
        based on pid of the pkt
        """
        pay = self._parse_payload(pkt)
        if self._same_as_last(pay, pid):
            return False
        if pid in self.pids.pmt:
            return self._parse_pmt(pay, pid)
        if pid == self.pids.PAT_PID:
            return self._parse_pat(pay)
        if pid == self.pids.SDT_PID and self.info:
            return self._parse_sdt(pay)
        return False


    def _parse_info(self, pkt):
        """
        _parse_info parses the packet for tables
        and returns the pid
        """
        pid = self._parse_pid(pkt[1], pkt[2])
        if pid in self.pids.tables:
            self._parse_tables(pkt, pid)
        return pid

    def _parse(self, pkt):
        cue = False
        pid = self._parse_info(pkt)
        #self._parse_cc(pkt, pid)
        if self._pcr_flag(pkt):
            self._parse_pcr(pkt, pid)
        if self._pusi_flag(pkt):
            self._parse_pts(pkt, pid)
        if self._pid_has_scte35(pid):
            cue = self._parse_scte35(pkt, pid)
        return cue

    def _pid_has_scte35(self,pid):
        if pid in self.pids.scte35 or pid in self.pids.maybe_scte35:
            return True
        return False

    def _chk_partial(self, pay, pid, sep):
        if pid in self.maps.partial:
            pay = self.maps.partial.pop(pid) + pay
        return self._split_by_idx(pay, sep)

    def _same_as_last(self, pay, pid):
        same = False
        if pid in self.maps.last:
            same = (False, True)[pay == self.maps.last[pid]]
        if not same:
            self.maps.last[pid] = pay
        return same

    def _section_incomplete(self, pay, pid, seclen):
        # + 3 for the bytes before section starts
        if (seclen + 3) > len(pay):
            self.maps.partial[pid] = pay
            return True
        return False

    def _parse_cue(self, pay, pid):
        packet_data = None
        packet_data = self._mk_packet_data(pid)
        cue = Cue(pay, packet_data)
        if cue.decode():
            return cue
        return False

    def _strip_scte35_pes(self, pay):
        if self.SCTE35_PES_START in pay:
            # print2(f"# Stripping PES Header from SCTE35 @ {self.pid2pts(pid)}")
            pay = pay.split(self.SCTE35_PES_START, 1)[-1]
            peslen = pay[4] + 5  # PES header length
            pay = pay[peslen:]
        return pay

    def _parse_scte35(self, pkt, pid):
        """
        parse a scte35 cue from one or more packets
        """
        pay = self._parse_payload(pkt)
        pay = self._strip_scte35_pes(pay)
        if not pay:
            return False
        pay = self._chk_partial(pay, pid, self.SCTE35_TID)
        if not pay:
            if pid in self.pids.maybe_scte35:
                self.pids.maybe_scte35.remove(pid)
            return False
        if pay[13] == self.show_null:
            return False
        seclen = self._parse_length(pay[1], pay[2])
        if self._section_incomplete(pay, pid, seclen):
            return False
        pay = pay[: seclen + 3]
        cue = self._parse_cue(pay, pid)
        return cue

    def _parse_sdt(self, pay):
        """
        _parse_sdt parses the SDT for program metadata
        """
        pay = self._chk_partial(pay, self.pids.SDT_PID, self.SDT_TID)
        if not pay:
            return False
        seclen = self._parse_length(pay[1], pay[2])
        if self._section_incomplete(pay, self.pids.SDT_PID, seclen):
            return False
        idx = 11
        while idx < seclen + 3:
            service_id = self._parse_program(pay[idx], pay[idx + 1])
            idx += 3
            dloop_len = self._parse_length(pay[idx], pay[idx + 1])
            idx += 2
            i = 0
            while i < dloop_len:
                if pay[idx] == 0x48:
                    i += 3
                    spnl = pay[idx + i]
                    i += 1
                    service_provider_name = pay[idx + i : idx + i + spnl]
                    i += spnl
                    snl = pay[idx + i]
                    i += 1
                    service_name = pay[idx + i : idx + i + snl]
                    i += snl
                    if service_id not in self.maps.prgm:
                        self.maps.prgm[service_id] = ProgramInfo()
                    pinfo = self.maps.prgm[service_id]
                    pinfo.provider = service_provider_name
                    pinfo.service = service_name
                i = dloop_len
                idx += i
                return True
        return False

    def _parse_pat(self, pay):
        """
        parse program association table
        for program to pmt_pid mappings.
        """
        pay = self._chk_partial(pay, self.pids.PAT_PID, b"")
        seclen = self._parse_length(pay[2], pay[3])
        if self._section_incomplete(pay, self.pids.PAT_PID, seclen):
            return False
        seclen -= 5  # pay bytes 4,5,6,7,8
        idx = 9
        chunk_size = 4
        while seclen > 4:  #  4 bytes for crc
            program_number = self._parse_program(pay[idx], pay[idx + 1])
            if program_number > 0:
                pmt_pid = self._parse_pid(pay[idx + 2], pay[idx + 3])
                self.pids.pmt.add(pmt_pid)
                self.pids.tables.add(pmt_pid)
            seclen -= chunk_size
            idx += chunk_size
        return True

    def _parse_pmt(self, pay, pid):
        """
        parse program maps for streams
        """
        pay = self._chk_partial(pay, pid, self.PMT_TID)
        if not pay:
            return False
        seclen = self._parse_length(pay[1], pay[2])
        if self._section_incomplete(pay, pid, seclen):
            return False
        program_number = self._parse_program(pay[3], pay[4])
        if self.the_program and (program_number != self.the_program):
            return False
        pcr_pid = self._parse_pid(pay[8], pay[9])
        if program_number not in self.maps.prgm:
            self.maps.prgm[program_number] = ProgramInfo()
        pinfo = self.maps.prgm[program_number]
        pinfo.pid = pid
        pinfo.pcr_pid = pcr_pid
        self.pids.pcr.add(pcr_pid)
        self.maps.pid_prgm[pcr_pid] = program_number
        proginfolen = self._parse_length(pay[10], pay[11])
        idx = 12 + proginfolen
        si_len = seclen - (9 + proginfolen)
        self._parse_program_streams(si_len, pay, idx, program_number)
        return True

    def _parse_program_streams(self, si_len, pay, idx, program_number):
        """
        parse the elementary streams
        from a program
        """
        # 5 bytes for stream_type info
        chunk_size = 5
        end_idx = (idx + si_len) - chunk_size
        while idx < end_idx:
            stream_type, pid, ei_len = self._parse_stream_type(pay, idx)
            pinfo = self.maps.prgm[program_number]
            pinfo.streams[pid] = stream_type
            idx += chunk_size + ei_len
            self.maps.pid_prgm[pid] = program_number

    def _parse_stream_type(self, pay, idx):
        """
        extract stream pid and type
        """
        stream_type = hex(pay[idx])
        el_pid = self._parse_pid(pay[idx + 1], pay[idx + 2])
        ei_len = self._parse_length(pay[idx + 3], pay[idx + 4])
        self._set_scte35_pids(el_pid, stream_type)
        return stream_type, el_pid, ei_len

    def _set_scte35_pids(self, pid, stream_type):
        """
        if stream_type is 0x06 or 0x86
        add it to self._scte35_pids.
        """
        if stream_type in ["0x86"]:
            self.pids.scte35.add(pid)
        if stream_type in ["0x06", "0x6"]:
            self.pids.maybe_scte35.add(pid)
