import sys
from functools import partial

from bitn import BitBin
from .cue import Cue
from .streamtype import stream_type_map
from .tools import CMD_TYPES, parse_pid, to_stderr


def _parse_stream_type(bitbin):
    """
    extract stream pid and type
    """
    stream_type = bitbin.ashex(8)  # 8
    bitbin.forward(3)  # 11
    el_pid = bitbin.asint(13)  # 24
    bitbin.forward(4)  # 28
    eilib = bitbin.asint(12) << 3  # 40
    bitbin.forward(eilib)
    minus = 40 + eilib
    return minus, [stream_type, el_pid]


def _show_program_stream(pid, stream_type):
    """
    print program -> stream mappings
    """
    streaminfo = f"[{stream_type}] Reserved or Private"
    if stream_type in stream_type_map.keys():
        streaminfo = f"[{stream_type}] {stream_type_map[stream_type]}"
    to_stderr(f"\t   {pid}: {streaminfo}")


def show_cue(cue):
    """
    default function call for
    Stream.decode,
    Stream.decode_program,
    and Stream.decode_proxy
    when a SCTE-35 packet is found.
    """
    cue.show()


class Stream:
    """
    Stream class
    With MPEG-TS program awareness.
    Accurate pts for streams with
    more than one program containing
    SCTE-35 streams.
    """

    _CMD_TYPES = CMD_TYPES
    _PACKET_SIZE = 188

    def __init__(self, tsdata, show_null=False):
        self._tsdata = tsdata
        if show_null:
            self._CMD_TYPES.append(0)
        self._scte35_pids = set()
        self._pid_prog = {}
        self._pmt_pids = set()
        self._programs = set()
        self._prog_pts = {}
        self.info = False
        self.the_program = False

    def _find_start(self):
        """
        handles partial packets
        """
        if self._tsdata.read(self._PACKET_SIZE)[0] == 71:
            return
        sync_byte = b"G"
        while self._tsdata:
            one_byte = self._tsdata.read(1)
            if not one_byte:
                sys.exit()
            if one_byte is sync_byte:
                self._tsdata.read(self._PACKET_SIZE - 1)
                if self._tsdata.read(1) is sync_byte:
                    self._tsdata.read(self._PACKET_SIZE - 1)
                    return

    def decode(self, func=show_cue):
        """
        reads MPEG-TS to find SCTE-35 packets
        """
        self._find_start()
        for pkt in iter(partial(self._tsdata.read, self._PACKET_SIZE), b""):
            cue = self._parser(pkt)
            if cue:
                func(cue)

    def decode_next(self):
        """
        returns a threefive.Cue instance
        when a SCTE-35 packet is found
        """
        self._find_start()
        for pkt in iter(partial(self._tsdata.read, self._PACKET_SIZE), b""):
            cue = self._parser(pkt)
            if cue:
                return cue

    def decode_program(self, the_program, func=show_cue):
        """
        returns a threefive.Cue instance
        when a SCTE-35 packet is found
        """
        self.the_program = the_program
        self.decode(func)

    def decode_proxy(self, func=show_cue):
        """
        reads an MPEG-TS stream
        and writes all ts packets to stdout
        and SCTE-35 data to stderr
        """
        self._find_start()
        for pkt in iter(partial(self._tsdata.read, self._PACKET_SIZE), b""):
            sys.stdout.buffer.write(pkt)
            cue = self._parser(pkt)
            if cue:
                func(cue)

    def show(self):
        """
        displays program stream mappings
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
        prgm = self._pid_prog[pid]
        packet_data["program"] = prgm
        if prgm in self._prog_pts:
            packet_data["pts"] = round(self._prog_pts[prgm], 6)
        return packet_data

    def _program_association_table(self, pkt):
        """
        parse program association table ( pid 0 )
        to program to program table pid mappings.
        """
        sectionlen = (pkt[6] & 15 << 8) | pkt[7]
        pkt = pkt[13 : (sectionlen + 5)]
        bitbin = BitBin(pkt)
        slib = sectionlen << 3
        slib -= 40
        while slib > 32:
            program_number = bitbin.asint(16)
            bitbin.forward(3)
            if program_number == 0:
                bitbin.forward(13)
            else:
                self._pmt_pids.add(bitbin.asint(13))
            slib -= 32
        bitbin.forward(32)

    def _parser(self, pkt):
        """
        parse pid from pkt and
        route it appropriately
        """
        pid = parse_pid(pkt[1], pkt[2])
        if pid == 0:
            self._program_association_table(pkt)
            return False
        if pid in self._pmt_pids:
            self._program_map_section(pkt)
        # This return makes Stream.show() fast
        if self.info:
            return False
        if pid in self._scte35_pids:
            return self._parse_scte35(pkt, pid)
        if pid in self._pid_prog.keys():
            if (pkt[1] >> 6) & 1:
                pkt = pkt[0:18]
                self._parse_pusi(pkt, pid)

    def _parse_pts(self, pkt, pid):
        """
        parse pts
        """
        pts = ((pkt[13] >> 1) & 7) << 30
        pts |= ((pkt[14] << 7) | (pkt[15] >> 1)) << 15
        pts |= (pkt[16] << 7) | (pkt[17] >> 1)
        pts /= 90000.0
        ppp = self._pid_prog[pid]
        self._prog_pts[ppp] = pts

    def _parse_pusi(self, pkt, pid):
        """
        used to determine if pts data is available.
        """
        if pkt[6] & 1:
            if (pkt[10] >> 6) & 2:
                if (pkt[11] >> 6) & 2:
                    if (pkt[13] >> 4) & 2:
                        self._parse_pts(pkt, pid)

    def _parse_scte35(self, pkt, pid):
        """
        parse a SCTE-35 packet
        """
        packet_data = self._mk_packet_data(pid)
        pkt = pkt[:5] + b"\xfc0" + pkt.split(b"\x00\xfc0")[1]
        # check splice command type
        if pkt[18] in self._CMD_TYPES:
            return Cue(pkt, packet_data)
        return False

    def _parse_program_streams(self, slib, bitbin, program_number):
        """
        parse the elementary streams
        from a program
        """
        if program_number not in self._programs:
            self._programs.add(program_number)
            if self.info:
                to_stderr(f"\nProgram: {program_number}")
            while slib > 32:
                minus, pstream = _parse_stream_type(bitbin)
                slib -= minus
                stream_type = pstream[0]
                pid = pstream[1]
                self._pid_prog[pid] = program_number
                if self.info:
                    _show_program_stream(pid, stream_type)
                if stream_type == "0x86":
                    self._scte35_pids.add(pid)
        else:
            if self.info:
                sys.exit()

    def _program_map_section(self, pkt):
        """
        parse program maps for streams
        """
        # table_id = pkt[5]
        sectioninfolen = (pkt[6] & 15 << 8) | pkt[7]
        slib = sectioninfolen << 3
        program_number = (pkt[8] << 8) | pkt[9]
        # version = pkt[10] >> 1 & 31
        # current_next = pkt[10] & 1
        if self.the_program and (program_number != self.the_program):
            return None
        # section_number = pkt[11]
        # last_section_number = pkt[12]
        # pcr_pid = (pkt[13]& 31) << 8 | pkt[14]
        proginfolen = (pkt[15] & 15 << 8) | pkt[16]
        pkt = pkt[(17 + proginfolen) : (slib + 9)]
        bitbin = BitBin(pkt)
        pilib = proginfolen << 3
        slib -= 72
        slib -= pilib  # Skip descriptors
        self._parse_program_streams(slib, bitbin, program_number)
