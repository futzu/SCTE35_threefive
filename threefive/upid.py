"""
threefive/upid.py

threefve.upid exposes two functions,
upid_decoder and upid_encoder for
use by the SegmentationDescriptor class.

"""


def upid_decoder(bitbin, upid_type, upid_length):
    """
    upid_decoder
    decodes segmentation_upids by type,
    from a bitbin instance.

    Used by the SegmentationDescriptor class.
    """
    upid_map = {
        0x02: ["Deprecated", _decode_uri],
        0x03: ["AdID", _decode_uri],
        0x04: ["UMID", _decode_umid],
        0x05: ["ISAN", _decode_isan],
        0x06: ["ISAN", _decode_isan],
        0x07: ["TID", _decode_uri],
        0x08: ["AiringID", _decode_air_id],
        0x09: ["ADI", _decode_uri],
        0x0A: ["EIDR", _decode_eidr],
        0x0B: ["ATSC", _decode_atsc],
        0x0C: ["MPU", _decode_mpu],
        0x0D: ["MID", _decode_mid],
        0x0E: ["ADS Info", _decode_uri],
        0x0F: ["URI", _decode_uri],
        0x10: ["UUID", _decode_uri],
    }
    if upid_type in upid_map.keys():
        upid_id = upid_map[upid_type][1](bitbin, upid_length)
        return upid_id


def upid_encoder(nbin, upid_type, upid_length, seg_upid):
    """
    upid_encoder
    encodes segmentation_upid values to bites
    added to the nbin instance.

    Used by the SegmentationDescriptor class.
    """
    upid_map = {
        0x02: ["Deprecated", _encode_uri],
        0x03: ["AdID", _encode_uri],
        0x04: ["UMID", _encode_umid],
        0x05: ["ISAN", _encode_isan],
        0x06: ["ISAN", _encode_isan],
        0x07: ["TID", _encode_uri],
        0x08: ["AiringID", _encode_air_id],
        0x09: ["ADI", _encode_uri],
        0x0A: ["EIDR", _encode_eidr],
        0x0B: ["ATSC", _encode_atsc],
        0x0C: ["MPU", _encode_mpu],
        0x0D: ["MID", _encode_mid],
        0x0E: ["ADS Info", _encode_uri],
        0x0F: ["URI", _encode_uri],
        0x10: ["UUID", _encode_uri],
    }
    if upid_type in upid_map.keys():
        upid_map[upid_type][1](nbin, seg_upid, upid_length)


def _decode_air_id(bitbin, upid_length):
    return bitbin.ashex(upid_length << 3)


def _encode_air_id(nbin, seg_upid, upid_length):
    nbin.add_hex(seg_upid, (upid_length << 3))


def _decode_atsc(bitbin, upid_length):
    return {
        "TSID": bitbin.asint(16),
        "reserved": bitbin.asint(2),
        "end_of_day": bitbin.asint(5),
        "unique_for": bitbin.asint(9),
        "content_id": bitbin.asdecodedhex((upid_length - 4) << 3),
    }


def _encode_atsc(nbin, seg_upid, upid_length):
    ulbits = upid_length << 3
    nbin.add_int(seg_upid["TSID"], 16)
    nbin.add_int(seg_upid["reserved"], 2)
    nbin.add_int(seg_upid["end_of_day"], 5)
    nbin.add_int(seg_upid["unique_for"], 9)
    nbin.add_bites(seg_upid["content_id"].encode("utf-8"), (ulbits - 32))


def _decode_eidr(bitbin, upid_length):
    pre = bitbin.asint(16)
    post = []
    bit_count = 80
    while bit_count:
        bit_count -= 16
        post.append(bitbin.ashex(16)[2:])
    return f"10.{pre}/{'-'.join(post)}"


def _encode_eidr(nbin, seg_upid, upid_length):
    pre, post = seg_upid[3:].split("/", 1)
    nbin.add_int(int(pre), 16)
    nbin.add_hex(post.replace("-", ""), 80)


def _decode_isan(bitbin, upid_length):
    return bitbin.ashex(upid_length << 3)


def _encode_isan(nbin, seg_upid, upid_length):
    nbin.add_hex(seg_upid, (upid_length << 3))


def _decode_mid(bitbin, upid_length):
    upids = []
    ulb = upid_length << 3
    while ulb:
        upid_type = bitbin.asint(8)  # 1 byte
        ulb -= 8
        upid_length = bitbin.asint(8)
        ulb -= 8
        segmentation_upid = upid_decoder(bitbin, upid_type, upid_length)
        mid_upid = {
            "upid_type": upid_type,
            "upid_length": upid_length,
            "segmentation_upid": segmentation_upid,
        }
        ulb -= upid_length << 3
        upids.append(mid_upid)
    return upids


def _encode_mid(nbin, seg_upid, upid_length):
    for mid_upid in seg_upid:
        nbin.add_int(mid_upid["upid_type"], 8)
        nbin.add_int(mid_upid["upid_length"], 8)
        upid_encoder(
            nbin,
            mid_upid["upid_type"],
            mid_upid["upid_length"],
            mid_upid["segmentation_upid"],
        )


def _decode_mpu(bitbin, upid_length):
    ulbits = upid_length << 3
    mpu_data = {
        "format_identifier": bitbin.ashex(32),
        "private_data": bitbin.ashex(ulbits - 32),
    }
    return mpu_data


def _encode_mpu(nbin, seg_upid, upid_length):
    ulbits = upid_length << 3
    nbin.add_hex(seg_upid["format_identifier"], 32)
    nbin.add_hex(seg_upid["private_data"], (ulbits - 32))


def _decode_umid(bitbin, upid_length):
    chunks = []
    ulb = upid_length << 3
    while ulb:
        chunks.append(bitbin.ashex(32).split("x", 1)[1])
        ulb -= 32
    return ".".join(chunks)


def _encode_umid(nbin, seg_upid, upid_length):
    chunks = seg_upid.split(".")
    for chunk in chunks:
        nbin.add_hex(chunk, 32)


def _decode_uri(bitbin, upid_length):
    return bitbin.asdecodedhex(upid_length << 3)


def _encode_uri(nbin, seg_upid, upid_length):
    seg_upid = seg_upid.encode("utf-8")
    nbin.add_bites(seg_upid, (upid_length << 3))
