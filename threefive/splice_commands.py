class Splice_Command:
    def __init__(self):
        pass

    def decode(self,bitn):
        pass

    def parse_break(self, bitbin):
        self.break_auto_return = bitbin.asflag(1)
        bitbin.forward(6)
        self.break_duration = bitbin.as90k(33)

    def splice_time(self, bitbin):  # 40bits
        self.time_specified_flag = bitbin.asflag(1)
        if self.time_specified_flag:
            bitbin.forward(6)
            self.pts_time = bitbin.as90k(33)
        else:
            bitbin.forward(7)


class Splice_Null(Splice_Command):
    """
    Table 7 - splice_null()
    """
    def decode(self,bitbin):
        self.name = "Splice Null"


class Splice_Schedule(Splice_Command):
    """
    Table 8 - splice_schedule()
    """

    def decode(self, bitbin):
        self.name = "Splice Schedule"
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


class Splice_Insert(Splice_Command):
    """
    Table 9 - splice_insert()
    """
    def __init__(self):
        self.splice_event_id = None
        self.splice_event_cancel_indicator = None
        self.out_of_network_indicator = None
        self.program_splice_flag = None
        self.duration_flag = None
        self.splice_immediate_flag = None
        self.component_count = None
        self.components = []
        self.duration_flag=None
        self.unique_program_id = None
        self.avail_num = None
        self.avail_expected = None
        self.break_auto_return = None
        self.break_duration = None
        self.time_specified_flag = None
        self.pts_time = None


    def decode(self, bitbin):
        self.name = "Splice Insert"
        self.splice_event_id = bitbin.asint(32)
        self.splice_event_cancel_indicator = bitbin.asflag(1)
        bitbin.forward(7)
        if not self.splice_event_cancel_indicator:
            self.out_of_network_indicator = bitbin.asflag(1)
            self.program_splice_flag = bitbin.asflag(1)
            self.duration_flag = bitbin.asflag(1)
            self.splice_immediate_flag = bitbin.asflag(1)
            bitbin.forward(4)
            if self.program_splice_flag and not self.splice_immediate_flag:
                self.splice_time(bitbin)
            if not self.program_splice_flag:
                self.component_count = bitbin.asint(8)
                self.components = []
                for i in range(0, self.component_count):
                    self.components[i] = bitbin.asint(8)
                if not self.splice_immediate_flag:
                    self.splice_time(bitbin)
            if self.duration_flag:
                self.parse_break(bitbin)
            self.unique_program_id = bitbin.asint(16)
            self.avail_num = bitbin.asint(8)
            self.avail_expected = bitbin.asint(8)


class Time_Signal(Splice_Command):
    """
    Table 10 - time_signal()
    """
    def __init__(self):
        self.time_specified_flag = None
        self.pts_time = None

    def decode(self, bitbin):
        self.name = "Time Signal"
        self.splice_time(bitbin)


class Bandwidth_Reservation(Splice_Command):
    """
    Table 11 - bandwidth_reservation()
    """
    def decode(self, bitbin):
        self.name = "Bandwidth Reservation"


class Private_Command(Splice_Command):
    """
    Table 12 - private_command()
    """
    def __init__(self):
        self.identifier = None

    def decode(self, bitbin):
        self.name = "Private Command"
        self.identifier = bitbin.asint(32)
        return False
