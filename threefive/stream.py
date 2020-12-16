"""
Mpeg-TS Stream parsing class Stream
"""

import sys
from functools import partial
from bitn import BitBin
from .cue import Cue
from .streamtype import stream_type_map
from .tools import CMD_TYPES, to_stderr


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
        """
        tsdata is an open file handle
        set show_null=True to include Splice Nulls

        example:

        from threefive import Stream

        with open("vid.ts",'rb') as tsdata:
            strm = Stream(tsdata,show_null=True)
            strm.decode()

        """
        self._tsdata = tsdata
        if show_null:
            self._CMD_TYPES.append(0)
        self._scte35_pids = set()
        self._data_pids = set()
        self._pid_prog = {}
        self._pmt_pids = set()
        self._programs = set()
        self._prog_pts = {}
        self.info = None
        self.the_program = None
        self.cue = None
        self.pat = None

    def decode(self, func=show_cue):
        """
        Stream.decode reads self.tsdata to find SCTE35 packets.

        func is the function called to handle each
        SCTE35 Cue found in the MPEGTS data.

        func is set to show_cue by default.
        All SCTE-35 data is written to sys.stderr.

        func can be set to a custom function that accepts
        a threefive.Cue instance as it's only argument.

        example:

            def myfunc(cue):
                # access cue data using dot notation
                print(f'Table Id: {cue.info_section.table_id}')
        """
        self._find_start()
        for pkt in iter(partial(self._tsdata.read, self._PACKET_SIZE), b""):
            cue = self._parser(pkt)
            if cue:
                func(cue)

    def decode_program(self, the_program, func=show_cue):
        """
        Stream.decode_program works just like Stream.decode
        except the argument, the_program limits SCTE35 parsing
        to that MPEGTS program.
        """
        self.the_program = the_program
        self.decode(func)

    def decode_proxy(self, func=show_cue):
        """
        Stream.decode_proxy works just like Stream.decode
        except that all ts packets are written to stdout
        for piping into another program like mplayer.
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

    def _find_start(self):
        """
        handles partial packets
        """
        sync_byte = b"G"
        while self._tsdata:
            if self._tsdata.read(1) == sync_byte:
                if self._tsdata.read(self._PACKET_SIZE - 1):
                    return

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
            if prgm in self._prog_pts:
                if pid not in self._data_pids:
                    packet_data["pts"] = round(self._prog_pts[prgm], 6)
        return packet_data

    def _parser(self, pkt):
        """
        parse pid from pkt and
        route it appropriately
        """
        pid = self._parse_pid(pkt[1], pkt[2])
        if pid == 0:
            self._program_association_table(pkt)
            return None
        if pid in self._pmt_pids:
            self._program_map_section(pkt)
            return None
        if self.info:
            return None
        if pid in self._pid_prog.keys():
            if (pkt[1] >> 6) & 1:
                part_pkt = pkt[0:18]
                self._parse_pusi(part_pkt, pid)
        if pid in self._scte35_pids:
            return self._parse_scte35(pkt, pid)
        return None

    @staticmethod
    def _parse_pid(byte1, byte2):
        """
        parse pid from packet
        """
        return (byte1 & 31) << 8 | byte2

    def _chk_pid_stream_type(self, pid, stream_type):
        if stream_type in ["0x6", "0x86"]:
            self._scte35_pids.add(pid)
        if stream_type == "0x6":
            self._data_pids.add(pid)

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
                minus, pstream = self._parse_stream_type(bitbin)
                slib -= minus
                stream_type = pstream[0]
                pid = pstream[1]
                self._pid_prog[pid] = program_number
                if self.info:
                    self._show_program_stream(pid, stream_type)
                self._chk_pid_stream_type(pid, stream_type)
        else:
            if self.info:
                sys.exit()

    def _parse_pts(self, pkt, pid):
        """
        parse pts and store by program key
        in the dict Stream._prog_pts
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
        parse a scte35 cue from one or more packets
        """
        if not self.cue:
            try:
                pkt = pkt[:5] + b"\xfc0" + pkt.split(b"\xfc0", 1)[1]
            except:
                return None
            packet_data = self._mk_packet_data(pid)
            if pkt[18] in self._CMD_TYPES:
                self.cue = Cue(pkt[:19], packet_data)
                self.cue.mk_info_section(pkt[5:19])
                self.cue.payload += pkt[19:]
            else:
                return None
        else:
            self.cue.payload += pkt[4:]
        if (self.cue.info_section.section_length + 3) <= len(self.cue.payload):
            self.cue.decode()
            cue = self.cue
            self.cue = None
            return cue
        return None

    @staticmethod
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

    def _program_association_table(self, pkt):
        """
        parse program association table ( pid 0 )
        to program to program table pid mappings.
        """
        if not self.pat:
            self.pat = {}
            self.pat["sectionlen"] = (pkt[6] & 15 << 8) | pkt[7]
            self.pat["data"] = pkt[13:]
        else:
            self.pat["data"] += pkt[4:]
        if len(self.pat["data"]) < self.pat["sectionlen"]:
            return
        bitbin = BitBin(self.pat["data"])
        slib = self.pat["sectionlen"] << 3
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
        self.pat = None

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

    @staticmethod
    def _show_program_stream(pid, stream_type):
        """
        print program -> stream mappings
        """
        streaminfo = f"[{stream_type}] Reserved or Private"
        if stream_type in stream_type_map:
            streaminfo = f"[{stream_type}] {stream_type_map[stream_type]}"
        to_stderr(f"\t   {pid}: {streaminfo}")
