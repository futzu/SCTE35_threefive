class SpliceCommand:
    '''
    command.SpliceCommand handles all splice commands.
    '''
    def parse(self,cmd_type,bitbin): 
        '''
        SpliceCommand.parse calls a method 
        depending on the value of cmd_type
        '''
        cmd_map = {0: self.splice_null,
            4: self.splice_schedule,
            5: self.splice_insert,
            6: self.time_signal,
            7: self.bandwidth_reservation,
            255: self.private_command }
        cmd_map[cmd_type](bitbin)

    def __repr__(self):
        return str(vars(self))
    
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

    def splice_null(self,bitbin):
        """
        Table 7 - splice_null()
        """
        self.name = "Splice Null"
        self.splice_command_length = 0

    def splice_schedule(Self,bitbin):
        """
        Table 8 - splice_schedule()
        """
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
                if self.duration_flag: self.break_duration(bitbin)
                self.unique_program_id = bitbin.asint(16)
                self.avail_num = bitbin.asint(8)
                self.avails_expected = bitbin.asint(8)
      
    def splice_insert(self,bitbin):
        """
        Table 9 - splice_insert()
        """
        self.name = "Splice Insert"
        self.splice_event_id = bitbin.asint(32) # uint32
        self.splice_event_cancel_indicator = bitbin.asflag(1)
        bitbin.forward(7) #uint8
        if not self.splice_event_cancel_indicator:
            self.out_of_network_indicator = bitbin.asflag(1)
            self.program_splice_flag = bitbin.asflag(1)
            self.duration_flag = bitbin.asflag(1)
            self.splice_immediate_flag = bitbin.asflag(1)
            bitbin.forward(4) #uint8
            if self.program_splice_flag and not self.splice_immediate_flag:
                self.splice_time(bitbin) # uint8 + uint32
            if not self.program_splice_flag:
                self.component_count = bitbin.asint(8)# uint 8
                self.components = []
                for i in range(0, self.component_count):
                    self.components[i] = bitbin.asint(8)
                if not self.splice_immediate_flag: self.splice_time(bitbin)
            if self.duration_flag: self.parse_break(bitbin)
            self.unique_program_id = bitbin.asint(16)
            self.avail_num = bitbin.asint(8)
            self.avail_expected = bitbin.asint(8)
            
    def time_signal(self, bitbin):
        """
        Table 10 - time_signal()
        """
        self.time_specified_flag = None
        self.pts_time = None
        self.name = "Time Signal"
        self.splice_time(bitbin)

    def bandwidth_reservation(self, bitbin):
        """
        Table 11 - bandwidth_reservation()
        """
        self.name = "Bandwidth Reservation"

    def private_command(self, bitbin):
        """
        Table 12 - private_command()
        """
        self.name = "Private Command"
        self.identifier = bitbin.asint(32)
