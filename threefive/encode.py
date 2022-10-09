"""
encode.py

threefive.encode has helper functions for Cue encoding.

"""


from .commands import SpliceNull, SpliceInsert, TimeSignal
from .cue import Cue


def mk_splice_null():
    """
    mk_splice_null returns a Cue
    with a Splice Null
    """
    cue = Cue()
    sn = SpliceNull()
    cue.command = sn
    cue.encode()
    return cue


def mk_time_signal(pts=None):
    """
     mk_time_signal returns a Cue
     with a Time Signal

     if pts is NOT set:
         time_specified_flag   False

    if pts IS set:
         time_specified_flag   True
         pts_time              pts

    """
    cue = Cue()
    ts = TimeSignal()
    ts.time_specified_flag = False
    if pts:
        pts = float(pts)
        ts.time_specified_flag = True
        ts.pts_time = pts
    cue.command = ts
    cue.encode()
    return cue


def mk_splice_insert(event_id, pts, duration=None):
    """
    mk_cue returns a Cue
    with a Splice Insert.

    splice_event_id = event_id

    If duration is NOT set,
        out_of_network_indicator   False
        time_specified_flag        False
        duration_flag              False
        splice_immediate_flag      True

    if duration IS set:
        out_of_network_indicator   True
        time_specified_flag        True
        duration_flag              True
        splice_immediate_flag      False
        break_auto_return          True
        break_duration             duration
        pts_time                   pts

    """
    pts = float(pts)
    cue = Cue()
    # default is a CUE-IN
    sin = SpliceInsert()
    sin.splice_event_id = event_id
    sin.splice_event_cancel_indicator = False
    sin.out_of_network_indicator = False
    sin.time_specified_flag = False
    sin.program_splice_flag = True
    sin.duration_flag = False
    sin.splice_immediate_flag = True
    sin.unique_program_id = event_id
    sin.avail_num = 0
    sin.avail_expected = 0
    # If we have a duration, make a CUE-OUT
    if duration is not None:
        duration = float(duration)
        sin.time_specified_flag = True
        sin.break_duration = duration
        sin.break_auto_return = True
        sin.splice_immediate_flag = False
        sin.duration_flag = True
        sin.out_of_network_indicator = True
        sin.pts_time = pts
    cue.command = sin  # Add SpliceInsert to the SCTE35 cue
    cue.encode()
    return cue
