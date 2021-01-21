"""
SCTE35 Splice Commands
"""
from bitn import BitBin
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

    def encode(self):
        """
        encode
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

    def __init__(self, bites=None):
        super().__init__(bites)
        self.identifier = None

    def decode(self):
        """
        decode private command
        """
        self.name = "Private Command"
        self.identifier = ifb(
            self.bites[0:3]
        )  # 3 bytes of 8 bits = 24 bits
        self.command_length = 3

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
        self.parse_pts(bitbin)
        self._set_len(start,bitbin.idx)

    def _set_len(self,start,end):
        self.command_length = (start - end ) >> 3

    def parse_pts(self, bitbin):
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

    def parse_break(self, bitbin):
        """
        SpliceInsert.parse_break(bitbin) is called
        if SpliceInsert.duration_flag is set
        """
        self.break_auto_return = bitbin.asflag(1)
        bitbin.forward(6)
        self.break_duration = bitbin.as90k(33)

    def _parse_flags(self,bitbin):
        """
        SpliceInsert._parse_flags set fout flags
        and is called from SpliceInsert.decode()
        """
        self.out_of_network_indicator = bitbin.asflag(1)
        self.program_splice_flag = bitbin.asflag(1)
        self.duration_flag = bitbin.asflag(1)
        self.splice_immediate_flag = bitbin.asflag(1)
        bitbin.forward(4)

    def _parse_components(self,bitbin):
        """
        SpliceInsert._parse_components loops
        over SpliceInsert.components,
        and is called from SpliceInsert.decode()
        """
        self.component_count = bitbin.asint(8)
        self.components = []
        for i in range(0, self.component_count):
            self.components[i] = bitbin.asint(8)

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
            self._parse_flags(bitbin)
            if self.program_splice_flag:
                if not self.splice_immediate_flag:
                    self.parse_pts(bitbin)
            else:
                self._parse_components(bitbin)
                if not self.splice_immediate_flag:
                    self.parse_pts(bitbin)
            if self.duration_flag:
                self.parse_break(bitbin)
            self.unique_program_id = bitbin.asint(16)
            self.avail_num = bitbin.asint(8)
            self.avail_expected = bitbin.asint(8)
        self._set_len(start,bitbin.idx)


command_map = {
    0: SpliceNull,
    5: SpliceInsert,
    6: TimeSignal,
    7: BandwidthReservation,
    255: PrivateCommand,
}

def mk_splice_command(sct, bites):
    """
    returns an instance
    command_map[sct]
    """
    if sct in command_map:
        cmd = command_map[sct](bites)
        cmd.decode()
        return cmd
    return False
