"""
SCTE35 Splice Commands
"""


class SpliceCommand:
    """
    Base class, not used directly.
    """

    def decode(self, bitbin):
        """
        SpliceCommand.decode defines
        a standard interface for
        SpliceCommand subclasses.
        """


class BandwidthReservation(SpliceCommand):
    """
    Table 11 - bandwidth_reservation()
    """

    def __init__(self):
        self.name = "Bandwidth Reservation"


class SpliceNull(SpliceCommand):
    """
    Table 7 - splice_null()
    """

    def __init__(self):
        """
         init splice null command
        """
        self.name = "Splice Null"
        self.splice_command_length = 0


class PrivateCommand:
    """
    Table 12 - private_command
    """

    def __init__(self):
        """
        init private command
        """
        self.name = "Private Command"
        self.identifier = None

    def decode(self, bitbin):
        """
        decode private command
        """
        self.identifier = bitbin.asint(32)


class TimeSignal:
    """
    Table 10 - time_signal()
    """

    def __init__(self):
        self.name = "Time Signal"
        self.time_specified_flag = None
        self.pts_time = None

    def decode(self, bitbin):  # 40bits
        """
        decode pts
        """
        self.time_specified_flag = bitbin.asflag(1)
        if self.time_specified_flag:
            bitbin.forward(6)
            self.pts_time = bitbin.as90k(33)
        else:
            bitbin.forward(7)


class SpliceInsert(TimeSignal):
    """
    Table 9 - splice_insert()
    """

    def __init__(self):
        super().__init__()
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

    def parse_break(self, bitbin):
        """
        SpliceInsert.parse_break(bitbin) is called
        if SpliceInsert.duration_flag is set
        """
        self.break_auto_return = bitbin.asflag(1)
        bitbin.forward(6)
        self.break_duration = bitbin.as90k(33)

    def decode(self, bitbin):
        """
        SpliceInsert.decode
        """
        self.splice_event_id = bitbin.asint(32)  # uint32
        self.splice_event_cancel_indicator = bitbin.asflag(1)
        bitbin.forward(7)  # uint8
        if not self.splice_event_cancel_indicator:
            self.out_of_network_indicator = bitbin.asflag(1)
            self.program_splice_flag = bitbin.asflag(1)
            self.duration_flag = bitbin.asflag(1)
            self.splice_immediate_flag = bitbin.asflag(1)
            bitbin.forward(4)  # uint8
            if self.program_splice_flag and not self.splice_immediate_flag:
                super().decode(bitbin)  # uint8 + uint32
            if not self.program_splice_flag:
                self.component_count = bitbin.asint(8)  # uint 8
                self.components = []
                for i in range(0, self.component_count):
                    self.components[i] = bitbin.asint(8)
                if not self.splice_immediate_flag:
                    super().decode(bitbin)
            if self.duration_flag:
                self.parse_break(bitbin)
            self.unique_program_id = bitbin.asint(16)
            self.avail_num = bitbin.asint(8)
            self.avail_expected = bitbin.asint(8)
