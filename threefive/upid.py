"""
threefive/upid.py

threefve.upid exposes one function,
upid_decoder for use by the
SegmentationDescriptor class.

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
        return upid_map[upid_type][0], upid_map[upid_type][1](bitbin, upid_length)
    return False


def _decode_air_id(bitbin, upid_length):
    return bitbin.as_hex(upid_length << 3)


def _decode_atsc(bitbin, upid_length):
    return {
        "TSID": bitbin.as_int(16),
        "reserved": bitbin.as_int(2),
        "end_of_day": bitbin.as_int(5),
        "unique_for": bitbin.as_int(9),
        "content_id": bitbin.as_ascii(((upid_length - 4) << 3)),
    }


def _decode_eidr(bitbin, upid_length):
    if upid_length < 12:
        raise Exception(f"upid_length is {upid_length} should be 12 bytes")
    pre = bitbin.as_int(16)
    post = []
    bit_count = 80
    while bit_count:
        bit_count -= 16
        post.append(bitbin.as_hex(16)[2:])
    return f"10.{pre}/{'-'.join(post)}"


def _decode_isan(bitbin, upid_length):
    return bitbin.as_hex(upid_length << 3)


def _decode_mid(bitbin, upid_length):
    upids = []
    ulb = upid_length << 3
    while ulb:
        upid_type = bitbin.as_int(8)  # 1 byte
        ulb -= 8
        upid_length = bitbin.as_int(8)
        ulb -= 8
        upid_type_name, segmentation_upid = upid_decoder(bitbin, upid_type, upid_length)
        mid_upid = {
            "upid_type": hex(upid_type),
            "upid_type_name": upid_type_name,
            "upid_length": upid_length,
            "segmentation_upid": segmentation_upid,
        }
        ulb -= upid_length << 3
        upids.append(mid_upid)
    return upids


def _decode_mpu(bitbin, upid_length):
    ulbits = upid_length << 3
    mpu_data = {
        "format_identifier": bitbin.as_hex(32),
        "private_data": bitbin.as_hex(ulbits - 32),
    }
    return mpu_data


def _decode_umid(bitbin, upid_length):
    chunks = []
    ulb = upid_length << 3
    while ulb:
        chunks.append(bitbin.as_hex(32).split("x", 1)[1])
        ulb -= 32
    return ".".join(chunks)


def _decode_uri(bitbin, upid_length):
    if upid_length > 0:
        return bitbin.as_ascii(upid_length << 3)
    return 0
