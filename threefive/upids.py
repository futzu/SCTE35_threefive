"""
threefive/upids.py

threefve.upids

"""
charset = "ascii"
"""
set charset to None to return raw bytes
"""
charset = "ascii"

class UpidDecoder:
    """
    UpidDecoder for use by the
    SegmentationDescriptor class.
    """

    def __init__(self, bitbin, upid_type, upid_length):
        self.bitbin = bitbin
        self.upid_type = upid_type
        self.upid_length = upid_length
        self.bit_length = upid_length << 3

    def _decode_air_id(self):
        return self.bitbin.as_hex(self.bit_length)

    def _decode_atsc(self):
        cont_size = self.bit_length - 32
        return {
            "TSID": self.bitbin.as_int(16),
            "reserved": self.bitbin.as_int(2),
            "end_of_day": self.bitbin.as_int(5),
            "unique_for": self.bitbin.as_int(9),
            "content_id": self.bitbin.as_charset(cont_size,charset)
        }

    def _decode_eidr(self):
        if self.upid_length != 12:
            return f"upid_length is {self.upid_length} should be 12 bytes."
        pre = self.bitbin.as_int(16)
        post = []
        bit_count = 80
        while bit_count:
            bit_count -= 16
            post.append(self.bitbin.as_hex(16)[2:])
        return f"10.{pre}/{'-'.join(post)}"

    def _decode_isan(self):
        return self.bitbin.as_hex(self.bit_length)

    def _decode_mid(self):
        upids = []
        ulb = self.bit_length
        while ulb:
            upid_type = self.bitbin.as_int(8)  # 1 byte
            ulb -= 8
            upid_length = self.bitbin.as_int(8)
            ulb -= 8
            upid_type_name, segmentation_upid = UpidDecoder(
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
        return upids

    def _decode_mpu(self):
        mpu_data = {
            "format_identifier": self.bitbin.as_int(32),
            "private_data": self.bitbin.as_hex(self.bit_length - 32),
        }
        return mpu_data

    def _decode_umid(self):
        chunks = []
        ulb = self.bit_length
        while ulb > 32:
            chunks.append(self.bitbin.as_hex(32)[2:])
            ulb -= 32
        return ".".join(chunks)

    def _decode_uri(self):
        return self.bitbin.as_charset(self.bit_length, charset)

    def _decode_no(self):
        return None

    def decode(self):
        """
        decode returns a upid determined by
        self.upid_type and upid_map below.
        """
        upid_map = {
            0x00: ["No UPID", self._decode_no],
            0x01: ["Deprecated", self._decode_uri],
            0x02: ["Deprecated", self._decode_uri],
            0x03: ["AdID", self._decode_uri],
            0x04: ["UMID", self._decode_umid],
            0x05: ["ISAN", self._decode_isan],
            0x06: ["ISAN", self._decode_isan],
            0x07: ["TID", self._decode_uri],
            0x08: ["AiringID", self._decode_air_id],
            0x09: ["ADI", self._decode_uri],
            0x10: ["UUID", self._decode_uri],
            0x11: ["SCR", self._decode_uri],
            0x0A: ["EIDR", self._decode_eidr],
            0x0B: ["ATSC", self._decode_atsc],
            0x0C: ["MPU", self._decode_mpu],
            0x0D: ["MID", self._decode_mid],
            0x0E: ["ADS Info", self._decode_uri],
            0x0F: ["URI", self._decode_uri],
            0xFD: ["Unknown", self._decode_uri],
        }
        if self.upid_type not in upid_map:
            self.upid_type = 0xFD
        if not self.upid_length:
            self.upid_type = 0x00
        upid_name = upid_map[self.upid_type][0]
        upid_value = upid_map[self.upid_type][1]()
        return upid_name, upid_value


def upid_encoder(nbin, upid_type, upid_length, seg_upid):
    """
    upid_encoder
    encodes segmentation_upid values to bites
    added to the nbin instance.

    Used by the SegmentationDescriptor class.
    """
    upid_map = {
        0x00: ["No UPID", _encode_no],
        0x01: ["Deprecated", _encode_uri],
        0x02: ["Deprecated", _encode_uri],
        0x03: ["AdID", _encode_uri],
        0x04: ["UMID", _encode_umid],
        0x07: ["TID", _encode_uri],
        0x0B: ["ATSC", _encode_atsc],
        0x09: ["ADI", _encode_uri],
        0x10: ["UUID", _encode_uri],
        0x11: ["SCR", _encode_uri],
        0x0A: ["EIDR", _encode_eidr],
        0x0C: ["MPU", _encode_mpu],
        0x0D: ["MID", _encode_mid],
        0x0E: ["ADS Info", _encode_uri],
        0x0F: ["URI", _encode_uri],
    }
    if upid_type in upid_map:
        upid_map[upid_type][1](nbin, seg_upid)

    upid_map_too = {
        0x05: ["ISAN", _encode_isan],
        0x06: ["ISAN", _encode_isan],
        0x08: ["AiringID", _encode_air_id],
    }
    if upid_type in upid_map_too:
        upid_map_too[upid_type][1](nbin, seg_upid, upid_length)


def _encode_air_id(nbin, seg_upid, upid_length):
    nbin.add_hex(seg_upid, (upid_length << 3))


def _encode_atsc(nbin, seg_upid):
    nbin.add_int(seg_upid["TSID"], 16)
    nbin.add_int(seg_upid["reserved"], 2)
    nbin.add_int(seg_upid["end_of_day"], 5)
    nbin.add_int(seg_upid["unique_for"], 9)
    nbin.add_bites(seg_upid["content_id"].encode("utf-8"))


def _encode_eidr(nbin, seg_upid):
    pre, post = seg_upid[3:].split("/", 1)
    nbin.add_int(int(pre), 16)
    nbin.add_hex(post.replace("-", ""), 80)


def _encode_isan(nbin, seg_upid, upid_length):
    nbin.add_hex(seg_upid, (upid_length << 3))


def _encode_mid(nbin, seg_upid):
    for mid_upid in seg_upid:
        nbin.add_int(mid_upid["upid_type"], 8)
        nbin.add_int(mid_upid["upid_length"], 8)
        upid_encoder(
            nbin,
            mid_upid["upid_type"],
            mid_upid["upid_length"],
            mid_upid["segmentation_upid"],
        )


def _encode_mpu(nbin, seg_upid):
    nbin.add_int(seg_upid["format_identifier"], 32)
    nbin.add_hex(seg_upid["private_data"])


def _encode_no(nbin, seg_upid):
    nbin.forward(0)


def _encode_umid(nbin, seg_upid):
    chunks = seg_upid.split(".")
    for chunk in chunks:
        nbin.add_hex(chunk, 32)


def _encode_uri(nbin, seg_upid):
    if len(seg_upid) > 0:
        seg_upid = seg_upid.encode()
        nbin.add_bites(seg_upid)
