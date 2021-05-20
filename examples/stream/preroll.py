"""

! Requires threefive 2.2.88+ !

Shows preroll using PCR and PTS
for the time of the SCTE-35 packet.
"""
import sys
from threefive import Stream

def show_preroll(cue):
    if cue.command.pts_time:
        if cue.packet_data:
            two = f' Splice Time: {cue.command.pts_time} Preroll:'
            if "pcr" in cue.packet_data:
                pcr_preroll = cue.command.pts_time - cue.packet_data['pcr']
                two += f' (PCR): {round(pcr_preroll,6)}'
            if "pts" in cue.packet_data:
                pts_preroll = cue.command.pts_time - cue.packet_data['pts']
                two+= f' (PTS): {round(pts_preroll,6)}'
            print(two)


def do():
    args = sys.argv[1:]
    for arg in args:
        print(f"file: {arg} with PCR")
        with open(arg, "rb") as vid:
            strm = Stream(vid, show_null=True)
            strm.decode_pcr(func=show_preroll)
        print(f"file: {arg} with PTS")
        with open(arg, "rb") as vid:
            strm = Stream(vid, show_null=True)
            strm.decode_fu(func=show_preroll)


if __name__ == "__main__":
    do()
