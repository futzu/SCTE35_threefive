"""
Mpeg-TS Stream parsing class Stream
"""
import sys
from functools import partial
from .cue import Cue
from .packetdata import PacketData
from .reader import reader

"""
stream types for program streams.
"""
streamtype_map = {
    "0x2": "MP2 Video",
    "0x3": "MP2 Audio",
    "0x4": "MP2 Audio",
    "0x6": "PES Packets/Private Data",
    "0xf": "AAC Audio",
    "0x1b": "AVC Video",
    "0x81": "AC3 Audio ",
    "0x86": "SCTE35 Data",
    "0xc0": "Unknown",
}


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
    print cue data to sys.stderr
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
        show print the Program Infomation
        in a familiar format.
        """
        serv = self.service.decode(errors="ignore")
        prov = self.provider.decode(errors="ignore")
        print(f"    Service:\t{ serv}\n    Provider:\t{prov}")
        print(f"    Pcr Pid:\t{self.pcr_pid}")
        print("    Streams:")
        # sorted_dict = {k:my_dict[k] for k in sorted(my_dict)})
        keys = sorted(self.streams)
        for k in keys:
            vee = self.streams[k]
            if vee in streamtype_map:
                vee = f"{vee} {streamtype_map[vee]}"
            else:
                vee = f"{vee} Unknown"
            print(f"\t\tPid: {k}[{hex(k)}]\tType: {vee}")
        print()


class Stream:
    """
    Stream class for parsing MPEG-TS data.
    """

    _PACKET_SIZE = 188
    _SYNC_BYTE = 0x47
    # pids
    _SDT_PID = 0x11
    _PAT_PID = 0x00
    # tids
    _PMT_TID = b"\x02"
    _SCTE35_TID = b"\xFC0"
    _SDT_TID = b"\x42"
    # pts
    ROLLOVER = 8589934591  # 95443.717678
    _NO_PTS_PIDS = [188, 190, 191, 240, 241, 242, 248]

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
        self.chk_cc = False
        self.start = {}
        self.info = None
        self.the_program = None
        self._pids = {"pcr": set(), "tables": set(), "pmt": set(), "scte35": set()}
        self._pids["tables"].add(self._PAT_PID)
        self._pids["tables"].add(self._SDT_PID)
        self._pid_cc = {}
        self._pid_prgm = {}
        self._prgm_pcr = {}
        self._prgm_pts = {}
        self._prgm = {}
        self._partial = {}
        self._last = {}

    def __repr__(self):
        return str(self.__dict__)

    def _find_start(self):
        while self._tsdata:
            one = self._tsdata.read(1)
            if not one:
                sys.stderr.buffer.write(
                    b"\nNo Stream Found\n",
                )
                return False
            if one[0] == self._SYNC_BYTE:
                tail = self._tsdata.read(self._PACKET_SIZE - 1)
                if tail:
                    self._parse(one + tail)
                    return True

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

    def _mk_pkts(self, chunk):
        return [
            self._parse(chunk[i : i + self._PACKET_SIZE])
            for i in range(0, len(chunk), self._PACKET_SIZE)
        ]

    def dump(self, fname):
        """
        Stream.dump dumps all the packets to a file.
        Useful for live streams.
        """
        if not self._find_start():
            return False
        with open(fname, "wb") as dumpfile:
            for pkt in iter(partial(self._tsdata.read, self._PACKET_SIZE * 30000), b""):
                dumpfile.write(pkt)

    def decode_fu(self, func=show_cue):
        """
        Stream.decode_fu decodes
        num_pkts packets at a time.
        """
        num_pkts = 10016
        if not self._find_start():
            return False
        for chunk in iter(
            partial(self._tsdata.read, (self._PACKET_SIZE * num_pkts)), b""
        ):
            _ = [func(cue) for cue in self._mk_pkts(chunk) if cue]
            del _
        self._tsdata.close()

    def decode_next(self):
        """
        Stream.decode_next returns the next
        SCTE35 cue as a threefive.Cue instance.
        """
        cue = self.decode(func=False)
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
        Stream.strip_scte35 works just like Stream.decode_proxy,
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
        if self._find_start():
            for pkt in iter(partial(self._tsdata.read, self._PACKET_SIZE), b""):
                self._parse_info(pkt)
            sopro = sorted(self._prgm.items())
            for k, vee in sopro:
                if len(vee.streams.items()) > 0:
                    print(f"Program: {k}")
                    vee.show()

    def decode_start_time(self):
        """
        displays streams that will be
        parsed for SCTE-35.
        """
        #     self.decode(func=no_op)
        if len(self.start.values()) > 0:
            return self.start.popitem()[1]
        return False

    def _mk_packet_data(self, pid):
        prgm = self._pid_prgm[pid]
        pdata = PacketData(pid, prgm)
        pdata.mk_pcr(self._prgm_pcr)
        pdata.mk_pts(self._prgm_pts)
        return pdata

    @staticmethod
    def _afc_flag(pkt):
        return pkt[3] & 0x20

    @staticmethod
    def _pcr_flag(pkt):
        return pkt[5] & 0x10

    @staticmethod
    def _pts_flag(pay):
        # uses pay not pkt
        return pay[7] & 0x80

    @staticmethod
    def _pusi_flag(pkt):
        return pkt[1] & 0x40

    @staticmethod
    def _spi_flag(pkt):
        return pkt[5] & 0x20

    @staticmethod
    def _parse_length(byte1, byte2):
        """
        parse a 12 bit length value
        """
        return (byte1 & 0x0F) << 8 | byte2

    @staticmethod
    def _parse_pid(byte1, byte2):
        """
        parse a 13 bit pid value
        """
        return (byte1 & 0x01F) << 8 | byte2

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
        except (IndexError, ValueError):
            return False

    def _parse_pts(self, pkt, pid):
        """
        parse pts and store by program key
        in the dict Stream._pid_pts
        """
        payload = self._parse_payload(pkt)
        if len(payload) < 14:
            return
        if self._pts_flag(payload):
            pts = ((payload[9] >> 1) & 7) << 30
            pts |= payload[10] << 22
            pts |= (payload[11] >> 1) << 15
            pts |= payload[12] << 7
            pts |= payload[13] >> 1
            prgm = 1
            if pid in self._pid_prgm:
                prgm = self._pid_prgm[pid]
            self._prgm_pts[prgm] = pts
            if prgm not in self.start:
                self.start[prgm] = pts

    def _parse_pcr(self, pkt, pid):
        """
        parse pcr and store by program key
        in the dict Stream._pid_pcr
        """
        if pkt[3] & 0x20:
            if pkt[5] & 0x10:
                pcr = pkt[6] << 25
                pcr |= pkt[7] << 17
                pcr |= pkt[8] << 9
                pcr |= pkt[9] << 1
                pcr |= pkt[10] >> 7
                prgm = 1
                if pid in self._pid_prgm:
                    prgm = self._pid_prgm[pid]
                self._prgm_pcr[prgm] = pcr

    def _parse_cc(self, pkt, pid):
        c_c = pkt[3] & 0xF
        if pid in self._pid_cc:
            last_cc = self._pid_cc[pid]
            if c_c not in (0, last_cc, last_cc + 1):
                print(f" pid: {hex(pid)} last cc: {last_cc} cc: {c_c}")
        self._pid_cc[pid] = c_c

    @staticmethod
    def _parse_payload(pkt):
        head_size = 4
        if pkt[3] & 0x20:
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
        if not self._chk_last(pay, pid):
            if pid == self._PAT_PID:
                return self._program_association_table(pay)
            if pid == self._SDT_PID:
                if self.info:
                    return self._stream_descriptor_table(pay)
            if pid in self._pids["pmt"]:
                return self._program_map_table(pay, pid)
        return False

    def _parse_info(self, pkt):
        pid = self._parse_pid(pkt[1], pkt[2])
        if pid in self._pids["tables"]:
            self._parse_tables(pkt, pid)
        return pid

    @staticmethod
    def as_90k(ticks):
        """
        as_90k returns ticks as 90k clock time
        """
        return round((ticks / 90000.0), 6)

    def pid2pts(self, pid):
        """
        pid2pts give a pid, returns the pts time
        """
        if pid in self._pid_prgm:
            prgm = self._pid_prgm[pid]
            return self.as_90k(self._prgm_pts[prgm])
        return None

    def _parse(self, pkt):
        cue = False
        # pid = self._parse_pid(pkt[1], pkt[2])
        pid = (pkt[1] & 0x01F) << 8 | pkt[2]
        if pid in self._pids["tables"]:
            self._parse_tables(pkt, pid)
        if self.chk_cc:
            self._parse_cc(pkt, pid)
        if pid in self._pids["pcr"]:
            # if pkt[1] & 0x40:
            #    if b'\x00\x00\x01' in pkt:
            # if pkt[1] & 0x40:
            # pay = self._parse_payload(pkt)
            # print(list(pay))
            #     if b'\x00\x00\x00\x01' in pay:
            #       for nal in pay.split(b'\x00\x00\x00\x01'):
            #         print(len(nal),nal,)
            self._parse_pcr(pkt, pid)
        if pkt[1] & 0x40:
            self._parse_pts(pkt, pid)
        if pid in self._pids["scte35"]:
            cue = self._parse_scte35(pkt, pid)
        return cue

    def _chk_partial(self, pay, pid, sep):
        if pid in self._partial:
            pay = self._partial.pop(pid) + pay
        return self._split_by_idx(pay, sep)

    def _chk_last(self, pay, pid):
        if pid in self._last:
            if pay == self._last[pid]:
                return True
        self._last[pid] = pay
        return False

    def _section_done(self, pay, pid, seclen):
        # + 3 for the bytes before section starts
        if (seclen + 3) > len(pay):
            self._partial[pid] = pay
            return False
        return True

    def _parse_cue(self, pay, pid):
        packet_data = None
        packet_data = self._mk_packet_data(pid)
        cue = Cue(pay, packet_data)
        if cue.decode():
            return cue
        return False

    def _parse_scte35(self, pkt, pid):
        """
        parse a scte35 cue from one or more packets
        """
        pay = self._chk_partial(self._parse_payload(pkt), pid, self._SCTE35_TID)
        if not pay:
            self._pids["scte35"].remove(pid)
            return False
        if pay[13] == self.show_null:
            return False
        seclen = self._parse_length(pay[1], pay[2])
        if not self._section_done(pay, pid, seclen):
            return False
        pay = pay[: seclen + 3]
        cue = self._parse_cue(pay, pid)
        return cue

    def _stream_descriptor_table(self, pay):
        """
        _stream_descriptor_table parses the SDT for program metadata
        """
        pay = self._chk_partial(pay, self._SDT_PID, self._SDT_TID)
        if not pay:
            return False
        seclen = self._parse_length(pay[1], pay[2])
        if not self._section_done(pay, self._SDT_PID, seclen):
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
                    if service_id not in self._prgm:
                        self._prgm[service_id] = ProgramInfo()
                    pinfo = self._prgm[service_id]
                    pinfo.provider = service_provider_name
                    pinfo.service = service_name
                i = dloop_len
                idx += i

    def _program_association_table(self, pay):
        """
        parse program association table
        for program to pmt_pid mappings.
        """
        pay = self._chk_partial(pay, self._PAT_PID, b"\x00")
        seclen = self._parse_length(pay[2], pay[3])
        if not self._section_done(pay, self._PAT_PID, seclen):
            return False
        seclen -= 5  # pay bytes 4,5,6,7,8
        idx = 9
        chunk_size = 4
        while seclen > 4:  #  4 bytes for crc
            program_number = self._parse_program(pay[idx], pay[idx + 1])
            if program_number > 0:
                pmt_pid = self._parse_pid(pay[idx + 2], pay[idx + 3])
                self._pids["tables"].add(pmt_pid)
                self._pids["pmt"].add(pmt_pid)

            seclen -= chunk_size
            idx += chunk_size

    def _program_map_table(self, pay, pid):
        """
        parse program maps for streams
        """
        pay = self._chk_partial(pay, pid, self._PMT_TID)
        if not pay:
            return False
        seclen = self._parse_length(pay[1], pay[2])
        if not self._section_done(pay, pid, seclen):
            return False
        program_number = self._parse_program(pay[3], pay[4])
        if self.the_program and (program_number != self.the_program):
            return False
        pcr_pid = self._parse_pid(pay[8], pay[9])
        if self.info:
            if program_number not in self._prgm:
                self._prgm[program_number] = ProgramInfo(pid=pid, pcr_pid=pcr_pid)
        self._pids["pcr"].add(pcr_pid)
        self._pid_prgm[pcr_pid] = program_number
        proginfolen = self._parse_length(pay[10], pay[11])
        idx = 12
        idx += proginfolen
        si_len = seclen - 9
        si_len -= proginfolen
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
            if self.info:
                pinfo = self._prgm[program_number]
                pinfo.streams[pid] = stream_type
            idx += chunk_size
            idx += ei_len
            self._pid_prgm[pid] = program_number
            self._chk_pid_stream_type(pid, stream_type)

    def _parse_stream_type(self, pay, idx):
        """
        extract stream pid and type
        """
        stream_type = hex(pay[idx])
        el_pid = self._parse_pid(pay[idx + 1], pay[idx + 2])
        ei_len = self._parse_length(pay[idx + 3], pay[idx + 4])
        return stream_type, el_pid, ei_len

    def _chk_pid_stream_type(self, pid, stream_type):
        """
        if stream_type is 0x06 or 0x86
        add it to self._scte35_pids.
        """
        if stream_type in ["0x6", "0x86"]:
            self._pids["scte35"].add(pid)
