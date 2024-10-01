"""
threefive/upids.py

threefve.upids

classy Upids

cyclomatic complexity 1.689


"""
from .xml import Node


charset = "ascii"  # this isn't a constant pylint.

"""
set charset to None to return raw bytes
"""


class Upid:
    """
    Upid base class handles URI UPIDS
    """

    def __init__(self, bitbin=None, upid_type=0, upid_length=0):
        self.bitbin = bitbin
        self.upid_type = upid_type
        self.upid_name = upid_map[upid_type][0]
        self.upid_length = upid_length
        self.bit_length = upid_length << 3
        self.upid_value = None

    def decode(self):
        """
        decode Upid
        """
        self.upid_value = self.bitbin.as_charset(self.bit_length, charset)
        return self.upid_name, self.upid_value

    def encode(self, nbin ):
        """
        encode Upid
        """
        if self.upid.value:
            self.upid.value = self.upid.value.encode("utf8")
            nbin.add_bites(self.upid.value)

    def xml(self):
        """
        xml return a upid xml node
        """
        ud_attrs = { 'upid_type': self.upid_name, # this is for clarity
                    'segmentation_upid_type': self.upid_type,
                    'segmentation_upid_format':'hexbinary',
                    'segmentation_upid_length':self.upid_length,}
        return  Node('SegmentationUpid',attrs= ud_attrs, value=self.upid_value)




class NoUpid(Upid):
    """
    NoUpid class
    """

    def decode(self):
        """
        decode for no upid
        """
        return self.upid_name, None

    def encode(self, nbin ):
        """
        encode for no upid
        """
        nbin.forward(0)


class AirId(Upid):
    """
    Air Id Upid
    """

    def decode(self):
        """
        decode AirId
        """
        self.upid_value=self.bitbin.as_hex(self.bit_length)
        return self.upid_name, self.upid_value

    def encode(self, nbin ):
        """
        encode AirId
        """
        nbin.add_hex(self.upid_value, (self.upid_length << 3))


class Atsc(Upid):
    """
    ATSC Upid
    """

    def decode(self):
        """
        decode Atsc Upid
        """
        cont_size = self.bit_length - 32
        self.upid_value= {
            "TSID": self.bitbin.as_int(16),
            "reserved": self.bitbin.as_int(2),
            "end_of_day": self.bitbin.as_int(5),
            "unique_for": self.bitbin.as_int(9),
            "content_id": self.bitbin.as_charset(cont_size, charset),
        }
        return self.upid_name,self.upid_value


    def encode(self, nbin ):
        """
        encode Atsc
        """
        nbin.add_int(self.upid.value["TSID"], 16)
        nbin.add_int(self.upid.value["reserved"], 2)
        nbin.add_int(self.upid.value["end_of_day"], 5)
        nbin.add_int(self.upid.value["unique_for"], 9)
        nbin.add_bites(self.upid.value["content_id"].encode("utf-8"))


class Eidr(Upid):
    """
    Eidr Upid
    """

    def decode(self):
        """
        decode Eidr Upid
        """
        pre = self.bitbin.as_hex(16)
        post = []
        # switch to compact binary format
        nibbles = 20
        while nibbles:
            post.append(hex(self.bitbin.as_int(4))[2:])
            nibbles -= 1
        self.upid_value = f"{pre}{''.join(post)}"
        return self.upid_name, self.upid_value

    def encode(self, nbin ):
        """
        encode Eidr Upid
        """
        # switch to compact binary format
        nbin.add_hex(self.upid.value[:6], 16)
        substring = self.upid.value[6:]
        for i in substring:
            hexed = f"0x{i}"
            nbin.add_hex(hexed, 4)


class Isan(Upid):
    """
    Isan Upid
    """

    def decode(self):
        """
        decode Isan Upid
        """
        self.upid_value= self.bitbin.as_hex(self.bit_length)
        return self.upid_name, self.upid_value

    def encode(self, nbin ):
        """
        encode Isan Upid
        """
        nbin.add_hex(self.upid.value, (self.upid_length << 3))


