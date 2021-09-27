"""
SCTE35 Splice Commands
"""
from .bitn import BitBin
from .base import SCTE35Base


class SpliceCommand(SCTE35Base):
    """
    Base class, not used directly.
    """

    def __init__(self, bites=None):
        self.calculated_length = None
        self.command_type = None
        self.name = None
        self.bites = bites

    def decode(self):
        """
        default decode method
        """

    def _set_len(self, start, end):
        """
        _set_len sets
        self.calculated_length
        """
        self.calculated_length = (start - end) >> 3

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
        self.command_type = 7
        self.name = "Bandwidth Reservation"

    def decode(self):
        """
        BandwidthReservation.decode method
        """


class PrivateCommand(SpliceCommand):
    """
    Table 12 - private_command
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.command_type = 255
        self.name = "Private Command"
        self.identifier = None

    def decode(self):
        """
        PrivateCommand.decode method
        """
        self.identifier = int.from_bytes(
            self.bites[0:3], byteorder="big"
        )  # 3 bytes = 24 bits
        self.bites = self.bites[3:]

    def encode(self, nbin=None):
        """
        encode private command
        """
        nbin = self._chk_nbin(nbin)
        self._chk_var(int, nbin.add_int, "identifier", 24)  # 3 bytes = 24 bits
        return nbin.bites


class SpliceNull(SpliceCommand):
    """
    Table 7 - splice_null()
    """

    def __init__(self, bites=None):
        super().__init__(bites)
        self.command_type = 0
        self.name = "Splice Null"


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
        TimeSignal.decode method
        """
        bitbin = BitBin(self.bites)
        start = bitbin.idx
        self._splice_time(bitbin)
        self._set_len(start, bitbin.idx)

    def encode(self, nbin=None):
        """
        encode converts TimeSignal vars
        to bytes
        """
        nbin = self._chk_nbin(nbin)
        self._encode_splice_time(nbin)
        return nbin.bites

    def _splice_time(self, bitbin):
        """
        parse_pts is called by either a
        TimeSignal or SpliceInsert instance
        to decode pts.
        """
        self.time_specified_flag = bitbin.as_flag(1)
        if self.time_specified_flag:
            bitbin.forward(6)
            self.pts_time = bitbin.as_90k(33)
        else:
            bitbin.forward(7)

    def _encode_splice_time(self, nbin):
        self._chk_var(bool, nbin.add_flag, "time_specified_flag", 1)
        if self.time_specified_flag:
            nbin.reserve(6)
            self._chk_var(float, nbin.add_90k, "pts_time", 33)
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
        self.component_count = None
        self.components = None
        self.unique_program_id = None
        self.avail_num = None
        self.avail_expected = None

    def _decode_break(self, bitbin):
        """
        SpliceInsert._decode_break(bitbin) is called
        if SpliceInsert.duration_flag is set
        """
        if self.duration_flag:
            self.break_auto_return = bitbin.as_flag(1)
            bitbin.forward(6)
            self.break_duration = bitbin.as_90k(33)

    def _encode_break(self, nbin):
        """
        SpliceInsert._encode_break(nbin) is called
        if SpliceInsert.duration_flag is set
        """
        if self.duration_flag:
            self._chk_var(bool, nbin.add_flag, "break_auto_return", 1)
            nbin.forward(6)
            self._chk_var(float, nbin.add_90k, "break_duration", 33)

    def _decode_event(self, bitbin):
        """
        SpliceInsert._decode_flags set four flags
        and is called from SpliceInsert.decode()
        """
        self.splice_event_id = bitbin.as_int(32)
        self.splice_event_cancel_indicator = bitbin.as_flag(1)
        bitbin.forward(7)

    def _encode_event(self, nbin):
        self._chk_var(int, nbin.add_int, "splice_event_id", 32)
        self._chk_var(bool, nbin.add_flag, "splice_event_cancel_indicator", 1)
        nbin.forward(7)

    def _decode_flags(self, bitbin):
        self.out_of_network_indicator = bitbin.as_flag(1)
        self.program_splice_flag = bitbin.as_flag(1)
        self.duration_flag = bitbin.as_flag(1)
        self.splice_immediate_flag = bitbin.as_flag(1)
        bitbin.forward(4)

    def _encode_flags(self, nbin):
        """
        SpliceInsert._encode_flags converts four flags
        to bits
        """
        self._chk_var(bool, nbin.add_flag, "out_of_network_indicator", 1)
        self._chk_var(bool, nbin.add_flag, "program_splice_flag", 1)
        self._chk_var(bool, nbin.add_flag, "duration_flag", 1)
        self._chk_var(bool, nbin.add_flag, "splice_immediate_flag", 1)
        nbin.forward(4)

    def _decode_components(self, bitbin):
        """
        SpliceInsert._decode_components loops
        over SpliceInsert.components,
        and is called from SpliceInsert.decode()
        """
        self.component_count = bitbin.as_int(8)
        self.components = []
        for i in range(0, self.component_count):
            self.components[i] = bitbin.as_int(8)

    def _encode_components(self, nbin):
        """
        SpliceInsert._encode_components loops
        over SpliceInsert.components,
        and is called from SpliceInsert.encode()
        """
        nbin.add_int(self.component_count, 8)
        for i in range(0, self.component_count):
            nbin.add_int(self.components[i], 8)

    def _decode_unique_avail(self, bitbin):
        self.unique_program_id = bitbin.as_int(16)
        self.avail_num = bitbin.as_int(8)
        self.avail_expected = bitbin.as_int(8)

    def _encode_unique_avail(self, nbin):
        self._chk_var(int, nbin.add_int, "unique_program_id", 16)
        self._chk_var(int, nbin.add_int, "avail_num", 8)
        self._chk_var(int, nbin.add_int, "avail_expected", 8)

    def decode(self):
        """
        SpliceInsert.decode
        """
        bitbin = BitBin(self.bites)
        start = bitbin.idx
        self._decode_event(bitbin)
        if not self.splice_event_cancel_indicator:
            self._decode_flags(bitbin)
            if self.program_splice_flag:
                if not self.splice_immediate_flag:
                    self._splice_time(bitbin)
            else:
                self._decode_components(bitbin)
                if not self.splice_immediate_flag:
                    self._splice_time(bitbin)
            self._decode_break(bitbin)
            self._decode_unique_avail(bitbin)
        self._set_len(start, bitbin.idx)

    def encode(self, nbin=None):
        """
        SpliceInsert.encode
        """
        nbin = self._chk_nbin(nbin)
        self._encode_event(nbin)
        if not self.splice_event_cancel_indicator:
            self._encode_flags(nbin)
            if self.program_splice_flag:
                if not self.splice_immediate_flag:
                    self._encode_splice_time(nbin)
            else:
                self._encode_components(nbin)
                if not self.splice_immediate_flag:
                    self._encode_splice_time(nbin)
            self._encode_break(nbin)
            self._encode_unique_avail(nbin)
        return nbin.bites


