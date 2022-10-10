from .bitn import BitBin
from .base import SCTE35Base


class SpliceCommand(SCTE35Base):
    def __init__(self, bites=None):
        self.avail_expected = None
        self.avail_num = None
        self.bites = bites
        self.break_autoreturn = None
        self.break_duration = None
        self.command_length = 0
        self.command_type = None
        self.component_count = None
        self.components = None
        self.duration_flag = None
        self.identifier = None
        self.name = None
        self.out_of_network_indicator = None
        self.program_splice_flag = None
        self.pts = None
        self.splice_event_cancel_indicator = None
        self.splice_event_id = None
        self.splice_immediate_flag = None
        self.time_specified_flag = None
        self.unique_program_id = None

    def _set_len(self, start, end):
        """
        _set_len sets
        self.command_length
        """
        self.command_length = (start - end) >> 3

    def decode(self, cmd_type):

        command_map = {
            0: self.splice_null,
            5: self.splice_insert,
            6: self.time_signal,
            7: self.bandwidth_reservation,
            255: self.private,
        }
        if cmd_type in command_map.keys():
            self.command_type = cmd_type
            command_map[self.command_type]()

    def BandwidthReservation(self, bitn):
        self.name = "Bandwidth Reservation"
        bitn.forward(0)

    def private(self, bitn):
        """
        PrivateCommand.decode method
        """
        self.name = "Private Command"
        self.identifier = int.from_bytes(self.bites[0:3], byteorder="big")
        self.bites = self.bites[3:]

    def splice_null(self, bitn):
        self.name = "Splice Null"
        bitn.forward(0)

    def splice_insert(self, bitn):
        """
        SpliceInsert.decode
        """
        bitn = BitBin(self.bites)
        start = bitn.idx
        self.name = "Splice Insert"
        self.splice_event_id = bitn.as_hex(32)
        self.splice_event_cancel_indicator = bitn.as_flag()
        bitn.forward(7)
        if not self.splice_event_cancel_indicator:
            self.out_of_network_indicator = bitn.as_flag()
            self.program_splice_flag = bitn.as_flag()
            self.duration_flag = bitn.as_flag()
            self.splice_immediate_flag = bitn.as_flag()
            bitn.forward(4)
            if self.program_splice_flag:
                if not self.splice_immediate_flag:
                    self.splice_time(bitn)
            else:
                self.component_count = bitbin.as_int(8)
                self.components = []
                for i in range(0, self.component_count):
                    self.components[i] = bitbin.as_int(8)
                if not self.splice_immediate_flag:
                    self.splice_time(bitn)
            if self.duration_flag:
                self.parse_break(bitn)
            self.unique_program_id = bitn.as_int(16)
            self.avail_num = bitn.as_int(8)
            self.avail_expected = bitn.as_int(8)

    def parse_break(self, bitn):
        self.break_auto_return = bitn.as_flag()
        bitn.forward(6)
        self.break_duration = bitn.as_90k(33)

    def splice_time(self, bitn):
        self.time_specified_flag = bitn.as_flag()
        if self.time_specified_flag:
            bitn.forward(6)
            self.pts_time = bitn.as_90k(33)
        else:
            bitn.forward(7)

    def time_signal(self):
        """
        TimeSignal.decode method
        """
        self.Name = "Time Signal"
        self.splice_time(bitn)
        bitn = BitBin(self.bites)
        start = bitn.idx
        self._splice_time(bitn)
        self._set_len(start, bitn.idx)
