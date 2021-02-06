import struct
from bitn import BitBin
import threefive
from threefive.descriptors import SegmentationDescriptor


"""

Custom MPU Parser Example

Create a function that takes a bytearray containing the MPU bytes and its length.
The return value is how the MPU will be represented in the JSON output.

Each custom MPU parser function needs to be registered in the format_identifier_map.
The function will be called if the format_identifier matches the received MPU.

"""


SBSB_mpu = "FC305700000000000000FFF00506FE1E3E6FBE0041023F43554549000000007FBF0C3053425342360C014C12C933BA0000006EFF1000000000007A71507777734567327335000000000000000000000000000001000065F06E76"


def parse_private_upid_SBSB(bites, upid_length):
    bitbin = BitBin(bites)
    return {
        "private_cni": hex(bitbin.asint(16)),
        "private_version": bitbin.asint(8),
        "private_transmission_id": struct.unpack("<Q", bitbin.asbites(64))[0],
        "private_product_code": struct.unpack("<Q", bitbin.asbites(64))[0],
        "private_web_publication_key": bitbin.astext(25 * 8),
    }


SegmentationDescriptor.format_identifier_map = {
    # format_identifier, name, function
    0x53425342: ["SBSB", parse_private_upid_SBSB],
}

cuep = threefive.Cue(SBSB_mpu)
cuep.decode()
cuep.show()
