"""
cue2vtt.py

uses webvtt subtitles to display splice insert cue out and cue In.

Usage:

pypy3 cue2vtt.py thevideo.ts | mplayer thevideo.ts -sub -

"""

import sys
from threefive import Stream
import time

def ts_to_vtt(timestamp):
    """
    ts_to_vtt converts timestamp into webvtt times
    """
    hours, seconds = divmod(timestamp, 3600)
    mins, seconds = divmod(seconds, 60)
    seconds = round(seconds, 3)
    return f"{int(hours):02}:{int(mins):02}:{seconds:02}"


def scte35_to_vtt(cue):
    """
    scte35_to_vtt prints splice insert cue out and cue in via webvtt
    """
    start =0
    end = 0
    duration = None
    pts_time = None
    upid = None
    seg_mesg= None
    now = cue.packet_data.pts
    if cue.command.has("pts_time"):
        start= pts_time = cue.command.pts_time+cue.info_section.pts_adjustment
        if pts_time > now:  time.sleep(pts_time -now)
    if cue.command.has("break_duration"):
        duration = cue.command.break_duration
    for d in cue.descriptors:
        if d.has("segmentation_duration"):
            duration = d.segmentation_duration
            if d.has("segmentation_upid"):
                upid = d.segmentation_upid
            if d.has("segmentation_message"):
                seg_mesg = d.segmentation_message
    if start and duration:
        end = start + duration
    if end == 0:
        end = start+4

    print(f"{ts_to_vtt(start)} --> {ts_to_vtt(end)} ")

    print(f"Cmd: {cue.command.name}    ")
    if pts_time:
        print(f"PTS:  {pts_time}  ")
    if duration:
        print(f"Duration:  {round(duration,3)} " )
    if seg_mesg:
        print(seg_mesg)
    if upid:
        print(f"Upid: {upid}")
    print()


if __name__ == "__main__":
    arg = sys.argv[1]
    print("WEBVTT\n\n\n")
    strm = Stream(arg)
    strm.decode(func=scte35_to_vtt)
