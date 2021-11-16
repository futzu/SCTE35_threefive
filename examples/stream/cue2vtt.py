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
    return f" {int(hours):02}:{int(mins):02}:{seconds:02}"


def scte35_to_vtt(cue):
    """
    scte35_to_vtt prints splice insert cue out and cue in via webvtt
    """
    ts = 0
    if cue.packet_data.pcr is not None:
        ts = cue.packet_data.pcr
    else:
        if cue.packet_data.pts is not None:
            ts = cue.packet_data.pts
    try:

        start = ts
        end = start + 5
        if cue.command.pts_time:
            start = cue.command.pts_time
        if cue.command.break_duration:
            end = start + cue.command.break_duration
        print(f"{ts_to_vtt(start)} --> {ts_to_vtt(end-1)}\nCue Out\n\n")
        print(f"{ts_to_vtt(end)} --> {ts_to_vtt(end+1)}\nCue In\n\n")
    except:
        print(f"{ts_to_vtt(ts)} --> {ts_to_vtt(ts+1)}\n{cue.command.name}\n\n")


if __name__ == "__main__":
    arg = sys.argv[1]
    print("WEBVTT\n\n\n")
    strm = Stream(arg)
    strm.decode(func=scte35_to_vtt)