class Mid(Upid):
    """
    Mid Upid
    """

    def decode(self):
        """
        decode Mid Upid
        """
        self.upid_value = []
        ulb = self.bit_length
        while ulb:
            upid_type = self.bitbin.as_int(8)  # 1 byte
            ulb -= 8
            upid_length = self.bitbin.as_int(8)
            ulb -= 8
            upid_type_name, segmentation_upid = upid_map[upid_type][1](
                self.bitbin, upid_type, upid_length
            ).decode()
            mid_upid = {
                "upid_type": upid_type,
                "upid_type_name": upid_type_name,
                "upid_length": upid_length,
                "segmentation_upid": segmentation_upid,
            }
            ulb -= upid_length << 3
            self.upid_value.append(mid_upid)
        return self.upid_name, self.upid_value

    def encode(self, nbin ):
        """
        encode Mid Upid
        """
        for mid_upid in self.upid.value:
            nbin.add_int(mid_upid["upid_type"], 8)
            nbin.add_int(mid_upid["upid_length"], 8)
            the_upid = upid_map[mid_upid["upid_type"]][1](
                None, mid_upid["upid_type"], mid_upid["upid_length"]
            )
            the_upid.encode(nbin, mid_upid["segmentation_upid"])

    def xml(self):
        """
        xml return a upid xml node

        """
        mid_nodes =[]
        for u in self.upid_value:
            u_attrs = { 'upid_type': self.upid_name, # this is for clarity
                    'segmentation_upid_type': self.upid_type,
                    'segmentation_upid_format':'hexbinary',
                    'segmentation_upid_length':self.upid_length,}
            value= u["segmentation_upid"]
            node= Node('SegmentationUpid', attrs=u_attrs, value=value)
            mid_nodes.append(node)
        return mid_nodes


class Mpu(Upid):
    """
    Mpu Upid
    """

    def _decode_adfr(self):
        """
        decode_adfr handles Addressabkle TV MPU Upids
        """
        data = bytes.fromhex(self.upid_value["private_data"][2:])
        self.upid_value["version"] = data[0]
        self.upid_value["channel_identifier"] = hex(int.from_bytes(data[1:3], byteorder="big"))
        self.upid_value["date"] = int.from_bytes(data[3:7], byteorder="big")
        self.upid_value["break_code"] = int.from_bytes(data[7:9], byteorder="big")
        self.upid_value["duration"] = hex(int.from_bytes(data[9:11], byteorder="big"))

    def decode(self):
        """
        decode MPU Upids
        """
        self.upid_value = {
            "format_identifier": self.bitbin.as_charset(32),
            "private_data": self.bitbin.as_hex(self.bit_length - 32),
        }
        if self.upid_value["format_identifier"] == "ADFR":
           self._decode_adfr()
        return self.upid_name, self.upid_value

    def encode(self, nbin ):
        """
        encode MPU Upids
        """
        bit_len = self.bit_length
        fm = bytes(self.upid.value["format_identifier"].encode("utf8"))
        nbin.add_bites(fm)
        bit_len -= 32
        nbin.add_hex(self.upid.value["private_data"], bit_len)


class Umid(Upid):
    """
    Umid Upid
    """

    def decode(self):
        """
        decode Umid Upids
        """
        chunks = []
        ulb = self.bit_length
        while ulb > 32:
            chunks.append(self.bitbin.as_hex(32)[2:])
            ulb -= 32
        self.upid_value= ".".join(chunks)
        return self.upid_name, self.upid_value

    def encode(self, nbin ):
        """
        encode Umid Upid
        """
        chunks = self.upid.value.split(".")
        for chunk in chunks:
            nbin.add_hex(chunk, 32)


upid_map = {
    0x00: ["No UPID", NoUpid],
    0x01: ["Deprecated", Upid],
    0x02: ["Deprecated", Upid],
    0x03: ["AdID", Upid],
    0x04: ["UMID", Umid],
    0x05: ["ISAN", Isan],
    0x06: ["ISAN", Isan],
    0x07: ["TID", Upid],
    0x08: ["AiringID", AirId],
    0x09: ["ADI", Upid],
    0x10: ["UUID", Upid],
    0x11: ["SCR", Upid],
    0x0A: ["EIDR", Eidr],
    0x0B: ["ATSC", Atsc],
    0x0C: ["MPU", Mpu],
    0x0D: ["MID", Mid],
    0x0E: ["ADS Info", Upid],
    0x0F: ["URI", Upid],
    0xFD: ["Unknown", Upid],
}
