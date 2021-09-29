package threefive

import "github.com/futzu/bitter"

/**
def upid_decoder(bitbin, upid_type, upid_length):
    """
    upid_decoder
    decodes segmentation_upids by type,
    from a bitbin instance.

    Used by the SegmentationDescriptor class.
    """

 **/
var upidMap = map[uint8]Upid{
	0x01: &URI{Name: "Deprecated"},
	0x02: &URI{Name: "Deprecated"},
	0x03: &URI{Name: "AdID"},
	// 0x04: ["UMID", _decode_umid],
	0x05: &Isan{Name: "ISAN"},
	0x06: &Isan{Name: "ISAN"},
	0x07: &URI{Name: "TID"},
	0x08: &AirID{Name: "AiringID"},
	0x09: &URI{Name: "ADI"},
	// 0x0A: ["EIDR", _decode_eidr],
	0x0B: &ATSC{Name: "ATSC"},
	0x0C: &MPU{Name: "MPU"},
	//  0x0D: ["MID", _decode_mid],
	0x0E: &URI{Name: "ADS Info"},
	0x0F: &URI{Name: "URI"},
	0x10: &URI{Name: "UUID"},
	0xFD: &URI{Name: "Unknown"},
}

// Upid is the interface for Segmentation Upida
type Upid interface {
	Decode(bitn *bitter.Bitn, upidlen uint8)
}

// AirID Segmentation Upid
type AirID struct {
	Name  string
	Value string
}

// Decode for AirId struct
func (upid *AirID) Decode(bitn *bitter.Bitn, upidlen uint8) {
	upid.Value = bitn.AsHex(uint(upidlen << 3))
}

// Isan Segmentation Upid
type Isan struct {
	Name  string
	Value string
}

// Decode for Isan Upid struct
func (upid *Isan) Decode(bitn *bitter.Bitn, upidlen uint8) {
	upid.Value = bitn.AsAscii(uint(upidlen << 3))
}

// URI Segmentation Upid
type URI struct {
	Name  string
	Value string
}

// Decode for URI struct
func (upid *URI) Decode(bitn *bitter.Bitn, upidlen uint8) {
	upid.Value = bitn.AsAscii(uint(upidlen) << 3)
}

// ATSC Segmentation Upid
type ATSC struct {
	Name      string
	TSID      uint64
	Reserved  uint8
	EndOfDay  uint8
	UniqueFor uint64
	ContentID string
}

// Decode for ATSC struct
func (upid *ATSC) Decode(bitn *bitter.Bitn, upidlen uint8) {
	upid.TSID = bitn.AsUInt64(16)
	upid.Reserved = bitn.AsUInt8(2)
	upid.EndOfDay = bitn.AsUInt8(5)
	upid.UniqueFor = bitn.AsUInt64(9)
	upid.ContentID = bitn.AsAscii(uint((upidlen - 4) << 3))
}

// EIDR Segmentation Upid
type EIDR struct {
	Name  string
	Value string
}

// MPU Segmentation Upid
type MPU struct {
	Name             string
	FormatIdentifier string
	PrivateData      string
}

// Decode interface for MPU
func (upid *MPU) Decode(bitn *bitter.Bitn, upidlen uint8) {
	ulb := uint(upidlen) << 3
	upid.FormatIdentifier = bitn.AsHex(32)
	upid.PrivateData = bitn.AsAscii(ulb - 32)

}
