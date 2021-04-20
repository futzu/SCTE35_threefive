import sys
from bitn import BitBin
from threefive import Cue, Stream

"""
Custom UPID handling example for Richard.
Parse Private data and insert the values into the descriptor
under segmentation_upid

   "descriptors": [
        {
            "tag": 2,
            "descriptor_length": 63,
            "identifier": "CUEI",
            "name": "Segmentation Descriptor",
            "segmentation_event_id": "0x0",
            "segmentation_event_cancel_indicator": false,
            "components": [],
            "program_segmentation_flag": true,
            "segmentation_duration_flag": false,
            "delivery_not_restricted_flag": true,
            "segmentation_message": "Content Identification",
            "segmentation_upid_type": 12,
            "segmentation_upid_length": 48,

            "segmentation_upid": {
                "format_identifier": "0x53425342",
                "private_data": "0x360c014c12c933ba0000006eff1000000000007a715077777345673273350000000000000000000000000000",


# These are Added

                "private_cni": "0x360c",
                "private_version": 1,
                "private_transmission_id": 5481664920464392192,
                "private_product_code": 7998129055419334656,
                "private_web_publication_key": "zqPwwsEg2s5\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000\u0000"
# End
            },



            "segmentation_type_id": 1,
            "segment_num": 0,
            "segments_expected": 0
        }
    ],


"""


SBSB_ID = "0x53425342"
SBSB_mpu = "FC305700000000000000FFF00506FE1E3E6FBE0041023F43554549000000007FBF0C3053425342360C014C12C933BA0000006EFF1000000000007A71507777734567327335000000000000000000000000000001000065F06E76"


def chk_SBSB(d):
    if d.tag == 2:
        if d.segmentation_upid_type == 12:
            if d.segmentation_upid["format_identifier"] == SBSB_ID:
                sbsb = parse_SBSB(d.segmentation_upid["private_data"])
                # add values returned from parse_SBSB to descriptor
                d.segmentation_upid.update(sbsb)


def parse_SBSB(pdata):
    """
    Parse  UPID Private data
    """
    bites = bytes.fromhex(pdata[2:])
    bitbin = BitBin(bites)
    return {
        "private_cni": bitbin.ashex(16),
        "private_version": bitbin.asint(8),
        "private_transmission_id": bitbin.asint(64),
        "private_product_code": bitbin.asint(64),
        "private_web_publication_key": bitbin.asascii(200),
    }


def do(cue):
    for d in cue.descriptors:
        chk_SBSB(d)
    cue.show()


def do_cue(scte35):
    mpu_cue = Cue(scte35)
    mpu_cue.decode()
    do(mpu_cue)


def do_stream():
    args = sys.argv[1:]
    for arg in args:
        print(f"Next File: {arg}")
        with open(arg, "rb") as tsdata:
            st = Stream(tsdata)
            st.decode(func=do)


if __name__ == "__main__":
    # parse file names if present
    if len(sys.argv) > 1:
        do_stream()
    else:
        # parse the encoded string
        do_cue(SBSB_mpu)
