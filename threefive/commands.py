"""
SCTE35 Splice Commands
"""
from bitn import BitBin, NBin
from .tools import ifb


class SpliceCommand:
    """
    Base class, not used directly.
    """

    def __init__(self, bites=None):
        self.command_length = 0
        self.bites = bites
        self.name = None

    def decode(self):
        """
        decode
        """

    def encode(self, nbin=None):
        """
        encode
        """
        nbin = self._chk_nbin(nbin)
        return nbin

    @staticmethod
    def _chk_nbin(nbin):
        if not nbin:
            nbin = NBin()
        return nbin


class BandwidthReservation(SpliceCommand):
    """
    Table 11 - bandwidth_reservation()
    """

    def decode(self):
        self.name = "Bandwidth Reservation"


class SpliceNull(SpliceCommand):
    """
    Table 7 - splice_null()
    """

    def decode(self):
        self.name = "Splice Null"


class PrivateCommand(SpliceCommand):
    """
    Table 12 - private_command
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.identifier = None

    def decode(self):
        """
        decode private command
        """
        self.name = "Private Command"
        self.identifier = ifb(self.bites[0:3])  # 3 bytes of 8 bits = 24 bits
        self.command_length = 3
        self.encode()

    def encode(self, nbin=None):
        """
        encode private command
        """
        nbin = self._chk_nbin(nbin)
        nbin.add_int(self.identifier, 24)  # 3 bytes of 8 bits = 24 bits
        return nbin


class TimeSignal(SpliceCommand):
    """
    Table 10 - time_signal()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
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
        return nbin

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
        nbin.add_flag(self.time_specified_flag)
        if self.time_specified_flag:
            nbin.reserve(6)
            nbin.add_90k(self.pts_time, 33)
        else:
            nbin.reserve(7)


class SpliceInsert(TimeSignal):
    """
    Table 9 - splice_insert()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
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
        nbin.add_flag(self.break_auto_return)
        nbin.forward(6)
        nbin.add_90k(self.break_duration, 33)

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
        nbin.add_flag(self.out_of_network_indicator)
        nbin.add_flag(self.program_splice_flag)
        nbin.add_flag(self.duration_flag)
        nbin.add_flag(self.splice_immediate_flag)
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
        nbin.add_int(self.splice_event_id, 32)
        nbin.add_flag(self.splice_event_cancel_indicator)
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
            nbin.add_int(self.unique_program_id, 16)
            nbin.add_int(self.avail_num, 8)
            nbin.add_int(self.avail_expected, 8)
        return nbin


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
