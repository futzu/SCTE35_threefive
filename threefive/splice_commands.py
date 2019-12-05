from .util import *

class Splice_Command: 
    def break_duration(self,bb):
        self.break_auto_return= bb.read('bool')
        reserved(bb,6)
        self.break_duration= time_90k(bb.read('uint:33'))

    def splice_time(self,bb): #40bits
        self.time_specified_flag=bb.read('bool')
        if self.time_specified_flag:
            reserved(bb,6)
            self.pts_time=time_90k(bb.read('uint:33'))
        else: reserved(bb,7)


class Splice_Null(Splice_Command):
    def __init__(self,bb,sct):
        self.splice_type=sct
        self.name='Splice Null'

             
class Splice_Schedule(Splice_Command):
    def __init__(self,bb,sct):
        self.splice_type=sct
        self.name='Splice Schedule'
        splice_count=bb.read('uint:8')
        for i in range(0,splice_count):            
            self.splice_event_id= bb.read('uint:32')
            self.splice_event_cancel_indicator= bb.read('bool')
            reserved(bb,7)
            if not self.splice_event_cancel_indicator:
                self.out_of_network_indicator=bb.read('bool')
                self.program_splice_flag=bb.read('bool')
                self.duration_flag=bb.read('bool')
                reserved(bb,5)
                if self.program_splice_flag:  
                    self.utc_splice_time=bb.read('uint:32')
                else:
                    self.component_count=bb.read('uint:8')
                    self.components=[]
                    for j in range(0,self.component_count):
                        self.components[j]={
                            'component_tag': bb.read('uint:8'),
                            'utc_splice_time':bb.read('uint:32')}
                if self.duration_flag: self.break_duration(bb)
                self.unique_program_id= bb.read('uint:16')
                self.avail_num= bb.read('uint:8')
                self.avails_expected=bb.read('uint:8')


class Splice_Insert(Splice_Command):
    def __init__(self,bb,sct):
        self.splice_type=sct 
        self.name='Splice Insert'
        self.splice_event_id=bb.read('uint:32')
        self.splice_event_cancel_indicator=bb.read('bool')
        reserved(bb,7)
        if not self.splice_event_cancel_indicator:    
            self.out_of_network_indicator=bb.read('bool')
            self.program_splice_flag=bb.read('bool')
            self.duration_flag=bb.read('bool')
            self.splice_immediate_flag=bb.read('bool')
            reserved(bb,4)
            if self.program_splice_flag and not self.splice_immediate_flag: 
                self.splice_time(bb)
            if not self.program_splice_flag:
                self.component_count=bb.read('uint:8')
                self.components=[]
                for i in range(0,self.component_count):  
                    self.components[i]=bb.read('uint:8')
                if not self.splice_immediate_flag: self.splice_time(bb)
            if self.duration_flag: self.break_duration(bb) 
            self.unique_program_id=bb.read('uint:16')
            self.avail_num=bb.read('uint:8')
            self.avail_expected=bb.read('uint:8')


class Time_Signal(Splice_Command):
    def __init__(self,bb,sct):
        self.splice_type=sct
        self.name='Time Signal'
        self.splice_time(bb)


class Bandwidth_Reservation(Splice_Command):
    def __init__(self,bb,sct):
        self.splice_type=sct
        self.name='Bandwidth Reservation'


class Private_Command(Splice_Command):
    def __init__(self,bb,sct):
        self.splice_type=sct
        self.name='Private Command'