class SpliceSchedule(SpliceCommand):
    """
    Table 8 - splice_schedule()
    """

    class SpliceEvent(SpliceInsert):
        """
        SpliceEvent is a class declared in
        the SpliceSchedule class.
        """

        def __init__(self):
            """
            SpliceEvent
            """
            super().__init__(None)
            self.name = None
            self.utc_splice_time = None

        def _decode_components(self, bitbin):
            """
            SpliceEvent._decode_components
            """
            component_count = bitbin.as_int(8)
            self.components = []
            for j in range(0, component_count):
                self.components[j] = {
                    "component_tag": bitbin.as_int(8),
                    "utc_splice_time": bitbin.as_int(32),
                }

        def decode(self, bitbin):
            """
            SpliceEvent.decode
            """
            self._decode_event(bitbin)
            if not self.splice_event_cancel_indicator:
                self._decode_flags(bitbin)
                bitbin.forward(5)
                if self.program_splice_flag:
                    self.utc_splice_time = bitbin.as_int(32)
                else:
                    self._decode_components(bitbin)
                self._decode_break(bitbin)
                self._decode_unique_avail(bitbin)

    def __init__(self, bites=None):
        """
        SpliceSchedule.__init__
        """
        super().__init__(bites)
        self.command_type = 4
        self.name = "Splice Schedule"
        self.splices = []

    def decode(self):
        """
        SpliceSchedule.decode
        """
        bitbin = BitBin(self.bites)
        start = bitbin.idx
        splice_count = bitbin.as_int(8)
        for i in range(0, splice_count):
            self.splices[i] = self.SpliceEvent()
            self.splices[i].decode(bitbin)
        self._set_len(start, bitbin.idx)


command_map = {
    0: SpliceNull,
    4: SpliceSchedule,
    5: SpliceInsert,
    6: TimeSignal,
    7: BandwidthReservation,
    255: PrivateCommand,
}
