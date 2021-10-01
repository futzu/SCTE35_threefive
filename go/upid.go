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

func UpidDecoder(upidType uint8) Upid {

	var u Upid
	switch upidType {
	case 0x01, 0x02:
		u = &URI{Name: "Deprecated"}
	case 0x03:
		u = &URI{Name: "AdID"}
	case 0x05, 0x06:
		u = &Isan{Name: "ISAN"}
	case 0x07:
		u = &URI{Name: "TID"}
	case 0x08:
		u = &AirID{Name: "AiringID"}
	case 0x09:
		u = &URI{Name: "ADI"}
	case 0x0b:
		u = &ATSC{Name: "ATSC"}
	case 0x0c:
		u = &MPU{Name: "MPU"}
	case 0x0e:
		u = &URI{Name: "ADS Info"}
	case 0x0f:
		u = &URI{Name: "URI"}
	case 0x10:
		u = &URI{Name: "UUID"}
	}
	return u
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
