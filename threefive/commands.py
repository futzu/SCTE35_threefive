"""
SCTE35 Splice Commands
"""
from .tools import ifb


class SpliceCommand:
    """
    Base class, not used directly.
    """

    def __init__(self, payload):
        self.idx = 0
        self.payload = payload
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
        self.identifier = ifb(self.payload[self.idx : self.idx + 3])


class TimeSignal(SpliceCommand):
    """
    Table 10 - time_signal()
    """

    def __init__(self, payload):
        super().__init__(payload)
        self.name = "Time Signal"
        self.time_specified_flag = None
        self.pts_time = None

    @staticmethod
    def as90k(five_bites):
        ttb = five_bites[0] & 1 << 32 | ifb(five_bites[1:5])
        return ttb / 90000.0

    def decode(self):  # 40bits
        """
        decode pts
        """
        self.time_specified_flag = self.payload[self.idx] >> 7 is 1
        if self.time_specified_flag:
            self.pts_time = self.payload[self.idx] & 1 << 32
            self.pts_time |= self.payload[self.idx + 1] << 24
            self.pts_time |= self.payload[self.idx + 2] << 16
            self.pts_time |= self.payload[self.idx + 3] << 8
            self.pts_time |= self.payload[self.idx + 4]
            self.pts_time /= 90000.0
            self.pts_time = round(self.pts_time, 6)
            self.idx += 5
        else:
            self.idx += 1


class SpliceInsert(TimeSignal):
    """
    Table 9 - splice_insert()
    """

    def __init__(self, payload):
        super().__init__(payload)
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

    def parse_break(self):
        """
        SpliceInsert.parse_break(bitbin) is called
        if SpliceInsert.duration_flag is set
        """
        self.break_auto_return = self.payload[self.idx] >> 7 is 1
        self.break_duration = self.payload[self.idx] & 1 << 32
        self.break_duration |= self.payload[self.idx + 1] << 24
        self.break_duration |= self.payload[self.idx + 2] << 16
        self.break_duration |= self.payload[self.idx + 3] << 8
        self.break_duration |= self.payload[self.idx + 4]
        self.break_duration /= 90000.0
        self.break_duration = round(self.break_duration, 6)
        self.idx += 4

    def decode(self):
        """
        SpliceInsert.decode
        """
        self.splice_event_id = ifb(self.payload[self.idx : self.idx + 4])
        self.idx += 4
        self.splice_event_cancel_indicator = self.payload[self.idx] >> 7 is 1
        self.idx += 1
        if not self.splice_event_cancel_indicator:
            self.out_of_network_indicator = self.payload[self.idx] >> 7 is 1
            self.program_splice_flag = (self.payload[self.idx] >> 6) & 1 is 1
            self.duration_flag = (self.payload[self.idx] >> 5) & 1 is 1
            self.splice_immediate_flag = (self.payload[self.idx] >> 4) & 1 is 1
            self.idx += 1
            if self.program_splice_flag and not self.splice_immediate_flag:
                super().decode()  # uint8 + uint32
            if not self.program_splice_flag:
                self.component_count = self.payload[self.idx]
                self.idx += 1
                self.components = []
                for i in range(0, self.component_count):
                    self.components[i] = self.payload[self.idx]
                    self.idx += 1
                if not self.splice_immediate_flag:
                    super().decode()
            if self.duration_flag:
                self.parse_break()
            self.unique_program_id = ifb(self.payload[self.idx : self.idx + 2])
            self.idx += 2
            self.avail_num = self.payload[self.idx]
            self.idx += 1
            self.avail_expected = self.payload[self.idx]
            self.idx += 1


command_map = {
    0: SpliceNull,
    5: SpliceInsert,
    6: TimeSignal,
    7: BandwidthReservation,
    255: PrivateCommand,
}


def mk_command(sct, payload):
    if sct in command_map:
        cmd = command_map[sct](payload)
        return cmd
    return False
