package cuei

import (
	"fmt"
)

// Upid is the Struct for Segmentation Upida
type Upid struct {
	Name             string `json:",omitempty"`
	UpidType         uint8  `json:",omitempty"`
	Value            string `json:",omitempty"`
	TSID             uint16 `json:",omitempty"`
	Reserved         uint8  `json:",omitempty"`
	EndOfDay         uint8  `json:",omitempty"`
	UniqueFor        uint16 `json:",omitempty"`
	ContentID        string `json:",omitempty"`
	Upids            []Upid `json:",omitempty"`
	FormatIdentifier string `json:",omitempty"`
	PrivateData      string `json:",omitempty"`
}

// UpidDecoder calls a method based on upidType
func (upid *Upid) Decoder(gob *Gob, upidType uint8, upidlen uint8) {

	upid.UpidType = upidType

	switch upidType {
	case 0x01, 0x02:
		upid.Name = "Deprecated"
		upid.URI(gob, upidlen)
	case 0x03:
		upid.Name = "AdID"
		upid.URI(gob, upidlen)
	case 0x05, 0x06:
		upid.Name = "ISAN"
		upid.ISAN(gob, upidlen)
	case 0x07:
		upid.Name = "TID"
		upid.URI(gob, upidlen)
	case 0x08:
		upid.Name = "AiringID"
		upid.AirID(gob, upidlen)
	case 0x09:
		upid.Name = "ADI"
		upid.URI(gob, upidlen)
	case 0x0a:
		upid.Name = "EIDR"
		upid.EIDR(gob, upidlen)
	case 0x0b:
		upid.Name = "ATSC"
		upid.ATSC(gob, upidlen)
	case 0x0c:
		upid.Name = "MPU"
		upid.MPU(gob, upidlen)
	case 0x0d:
		upid.Name = "MID"
		upid.MID(gob, upidlen)
	case 0x0e:
		upid.Name = "ADS Info"
		upid.URI(gob, upidlen)
	case 0x0f:
		upid.Name = "URI"
		upid.URI(gob, upidlen)
	case 0x10:
		upid.Name = "UUID"
		upid.URI(gob, upidlen)
	default:
		upid.Name = "UPID"
		upid.URI(gob, upidlen)
	}
}

// Decode for AirId
func (upid *Upid) AirID(gob *Gob, upidlen uint8) {
	upid.Value = gob.Hex(uint(upidlen << 3))
}

// Decode for Isan Upid
func (upid *Upid) ISAN(gob *Gob, upidlen uint8) {
	upid.Value = gob.Ascii(uint(upidlen << 3))
}

// Decode for URI Upid
func (upid *Upid) URI(gob *Gob, upidlen uint8) {
	upid.Value = gob.Ascii(uint(upidlen) << 3)
}

// Decode for ATSC Upid
func (upid *Upid) ATSC(gob *Gob, upidlen uint8) {
	upid.TSID = gob.UInt16(16)
	upid.Reserved = gob.UInt8(2)
	upid.EndOfDay = gob.UInt8(5)
	upid.UniqueFor = gob.UInt16(9)
	upid.ContentID = gob.Ascii(uint((upidlen - 4) << 3))
}

// Decode for EIDR Upid
func (upid *Upid) EIDR(gob *Gob, upidlen uint8) {
	if upidlen == 12 {
		head := gob.UInt64(16)
		tail := gob.Hex(80)
		upid.Value = fmt.Sprintf("10%v/%v", head, tail)
	}
}

// Decode for MPU Upid
func (upid *Upid) MPU(gob *Gob, upidlen uint8) {
	ulb := uint(upidlen) << 3
	upid.FormatIdentifier = gob.Hex(32)
	upid.PrivateData = gob.Ascii(ulb - 32)
}

// Decode for MID Upid
func (upid *Upid) MID(gob *Gob, upidlen uint8) {
	var i uint8
	i = 0
	for i < upidlen {
		utype := gob.UInt8(8)
		i++
		ulen := gob.UInt8(8)
		i++
		i += ulen
		var mupid Upid
		mupid.Decoder(gob, utype, ulen)
		upid.Upids = append(upid.Upids, mupid)
	}
}
