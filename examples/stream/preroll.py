import sys
from threefive import Stream
"""
Show the preroll, the difference between
the SCTE35 packet data PTS and PTS of the splice command. 

Usage:
python3  preroll.py vid.ts

Program: 1050   Splice Insert @21940.656778     Splice Time: 21951.133267       Preroll: 10.476489
Program: 1050   Splice Insert @21942.672778     Splice Time: 21951.133267       Preroll: 8.460489
Program: 1050   Splice Insert @21944.688778     Splice Time: 21951.133267       Preroll: 6.444489
Program: 1010   Splice Insert @22508.436511     Splice Time: 22516.907656       Preroll: 8.471145
Program: 1010   Splice Insert @22510.452511     Splice Time: 22516.907656       Preroll: 6.455145
Program: 1050   Splice Insert @22015.680778     Splice Time: 22026.133267       Preroll: 10.452489
Program: 1050   Splice Insert @22017.696778     Splice Time: 22026.133267       Preroll: 8.436489
Program: 1050   Splice Insert @22019.712778     Splice Time: 22026.133267       Preroll: 6.420489
Program: 1040   Splice Insert @22857.8786       Splice Time: 22864.350067       Preroll: 6.471467
Program: 1040   Splice Insert @22863.9266       Splice Time: 22870.350067       Preroll: 6.423467
Program: 1010   Splice Insert @22688.436511     Splice Time: 22696.907656       Preroll: 8.471145
Program: 1010   Splice Insert @22690.452511     Splice Time: 22696.907656       Preroll: 6.455145
Program: 1040   Splice Insert @22953.9266       Splice Time: 22960.350067       Preroll: 6.423467
Program: 1010   Splice Insert @23508.372511     Splice Time: 23516.827656       Preroll: 8.455145
Program: 1010   Splice Insert @23510.388511     Splice Time: 23516.827656       Preroll: 6.439145
Program: 1010   Splice Insert @23688.372511     Splice Time: 23696.827656       Preroll: 8.455145
Program: 1010   Splice Insert @23690.388511     Splice Time: 23696.827656       Preroll: 6.439145
Program: 1030   Splice Insert @23676.9783       Splice Time: 23683.480033       Preroll: 6.501733

"""


def show_preroll(cue):
    if cue.command.pts_time:
        print(f'Program: {cue.packet_data["program"]}\t{cue.command.name} @{cue.packet_data["pts"]}\tSplice Time: {cue.command.pts_time}\tPreroll: {cue.packet_data["preroll"]}')


def do():
    args = sys.argv[1:]
    for arg in args:
        print(f'next file: {arg}')
        with open(arg,'rb') as vid:
            strm = Stream(vid,show_null=True)
            strm.decode(func=show_preroll)

if __name__ == "__main__":
    do()
