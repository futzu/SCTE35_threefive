"""
Custom UPID handling example for Richard.
Parse Private data and insert the values into the descriptor
under segmentation_upid

# These are Added

"private_cni"
"private_version"
"private_transmission_id"
"private_product_code"
"private_web_publication_key"

"""
import sys
from threefive.bitn import BitBin
from threefive import Cue, Stream


SBSB_ID = "0x53425342"
SBSB_MPU = "FC305700000000000000FFF00506FE1E3E6FBE0041023F43554549000000007FBF0C3053425342360C014C12C933BA0000006EFF1000000000007A71507777734567327335000000000000000000000000000001000065F06E76"


def chk_sbsb(descptr):
    """
    chk_sbsb checks a Splice Descriptor for SBSB_ID
    """
    if descptr.tag == 2:
        if descptr.segmentation_upid_type == 12:
            if descptr.segmentation_upid["format_identifier"] == SBSB_ID:
                sbsb = parse_sbsb(descptr.segmentation_upid["private_data"])
                # add values returned from parse_SBSB to descriptor
                descptr.segmentation_upid.update(sbsb)


def parse_sbsb(pdata):
    """
    Parse  UPID Private data
    """
    bites = bytes.fromhex(pdata[2:])
    bitbin = BitBin(bites)
    return {
        "private_cni": bitbin.as_hex(16),
        "private_version": bitbin.as_int(8),
        "private_transmission_id": bitbin.as_int(64),
        "private_product_code": bitbin.as_int(64),
        "private_web_publication_key": bitbin.as_ascii(200),
    }


def do_descriptors(cue):
    """
    do - process cue.descriptors
    """
    for descptr in cue.descriptors:
        chk_sbsb(descptr)
    cue.show()


def do_cue(scte35):
    """
    do_cue, decode Cue and process if needed.
    """
    mpu_cue = Cue(scte35)
    mpu_cue.decode()
    do_descriptors(mpu_cue)


def do_stream():
    """
    do_stream processes a list of streams on the command line
    """
    args = sys.argv[1:]
    for arg in args:
        print(f"Next File: {arg}")
        strm = Stream(arg)
        strm.decode(func=do_descriptors)


if __name__ == "__main__":
    # parse file names if present
    if len(sys.argv) > 1:
        do_stream()
    else:
        # parse the encoded string
        do_cue(SBSB_MPU)
