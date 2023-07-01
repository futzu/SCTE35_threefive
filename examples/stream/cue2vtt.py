"""
cue2vtt.py

uses webvtt subtitles to display splice insert cue out and cue In.

Usage:

pypy3 cue2vtt.py thevideo.ts | mplayer thevideo.ts -sub -

"""

import sys
from threefive import Stream


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
    pts_time = cue.packet_data.pts
    start = cue.packet_data.pts
    if "pts_time" in cue.command.get():
        pts_time = cue.command.pts_time
    if "break_duration" in cue.command.get():
        duration = cue.command.break_duration
        end =  start + duration -1
    else:
        for d in cue.descriptors:
            if "segmentation_duration" in d.get():
                duration = d.segmentation_duration
                end = start + duration -1
    if end == 0:
        end = start+4
            
    print(f"{ts_to_vtt(start)} --> {ts_to_vtt(end)} ")

    print(f"Cmd: {cue.command.name}    ")
    if pts_time:
        print(f"PTS:  {pts_time}  ")
    if duration:
        print(f"Duration:  {round(duration,3)} " )
    print()


if __name__ == "__main__":
    arg = sys.argv[1]
    print("WEBVTT\n\n\n")
    strm = Stream(arg)
    strm.decode(func=scte35_to_vtt)

