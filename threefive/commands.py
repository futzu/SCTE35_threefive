"""
SCTE35 Splice Commands
"""
from .tools import ifb
from .const import PTS_TICKS_PER_SECOND


class SpliceCommand:
    """
    Base class, not used directly.
    """

    def __init__(self, bites):
        self.idx = 0
        self.bites = bites
        self.name = None

    def decode(self):
        """
        SpliceCommand.decode defines
        a standard interface for
        SpliceCommand subclasses.
        """


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

    def decode(self):
        """
        decode private command
        """
        self.name = "Private Command"
        _end = self.idx + 3  # 3 bytes of 8 bits = 24 bits
        self.identifier = ifb(self.bites[self.idx : _end])
        self.idx = _end


class TimeSignal(SpliceCommand):
    """
    Table 10 - time_signal()
    """

    def __init__(self, bites):
        super().__init__(bites)
        self.name = "Time Signal"
        self.time_specified_flag = None
        self.pts_time = None

    def as90k(self):
        _end = self.idx + 5  # 5 bytes of 8 bits = 40 bits
        _ttb = (self.bites[self.idx] & 1) << 32  # the +1 below
        _ttb |= ifb(self.bites[self.idx + 1 : _end])
        self.idx = _end
        return round((_ttb / PTS_TICKS_PER_SECOND), 6)

    def decode(self):  # 40bits
        """
        decode pts
        """
        _tsf = self.bites[self.idx] & 0x80
        self.time_specified_flag = bool(_tsf)
        if self.time_specified_flag:
            self.pts_time = self.as90k()
        else:
            self.idx += 1


class SpliceInsert(TimeSignal):
    """
    Table 9 - splice_insert()
    """

    def __init__(self, bites):
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

    def _parse_break(self):
        """
        SpliceInsert.parse_break(bitbin) is called
        if SpliceInsert.duration_flag is set
        """
        _bar = self.bites[self.idx] & 0x80
        self.break_auto_return = bool(_bar)
        self.break_duration = self.as90k()

    def _parse_event(self):
        _end = self.idx + 4
        self.splice_event_id = ifb(self.bites[self.idx : _end])
        self.idx = _end
        _seci = self.bites[self.idx] & 0x80
        self.splice_event_cancel_indicator = bool(_seci)
        self.idx += 1

    def _parse_flags(self):
        _ooni = self.bites[self.idx] & 0x80
        self.out_of_network_indicator = bool(_ooni)
        _psf = self.bites[self.idx] & 0x40
        self.program_splice_flag = bool(_psf)
        _df = self.bites[self.idx] & 0x20
        self.duration_flag = bool(_df)
        _sif = self.bites[self.idx] & 0x10
        self.splice_immediate_flag = bool(_sif)
        self.idx += 1

    def _parse_components(self):
        self.component_count = self.bites[self.idx]
        self.idx += 1
        self.components = []
        for i in range(0, self.component_count):
            self.components[i] = self.bites[self.idx]
            self.idx += 1

    def _parse_uniq(self):
        _end = self.idx + 2
        self.unique_program_id = ifb(self.bites[self.idx : _end])
        self.idx = _end

    def _parse_avail(self):
        self.avail_num = self.bites[self.idx]
        self.idx += 1
        self.avail_expected = self.bites[self.idx]
        self.idx += 1

    def decode(self):
        """
        SpliceInsert.decode
        """
        self._parse_event()
        if not self.splice_event_cancel_indicator:
            self._parse_flags()
            if self.program_splice_flag:
                if not self.splice_immediate_flag:
                    super().decode()
            if not self.program_splice_flag:
                self._parse_components()
                if not self.splice_immediate_flag:
                    super().decode()
            if self.duration_flag:
                self._parse_break()
            self._parse_uniq()
            self._parse_avail()


command_map = {
    0: SpliceNull,
    5: SpliceInsert,
    6: TimeSignal,
    7: BandwidthReservation,
    255: PrivateCommand,
}


def mk_command(sct, bites):
    if sct in command_map:
        cmd = command_map[sct](bites)
        return cmd
    return False
