

class Splice_Command:
    def __init__(self,sct):
        self.splice_type=sct
    
    def break_duration(self,bs):
        self.break_auto_return= bs.asflag(1)
        reserved=bs.asint(6)
        self.break_duration= bs.as90k(33)

    def splice_time(self,bs): #40bits
        self.time_specified_flag=bs.asflag(1)
        if self.time_specified_flag:
            reserved=bs.asint(6)
            self.pts_time=bs.as90k(33)
        else: reserved=bs.asint(7)


class Splice_Null(Splice_Command):
    '''
    Table 7 - splice_null()
    '''
    def __init__(self,bs,sct):
        super().__init__(sct)
        self.name='Splice Null'

             
class Splice_Schedule(Splice_Command):
    '''
    Table 8 - splice_schedule()
    '''
    def __init__(self,bs,sct):
        super().__init__(sct)
        self.name='Splice Schedule'
        splice_count=bs.asint(8)
        for i in range(0,splice_count):            
            self.splice_event_id= bs.asint(32)
            self.splice_event_cancel_indicator= bs.asflag(1)
            reserved=bs.asint(7)
            if not self.splice_event_cancel_indicator:
                self.out_of_network_indicator=bs.asflag(1)
                self.program_splice_flag=bs.asflag(1)
                self.duration_flag=bs.asflag(1)
                reserved=bs.asint(5)
                if self.program_splice_flag:  
                    self.utc_splice_time=bs.asint(32)
                else:
                    self.component_count=bs.asint(8)
                    self.components=[]
                    for j in range(0,self.component_count):
                        self.components[j]={
                            'component_tag': bs.asint(8),
                            'utc_splice_time':bs.asint(32)}
                if self.duration_flag: self.break_duration(bs)
                self.unique_program_id= bs.asint(16)
                self.avail_num= bs.asint(8)
                self.avails_expected=bs.asint(8)


class Splice_Insert(Splice_Command):
    '''
    Table 9 - splice_insert()
    '''
    def __init__(self,bs,sct):
        super().__init__(sct)
        self.name='Splice Insert'
        self.splice_event_id=bs.asint(32)
        self.splice_event_cancel_indicator=bs.asflag(1)
        reserved=bs.asint(7)
        if not self.splice_event_cancel_indicator:    
            self.out_of_network_indicator=bs.asflag(1)
            self.program_splice_flag=bs.asflag(1)
            self.duration_flag=bs.asflag(1)
            self.splice_immediate_flag=bs.asflag(1)
            reserved=bs.asint(4)
            if self.program_splice_flag and not self.splice_immediate_flag: 
                self.splice_time(bs)
            if not self.program_splice_flag:
                self.component_count=bs.asint(8)
                self.components=[]
                for i in range(0,self.component_count):  
                    self.components[i]=bs.asint(8)
                if not self.splice_immediate_flag: self.splice_time(bs)
            if self.duration_flag: self.break_duration(bs) 
            self.unique_program_id=bs.asint(16)
            self.avail_num=bs.asint(8)
            self.avail_expected=bs.asint(8)


class Time_Signal(Splice_Command):
    '''
    Table 10 - time_signal()
    '''
    def __init__(self,bs,sct):
        super().__init__(sct)
        self.name='Time Signal'
        self.splice_time(bs)


class Bandwidth_Reservation(Splice_Command):
    '''
    Table 11 - bandwidth_reservation()
    '''
    def __init__(self,bs,sct):
        super().__init__(sct)
        self.name='Bandwidth Reservation'


class Private_Command(Splice_Command):
    '''
    Table 12 - private_command()
    '''
    def __init__(self,bs,sct):
        super().__init__(sct)
        self.name='Private Command'
        self.identifier=bs.asint(32)
        
