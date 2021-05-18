import sys
from threefive import Stream

"""
Show the preroll, the difference between
the SCTE35 packet data PTS and PTS of the splice command.

Usage:
python3  preroll2.py vid.ts

21951.133267(preroll time = 10.476489)
21951.133267(preroll time = 8.460489)
21951.133267(preroll time = 6.444489)
22516.907656(preroll time = 8.471145)
22516.907656(preroll time = 6.455145)
22026.133267(preroll time = 10.452489)
22026.133267(preroll time = 8.436489)
22026.133267(preroll time = 6.420489)
22864.350067(preroll time = 6.471467)
22870.350067(preroll time = 6.423467)
22696.907656(preroll time = 8.471145)
22696.907656(preroll time = 6.455145)
22960.350067(preroll time = 6.423467)
23516.827656(preroll time = 8.455145)
23516.827656(preroll time = 6.439145)
23696.827656(preroll time = 8.455145)
23696.827656(preroll time = 6.439145)
23683.480033(preroll time = 6.501733)



"""


def show_preroll(cue):
    if cue.command.pts_time:
        if cue.packet_data:
            if "pts" in cue.packet_data:
                two = f'{cue.command.pts_time}(preroll time = {cue.packet_data["preroll"]})'
                print(two)


def do():
    args = sys.argv[1:]
    for arg in args:
        with open(arg, "rb") as vid:
            strm = Stream(vid, show_null=True)
            strm.decode(func=show_preroll)


if __name__ == "__main__":
    do()
