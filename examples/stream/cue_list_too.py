"""
cue_list_too.py
Example to show how to get a
list of SCTE-35 cues as threefive.Cue instances,
and print a list of the pcr of the SCTE35 packet with the base64 Cue string.

Use like:

python3 cue_list_too.py myvideo.ts

Output:

PCR -> Cue
21940.651167  :  /DAvAAAAAAAA///wFAUAAAASf+/+dcFLSn4AZv8wAAES/wAKAAhDVUVJAAAAEuqoRz8=
21942.658133  :  /DAvAAAAAAAA///wFAUAAAASf+/+dcFLSn4AZv8wAAES/wAKAAhDVUVJAAAAEuqoRz8=
21944.665344  :  /DAvAAAAAAAA///wFAUAAAASf+/+dcFLSn4AZv8wAAES/wAKAAhDVUVJAAAAEuqoRz8=
22015.646556  :  /DAqAAAAAAAA///wDwUAAAASf0/+dihKegABEv8ACgAIQ1VFSQAAABIe1kvb
22017.653522  :  /DAqAAAAAAAA///wDwUAAAASf0/+dihKegABEv8ACgAIQ1VFSQAAABIe1kvb
22019.660733  :  /DAqAAAAAAAA///wDwUAAAASf0/+dihKegABEv8ACgAIQ1VFSQAAABIe1kvb
22508.448011  :  /DAvAAAAAAAA///wFAVAAAT2f+/+eMpEWX4A9zFAAAEL/wAKAAhDVUVJAAAACwRZmfY=
22510.424778  :  /DAvAAAAAAAA///wFAVAAAT2f+/+eMpEWX4A9zFAAAEL/wAKAAhDVUVJAAAACwRZmfY=
22688.424856  :  /DAqAAAAAAAA///wDwVAAAT2f0/+ecF1mQABC/8ACgAIQ1VFSQAAAAsuZVlR

"""
import sys

from threefive import Segment

if __name__ == "__main__":

    seg = Segment(sys.argv[1])
    seg.decode()

    print("\n\nPCR -> Cue")
    pcr_cue_map = {cue.packet_data.pcr: cue.encode() for cue in seg.cues}
    for ts in sorted(pcr_cue_map):
        print(ts, " : ", pcr_cue_map[ts])
