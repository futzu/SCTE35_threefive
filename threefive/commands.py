"""
commands.py
classes:
    SpliceCommand,
    BandwidthReservation,
    SpliceNull,
    PrivateCommand,
    TimeSignal,
    SpliceInsert
"""

from .tools import i2b, reserve, to_stderr


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

    def encode(self):
        """
        SpliceCommand.encode defines
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

    def encode(self):
        """
        encode private command
        """
        command_bytes = i2b(self.identifier, 4)
        return command_bytes


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

    def encode(self):
        """
        encode pts
        """
        if self.time_specified_flag:
            st_bytes = self.time_specified_flag << 39
            st_bytes += reserve(6) << 33  # forward six bits
            st_bytes += int(self.pts_time * 90000)
            return i2b(st_bytes, 5)
        return i2b(reserve(7), 1)


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

    def encode_break(self):  # 40bits
        """
        encodes SpliceInsert.break_auto_return
        and SpliceInsert.break_duration
        """
        break_bytes = self.break_auto_return << 39
        break_bytes += reserve(6) << 33  # forward 6
        break_bytes += int(self.break_duration * 90000)
        return i2b(break_bytes, 5)

    def decode(self, bitbin):
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

    def encode(self):
        bencoded = i2b(self.splice_event_id, 4)
        bencoded += i2b((self.splice_event_cancel_indicator << 7) + reserve(7), 1)
        if not self.splice_event_cancel_indicator:
            four_flags = self.out_of_network_indicator << 7
            four_flags += self.program_splice_flag << 6
            four_flags += self.duration_flag << 5
            four_flags += self.splice_immediate_flag << 4
            four_flags += reserve(4)
            bencoded += i2b(four_flags, 1)
            if self.program_splice_flag and not self.splice_immediate_flag:
                bencoded += super().encode()
            if not self.program_splice_flag:
                bencoded += i2b(self.component_count, 1)
                for i in range(0, self.component_count):
                    bencoded += i2b(self.components[i], 1)
                if not self.splice_immediate_flag:
                    bencoded += super().encode()
            if self.duration_flag:
                bencoded += self.encode_break()
            bencoded += i2b(self.unique_program_id, 2)
            bencoded += i2b(self.avail_num, 1)
            bencoded += i2b(self.avail_expected, 1)
            to_stderr(bencoded)
