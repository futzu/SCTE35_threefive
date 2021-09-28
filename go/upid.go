package threefive

import "github.com/futzu/bitter"
      /**
    upid_map = map[uint8]map[string]Upid{
        0x01: ["Deprecated",&URI{}],
        0x02: ["Deprecated",&URI{}],
        0x03: ["AdID", &URI{}],
       // 0x04: ["UMID", _decode_umid],
     //   0x05: ["ISAN", Isan],
     //   0x06: ["ISAN", Isan],
        0x07: ["TID",&URI{}],
	0x08: ["AiringID", &AirID{}],
        0x09: ["ADI",&URI{}],
   //     0x0A: ["EIDR", _decode_eidr],
    //    0x0B: ["ATSC", _decode_atsc],
    //    0x0C: ["MPU", _decode_mpu],
    //    0x0D: ["MID", _decode_mid],
        0x0E: ["ADS Info", &URI{}],
        0x0F: ["URI", &URI{}],
        0x10: ["UUID", &URI{},
        0xFD: ["Unknown", &URI{}],
    }
    **/
	       /**
    if upid_type not in upid_map.keys():
        upid_type = 0xFD
    return upid_map[upid_type][0], upid_map[upid_type][1](bitbin, upid_length)
**/

type UpidDetails struct {
    Name
}


// Upid is the interface for Segmentation Upida
type Upid interface {
	Decode(bitn *bitter.Bitn, upidtype string, name string, upidlen uint)
}

// AirID Segmentation Upid
type AirID struct {
	UpidType string
	Name     string
	Value    string
}

// Decode for AirId struct
func (upid *AirID) Decode(bitn *bitter.Bitn, upidtype string, name string, upidlen uint) {
	upid.UpidType = upidtype
	upid.Name = name
	upid.Value = bitn.AsHex(upidlen << 3)
}

// Isan Segmentation Upid
type Isan struct {
	UpidType string
	Name     string
	Value    string
}

// Decode for Isan Upid struct
func (upid *Isan) Decode(bitn *bitter.Bitn, upidtype string, name string, upidlen uint) {
	upid.UpidType = upidtype
	upid.Name = name
	upid.Value = bitn.AsAscii(upidlen << 3)
}

// URI Segmentation Upid
type URI struct {
	UpidType string
	Name     string
	Value    string
}

// Decode for URI struct
func (upid *URI) Decode(bitn *bitter.Bitn, upidtype string, name string, upidlen uint) {
	upid.UpidType = upidtype
	upid.Name = name
	upid.Value = bitn.AsAscii(upidlen << 3)
}

// ATSC Segmentation Upid
type ATSC struct {
	UpidType  string
	Name      string
	TSID      uint64
	Reserved  uint8
	EndOfDay  uint8
	UniqueFor uint64
	ContentID string
}

// Decode for ATSC struct
func (upid *ATSC) Decode(bitn *bitter.Bitn, upidtype string, name string, upidlen uint) {
	upid.UpidType = upidtype
	upid.Name = name
	upid.TSID = bitn.AsUInt64(16)
	upid.Reserved = bitn.AsUInt8(2)
	upid.EndOfDay = bitn.AsUInt8(5)
	upid.UniqueFor = bitn.AsUInt64(9)
	upid.ContentID = bitn.AsAscii(((upid_length - 4) << 3))
}

type EIDR struct {
	UpidType  string
	Name      string
	Value    string

}
/**
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
**/
type ISAN struct {
	UpidType  string
	Name      string
	Value    string

}

/**

func (upid *ISAN) Decode(bitn *bitter.Bitn, upidtype string, name string, upidlen uint) {


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


 **/
 
type MPU struct {
UpidType  string
Name      string 
FormatIdentifier string
PrivateData    string   
} 

func (upid *MPU) Decode(bitn *bitter.Bitn, upidtype string, name string, upidlen uint) {
    upid.UpidType = upidtype
	upid.Name = name
    ulb := upidlen << 3
    upid.FormatIdentifier = bitn.AsHex(32)
    upid.PrivateData = bitn.AsAscii(ulb-32)

}

/**
def _decode_umid(bitbin, upid_length):
    chunks = []
    ulb = upid_length << 3
    while ulb:
        chunks.append(bitbin.as_hex(32).split("x", 1)[1])
        ulb -= 32
    return ".".join(chunks)

**/
