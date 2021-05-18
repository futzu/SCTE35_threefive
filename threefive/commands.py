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
        self.name = None
        self.identifier = None
        self.time_specified_flag = None
        self.pts_time = None
        self.splices = None
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


class BandwidthReservation(SpliceCommand):
    """
    Table 11 - bandwidth_reservation()
    """

    def decode(self):
        """
        BandwidthReservation.decode method
        """
        self.name = "Bandwidth Reservation"


class PrivateCommand(SpliceCommand):
    """
    Table 12 - private_command
    """

    def decode(self):
        """
        PrivateCommand.decode method
        """
        self.name = "Private Command"
        self.identifier = int.from_bytes(
            self.bites[0:3], byteorder="big"
        )  # 3 bytes = 24 bits
        self.bites = self.bites[3:]


class SpliceNull(SpliceCommand):
    """
    Table 7 - splice_null()
    """

    def decode(self):
        """
        SpliceNull.decode method
        """
        self.calculated_length = 0
        self.name = "Splice Null"


class TimeSignal(SpliceCommand):
    """
    Table 10 - time_signal()
    """

    def decode(self):
        """
        TimeSignal.decode method
        """
        self.name = "Time Signal"
        bitbin = BitBin(self.bites)
        start = bitbin.idx
        self._splice_time(bitbin)
        self._set_len(start, bitbin.idx)

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

    def _decode_event(self, bitbin):
        """
        _decode_event sets splice_event_id
        and splice_event_cancel_indicator
        """
        self.splice_event_id = bitbin.as_int(32)
        self.splice_event_cancel_indicator = bitbin.as_flag(1)
        bitbin.forward(7)

    def _decode_flags(self, bitbin):
        """
        SpliceInsert._decode_flags set four flags
        and is called from SpliceInsert.decode()
        """
        self.out_of_network_indicator = bitbin.as_flag(1)
        self.program_splice_flag = bitbin.as_flag(1)
        self.duration_flag = bitbin.as_flag(1)

    def _decode_components(self, bitbin):
        """
        SpliceInsert._decode_components loops
        over SpliceInsert.components,
        and is called from SpliceInsert.decode()
        """
        component_count = bitbin.as_int(8)
        self.components = []
        for i in range(0, component_count):
            self.components[i] = bitbin.as_int(8)

    def _decode_unique_avail(self, bitbin):
        self.unique_program_id = bitbin.as_int(16)
        self.avail_num = bitbin.as_int(8)
        self.avail_expected = bitbin.as_int(8)

    def decode(self):
        """
        SpliceInsert.decode
        """
        bitbin = BitBin(self.bites)
        start = bitbin.idx
        self._decode_event(bitbin)
        if not self.splice_event_cancel_indicator:
            self._decode_flags(bitbin)
            self.splice_immediate_flag = bitbin.as_flag(1)
            bitbin.forward(4)
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


class SpliceSchedule(SpliceCommand):
    """
    Table 8 - splice_schedule()
    """

    class SpliceEvent(SpliceInsert):
        """
        SpliceSchedule is comprised
        of SpliceEvent instances
        """

        def __init__(self):
            super().__init__(None)
            self.name = None
            self.utc_splice_time = None

        def _decode_components(self, bitbin):
            component_count = bitbin.as_int(8)
            self.components = []
            for j in range(0, component_count):
                self.components[j] = {
                    "component_tag": bitbin.as_int(8),
                    "utc_splice_time": bitbin.as_int(32),
                }

        def decode(self, bitbin):
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

    def decode(self):
        """
        SpliceSchedule.decode
        """
        self.name = "Splice Schedule"
        self.splices = []
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
