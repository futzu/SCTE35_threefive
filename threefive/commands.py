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
        self.command_length = 0
        self.command_type = None
        self.bites = bites

    def decode(self):
        """
        default decode method
        """


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
        self.identifier = int.from_bytes(
            self.bites[0:3], byteorder="big"
        )  # 3 bytes = 24 bits


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

    def _set_len(self, start, end):
        self.command_length = (start - end) >> 3

    def _decode_pts(self, bitbin):
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
        self.break_auto_return = bitbin.as_flag(1)
        bitbin.forward(6)
        self.break_duration = bitbin.as_90k(33)

    def _decode_flags(self, bitbin):
        """
        SpliceInsert._decode_flags set four flags
        and is called from SpliceInsert.decode()
        """
        self.out_of_network_indicator = bitbin.as_flag(1)
        self.program_splice_flag = bitbin.as_flag(1)
        self.duration_flag = bitbin.as_flag(1)
        self.splice_immediate_flag = bitbin.as_flag(1)
        bitbin.forward(4)

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

    def decode(self):
        """
        SpliceInsert.decode
        """
        bitbin = BitBin(self.bites)
        start = bitbin.idx
        self.splice_event_id = bitbin.as_int(32)
        self.splice_event_cancel_indicator = bitbin.as_flag(1)
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
            self.unique_program_id = bitbin.as_int(16)
            self.avail_num = bitbin.as_int(8)
            self.avail_expected = bitbin.as_int(8)
        self._set_len(start, bitbin.idx)


class SpliceSchedule(SpliceCommand):
    """
    Table 8 - splice_schedule()
    """

    def __init__(self):
        self.name = "Splice Schedule"

    def decode(self, bitbin):
        splice_count = bitbin.asint(8)
        for i in range(0, splice_count):
            self.splice_event_id = bitbin.asint(32)
            self.splice_event_cancel_indicator = bitbin.asflag(1)
            bitbin.forward(7)
            if not self.splice_event_cancel_indicator:
                self.out_of_network_indicator = bitbin.asflag(1)
                self.program_splice_flag = bitbin.asflag(1)
                self.duration_flag = bitbin.asflag(1)
                bitbin.forward(5)
                if self.program_splice_flag:
                    self.utc_splice_time = bitbin.asint(32)
                else:
                    self.component_count = bitbin.asint(8)
                    self.components = []
                    for j in range(0, self.component_count):
                        self.components[j] = {
                            "component_tag": bitbin.asint(8),
                            "utc_splice_time": bitbin.asint(32),
                        }
                if self.duration_flag:
                    self.break_duration(bitbin)
                self.unique_program_id = bitbin.asint(16)
                self.avail_num = bitbin.asint(8)
                self.avails_expected = bitbin.asint(8)


command_map = {
    0: SpliceNull,
    4: SpliceSchedule,
    5: SpliceInsert,
    6: TimeSignal,
    7: BandwidthReservation,
    255: PrivateCommand,
}
