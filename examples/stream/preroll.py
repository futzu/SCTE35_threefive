"""
Pre-roll is the difference in time between when a SCTE-35 packet
is inserted in a MPEGTS stream and the splice time of the SCTE-35 Cue.

"""

import sys
from threefive import Stream


def show_preroll(cue):
    """
    Print Splice Time, pre-roll and the base64 encoded SCTE-35 Cue.
    """
    if cue.command.pts_time:
        if cue.packet_data:
            out = f"{cue.command.pts_time},"
            if cue.packet_data.pts and cue.command.pts_time:
                pts_preroll = cue.command.pts_time - cue.packet_data.pts
                out += f"\t{pts_preroll:.6f},"
            out +=f"\t{cue.encode()}"
            print(out)


def do():
    """
    do processes multiple command line args
    """
    args = sys.argv[1:]
    for arg in args:
        print(f"Input: {arg}")
        print("Splice Time,\tPre-roll,\tCue")
        strm = Stream(arg, show_null=False)
        """
        threefive.Stream.decode accepts an optional function
        to be used to when a Cue is found. The function must
        meet the interface func(cue).

        In this example, we are using the function show_preroll.
        """
        strm.decode(func=show_preroll)


if __name__ == "__main__":
    do()
