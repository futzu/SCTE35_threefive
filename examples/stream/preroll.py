"""

! Requires threefive 2.2.88+ !

Shows preroll using PCR and PTS
for the time of the SCTE-35 packet.
"""

import sys
from threefive import Stream


def show_preroll(cue):
    """
    show_preroll shows preroll times with pcr and pts.
    """
    if cue.command.pts_time:
        if cue.packet_data:
            two = f" Splice Time: {cue.command.pts_time} Preroll:"
            if cue.packet_data.pcr:
                pcr_preroll = cue.command.pts_time - cue.packet_data.pcr
                two += f" (PCR): {round(pcr_preroll,6)}"
            if cue.packet_data.pts:
                pts_preroll = cue.command.pts_time - cue.packet_data.pts
                two += f" (PTS): {round(pts_preroll,6)}"
            print(two)


def do():
    """
    do processes multiple command line args
    """
    args = sys.argv[1:]
    for arg in args:
        print(f"file: {arg}")
        strm = Stream(arg, show_null=False)
        strm.decode_fu(func=show_preroll)


if __name__ == "__main__":
    do()
