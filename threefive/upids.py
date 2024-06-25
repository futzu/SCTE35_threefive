"""
threefive/upids.py

threefve.upids

classy Upids

cyclomatic complexity 1.689


"""

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

    def decode(self):
        """
        decode Upid
        """
        return self.upid_name, self.bitbin.as_charset(self.bit_length, charset)

    def encode(self, nbin, seg_upid):
        """
        encode Upid
        """
        if seg_upid:
            seg_upid = seg_upid.encode("utf8")
            nbin.add_bites(seg_upid)


class NoUpid(Upid):
    """
    NoUpid class
    """

    def decode(self):
        """
        decode for no upid
        """
        return self.upid_name, None

    def encode(self, nbin, seg_upid):
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
        return self.upid_name, self.bitbin.as_hex(self.bit_length)

    def encode(self, nbin, seg_upid):
        """
        encode AirId
        """
        nbin.add_hex(seg_upid, (self.upid_length << 3))


class Atsc(Upid):
    """
    ATSC Upid
    """

    def decode(self):
        """
        decode Atsc Upid
        """
        cont_size = self.bit_length - 32
        return self.upid_name, {
            "TSID": self.bitbin.as_int(16),
            "reserved": self.bitbin.as_int(2),
            "end_of_day": self.bitbin.as_int(5),
            "unique_for": self.bitbin.as_int(9),
            "content_id": self.bitbin.as_charset(cont_size, charset),
        }

    def encode(self, nbin, seg_upid):
        """
        encode Atsc
        """
        nbin.add_int(seg_upid["TSID"], 16)
        nbin.add_int(seg_upid["reserved"], 2)
        nbin.add_int(seg_upid["end_of_day"], 5)
        nbin.add_int(seg_upid["unique_for"], 9)
        nbin.add_bites(seg_upid["content_id"].encode("utf-8"))


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
        return self.upid_name, f"{pre}{''.join(post)}"

    def encode(self, nbin, seg_upid):
        """
        encode Eidr Upid
        """
        # switch to compact binary format
        nbin.add_hex(seg_upid[:6], 16)
        substring = seg_upid[6:]
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
        return self.upid_name, self.bitbin.as_hex(self.bit_length)

    def encode(self, nbin, seg_upid):
        """
        encode Isan Upid
        """
        nbin.add_hex(seg_upid, (self.upid_length << 3))


class Mid(Upid):
    """
    Mid Upid
    """

    def decode(self):
        """
        decode Mid Upid
        """
        upids = []
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
            upids.append(mid_upid)
        return self.upid_name, upids

    def encode(self, nbin, seg_upid):
        """
        encode Mid Upid
        """
        for mid_upid in seg_upid:
            nbin.add_int(mid_upid["upid_type"], 8)
            nbin.add_int(mid_upid["upid_length"], 8)
            the_upid = upid_map[mid_upid["upid_type"]][1](
                None, mid_upid["upid_type"], mid_upid["upid_length"]
            )
            the_upid.encode(nbin, mid_upid["segmentation_upid"])


class Mpu(Upid):
    """
    Mpu Upid
    """

    def _decode_adfr(self, mpu_data):
        """
        decode_adfr handles Addressabkle TV MPU Upids
        """
        data = bytes.fromhex(mpu_data["private_data"][2:])
        mpu_data["version"] = data[0]
        mpu_data["channel_identifier"] = hex(int.from_bytes(data[1:3], byteorder="big"))
        mpu_data["date"] = int.from_bytes(data[3:7], byteorder="big")
        mpu_data["break_code"] = int.from_bytes(data[7:9], byteorder="big")
        mpu_data["duration"] = hex(int.from_bytes(data[9:11], byteorder="big"))
        return mpu_data

    def decode(self):
        """
        decode MPU Upids
        """
        mpu_data = {
            "format_identifier": self.bitbin.as_charset(32),
            "private_data": self.bitbin.as_hex(self.bit_length - 32),
        }
        if mpu_data["format_identifier"] == "ADFR":
            mpu_data = self._decode_adfr(mpu_data)
        return self.upid_name, mpu_data

    def encode(self, nbin, seg_upid):
        """
        encode MPU Upids
        """
        bit_len = self.bit_length
        fm = bytes(seg_upid["format_identifier"].encode("utf8"))
        nbin.add_bites(fm)
        bit_len -= 32
        nbin.add_hex(seg_upid["private_data"], bit_len)


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
        return self.upid_name, ".".join(chunks)

    def encode(self, nbin, seg_upid):
        """
        encode Umid Upid
        """
        chunks = seg_upid.split(".")
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
