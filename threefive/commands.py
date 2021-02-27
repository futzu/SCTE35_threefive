"""
SCTE35 Splice Commands
"""
from bitn import BitBin
from .base import SCTE35Base
from .tools import ifb


class SpliceCommand(SCTE35Base):
    """
    Base class, not used directly.
    """

    def __init__(self, bites=None):
        self.command_length = 0
        self.command_type = None
        self.bites = bites

    def decode(self):
        """
        default decode method
        """

    def encode(self, nbin=None):
        """
        encode
        """
        nbin = self._chk_nbin(nbin)
        return nbin.bites


class BandwidthReservation(SpliceCommand):
    """
    Table 11 - bandwidth_reservation()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.command_type = 255
        self.name = "Bandwidth Reservation"


class SpliceNull(SpliceCommand):
    """
    Table 7 - splice_null()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.command_type = 0
        self.name = "Splice Null"


class PrivateCommand(SpliceCommand):
    """
    Table 12 - private_command
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.command_type = 255
        self.name = "Private Command"
        self.identifier = None
        self.command_length = 3

    def decode(self):
        """
        decode private command
        """
        self.identifier = ifb(self.bites[0:3])  # 3 bytes of 8 bits = 24 bits
        self.encode()

    def encode(self, nbin=None):
        """
        encode private command
        """
        nbin = self._chk_nbin(nbin)
        self.precheck(
            int, nbin.add_int, "identifier", 24
        )  # 3 bytes of 8 bits = 24 bits
        return nbin.bites


class TimeSignal(SpliceCommand):
    """
    Table 10 - time_signal()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.command_type = 6
        self.name = "Time Signal"
        self.time_specified_flag = None
        self.pts_time = None

    def decode(self):
        """
        decode is called only by a TimeSignal instance
        """
        bitbin = BitBin(self.bites)
        start = bitbin.idx
        self._decode_pts(bitbin)
        self._set_len(start, bitbin.idx)

    def encode(self, nbin=None):
        """
        encode converts TimeSignal vars
        to bytes
        """
        nbin = self._chk_nbin(nbin)
        self._encode_pts(nbin)
        return nbin.bites

    def _set_len(self, start, end):
        self.command_length = (start - end) >> 3

    def _decode_pts(self, bitbin):
        """
        parse_pts is called by either a
        TimeSignal or SpliceInsert instance
        to decode pts.
        """
        self.time_specified_flag = bitbin.asflag(1)
        if self.time_specified_flag:
            bitbin.forward(6)
            self.pts_time = bitbin.as90k(33)
        else:
            bitbin.forward(7)

    def _encode_pts(self, nbin):
        self.precheck(bool, nbin.add_flag, "time_specified_flag", 1)
        if self.time_specified_flag:
            nbin.reserve(6)
            self.precheck(float, nbin.add_90k, "pts_time", 33)
        else:
            nbin.reserve(7)


class SpliceInsert(TimeSignal):
    """
    Table 9 - splice_insert()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.command_type = 5
        self.name = "Splice Insert"
        self.break_auto_return = None
        self.break_duration = None
        self.splice_event_id = None
        self.splice_event_cancel_indicator = None
        self.out_of_network_indicator = None
        self.program_splice_flag = None
        self.duration_flag = None
        self.splice_immediate_flag = None
        self.components = None
        self.component_count = None
        self.unique_program_id = None
        self.avail_num = None
        self.avail_expected = None

    def _decode_break(self, bitbin):
        """
        SpliceInsert._decode_break(bitbin) is called
        if SpliceInsert.duration_flag is set
        """
        self.break_auto_return = bitbin.asflag(1)
        bitbin.forward(6)
        self.break_duration = bitbin.as90k(33)

    def _encode_break(self, nbin):
        """
        SpliceInsert._encode_break(nbin) is called
        if SpliceInsert.duration_flag is set
        """
        self.precheck(bool, nbin.add_flag, "break_auto_return", 1)
        nbin.forward(6)
        self.precheck(float, nbin.add_90k, "break_duration", 33)

    def _decode_flags(self, bitbin):
        """
        SpliceInsert._decode_flags set four flags
        and is called from SpliceInsert.decode()
        """
        self.out_of_network_indicator = bitbin.asflag(1)
        self.program_splice_flag = bitbin.asflag(1)
        self.duration_flag = bitbin.asflag(1)
        self.splice_immediate_flag = bitbin.asflag(1)
        bitbin.forward(4)

    def _encode_flags(self, nbin):
        """
        SpliceInsert._encode_flags converts four flags
        to bits
        """
        self.precheck(bool, nbin.add_flag, "out_of_network_indicator", 1)
        self.precheck(bool, nbin.add_flag, "program_splice_flag", 1)
        self.precheck(bool, nbin.add_flag, "duration_flag", 1)
        self.precheck(bool, nbin.add_flag, "splice_immediate_flag", 1)
        nbin.forward(4)

    def _decode_components(self, bitbin):
        """
        SpliceInsert._decode_components loops
        over SpliceInsert.components,
        and is called from SpliceInsert.decode()
        """
        self.component_count = bitbin.asint(8)
        self.components = []
        for i in range(0, self.component_count):
            self.components[i] = bitbin.asint(8)

    def _encode_components(self, nbin):
        """
        SpliceInsert._encode_components loops
        over SpliceInsert.components,
        and is called from SpliceInsert.encode()
        """
        nbin.add_int(self.component_count, 8)
        for i in range(0, self.component_count):
            nbin.add_int(self.components[i], 8)

    def decode(self):
        """
        SpliceInsert.decode
        """
        bitbin = BitBin(self.bites)
        start = bitbin.idx
        self.splice_event_id = bitbin.asint(32)
        self.splice_event_cancel_indicator = bitbin.asflag(1)
        bitbin.forward(7)
        if not self.splice_event_cancel_indicator:
            self._decode_flags(bitbin)
            if self.program_splice_flag:
                if not self.splice_immediate_flag:
                    self._decode_pts(bitbin)
            else:
                self._decode_components(bitbin)
                if not self.splice_immediate_flag:
                    self._decode_pts(bitbin)
            if self.duration_flag:
                self._decode_break(bitbin)
            self.unique_program_id = bitbin.asint(16)
            self.avail_num = bitbin.asint(8)
            self.avail_expected = bitbin.asint(8)
        self._set_len(start, bitbin.idx)

    def encode(self, nbin=None):
        """
        SpliceInsert.encode
        """
        nbin = self._chk_nbin(nbin)
        self.precheck(int, nbin.add_int, "splice_event_id", 32)
        self.precheck(bool, nbin.add_flag, "splice_event_cancel_indicator", 1)
        nbin.forward(7)
        if not self.splice_event_cancel_indicator:
            self._encode_flags(nbin)
            if self.program_splice_flag:
                if not self.splice_immediate_flag:
                    self._encode_pts(nbin)
            else:
                self._encode_components(nbin)
                if not self.splice_immediate_flag:
                    self._encode_pts(nbin)
            if self.duration_flag:
                self._encode_break(nbin)
            self.precheck(int, nbin.add_int, "unique_program_id", 16)
            self.precheck(int, nbin.add_int, "avail_num", 8)
            self.precheck(int, nbin.add_int, "avail_expected", 8)
        return nbin.bites


command_map = {
    0: SpliceNull,
    5: SpliceInsert,
    6: TimeSignal,
    7: BandwidthReservation,
    255: PrivateCommand,
}


def splice_command(sct, bites):
    """
    splice_command
    returns an instance
    command_map[sct]
    """
    if sct in command_map:
        cmd = command_map[sct](bites)
        cmd.decode()
        return cmd
    return False
