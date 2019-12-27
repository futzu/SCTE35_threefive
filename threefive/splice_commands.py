from .util import *

class Splice_Command: 
    def break_duration(self,bs):
        self.break_auto_return= bs.boolean(1)
        reserved=bs.slice(6)
        self.break_duration= time_90k(bs.slice(33))

    def splice_time(self,bs): #40bits
        self.time_specified_flag=bs.boolean(1)
        if self.time_specified_flag:
            reserved=bs.slice(6)
            self.pts_time=time_90k(bs.slice(33))
        else: reserved=bs.slice(7)


class Splice_Null(Splice_Command):
    def __init__(self,bs,sct):
        self.splice_type=sct
        self.name='Splice Null'

             
class Splice_Schedule(Splice_Command):
    def __init__(self,bs,sct):
        self.splice_type=sct
        self.name='Splice Schedule'
        splice_count=bs.slice(8)
        for i in range(0,splice_count):            
            self.splice_event_id= bs.slice(32)
            self.splice_event_cancel_indicator= bs.boolean(1)
            reserved=bs.slice(7)
            if not self.splice_event_cancel_indicator:
                self.out_of_network_indicator=bs.boolean(1)
                self.program_splice_flag=bs.boolean(1)
                self.duration_flag=bs.boolean(1)
                reserved=bs.slice(5)
                if self.program_splice_flag:  
                    self.utc_splice_time=bs.slice(32)
                else:
                    self.component_count=bs.slice(8)
                    self.components=[]
                    for j in range(0,self.component_count):
                        self.components[j]={
                            'component_tag': bs.slice(8),
                            'utc_splice_time':bs.slice(32)}
                if self.duration_flag: self.break_duration(bs)
                self.unique_program_id= bs.slice(16)
                self.avail_num= bs.slice(8)
                self.avails_expected=bs.slice(8)


class Splice_Insert(Splice_Command):
    def __init__(self,bs,sct):
        self.splice_type=sct 
        self.name='Splice Insert'
        self.splice_event_id=bs.slice(32)
        self.splice_event_cancel_indicator=bs.boolean(1)
        reserved=bs.slice(7)
        if not self.splice_event_cancel_indicator:    
            self.out_of_network_indicator=bs.boolean(1)
            self.program_splice_flag=bs.boolean(1)
            self.duration_flag=bs.boolean(1)
            self.splice_immediate_flag=bs.boolean(1)
            reserved=bs.slice(4)
            if self.program_splice_flag and not self.splice_immediate_flag: 
                self.splice_time(bs)
            if not self.program_splice_flag:
                self.component_count=bs.slice(8)
                self.components=[]
                for i in range(0,self.component_count):  
                    self.components[i]=bs.slice(8)
                if not self.splice_immediate_flag: self.splice_time(bs)
            if self.duration_flag: self.break_duration(bs) 
            self.unique_program_id=bs.slice(16)
            self.avail_num=bs.slice(8)
            self.avail_expected=bs.slice(8)


class Time_Signal(Splice_Command):
    def __init__(self,bs,sct):
        self.splice_type=sct
        self.name='Time Signal'
        self.splice_time(bs)


class Bandwidth_Reservation(Splice_Command):
    def __init__(self,bs,sct):
        self.splice_type=sct
        self.name='Bandwidth Reservation'


class Private_Command(Splice_Command):
    def __init__(self,bs,sct):
        self.splice_type=sct
        self.name='Private Command'

