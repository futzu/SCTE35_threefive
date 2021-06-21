package threefive

import "github.com/futzu/bitter"

// SegCmpt Segmentation Descriptor Component
type SegCmpt struct {
	ComponentTag uint8
	PtsOffset    float64
}

// SpDscptr Splice Descriptor
type SpDscptr struct {
	Tag    uint8
	Length uint8
	Name   string
	// identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
	ID string

	ProviderAvailID uint64

	PreRoll                          uint8    `json:",omitempty"`
	DTMFCount                        uint64   `json:",omitempty"`
	DTMFChars                        []string `json:",omitempty"`
	TAISeconds                       uint64   `json:",omitempty"`
	TAINano                          uint64   `json:",omitempty"`
	UTCOffset                        uint64   `json:",omitempty"`
	SegmentationEventID              string   `json:",omitempty"`
	SegmentationEventCancelIndicator bool     `json:",omitempty"`
	ProgramSegmentationFlag          bool     `json:",omitempty"`
	SegmentationDurationFlag         bool     `json:",omitempty"`
	DeliveryNotRestrictedFlag        bool     `json:",omitempty"`
	WebDeliveryAllowedFlag           bool     `json:",omitempty"`
	NoRegionalBlackoutFlag           bool     `json:",omitempty"`
	ArchiveAllowedFlag               bool     `json:",omitempty"`
	//  DeviceRestrictions = table20[bitn.AsUInt64(2)]
	Components               []SegCmpt `json:",omitempty"`
	SegmentationDuration     float64   `json:",omitempty"`
	SegmentationMessage      string    `json:",omitempty"`
	SegmentationUpidType     uint8     `json:",omitempty"`
	SegmentationUpidTypeName string    `json:",omitempty"`
	SegmentationUpidLength   uint8     `json:",omitempty"`
	SegmentationUpid         string    `json:",omitempty"`
	SegmentationTypeID       uint8     `json:",omitempty"`
	SegmentNum               uint64    `json:",omitempty"`
	SegmentsExpected         uint64    `json:",omitempty"`
	SubSegmentNum            uint64    `json:",omitempty"`
	SubSegmentsExpected      uint64    `json:",omitempty"`
	/**

	  DeviceRestrictions

	  **/
}

// MetaData for splice descriptors
func (dscptr *SpDscptr) MetaData(bitn *bitter.Bitn) {
	dscptr.Tag = bitn.AsUInt8(8)
	dscptr.Length = bitn.AsUInt8(8)
	dscptr.ID = bitn.AsHex(32)
}

// Decode splice descriptor values
func (dscptr *SpDscptr) Decode(bitn *bitter.Bitn) {
	ddt := dscptr.Tag
	if ddt == 0 {
		dscptr.AvailDscptr(bitn)
	}
	if ddt == 1 {
		dscptr.DTMFDscptr(bitn)
	}
	if ddt == 2 {
		dscptr.SegmentDscptr(bitn)
	}
	if ddt == 3 {
		dscptr.TimeDscptr(bitn)
	}

}

// AvailDscptr Avail Splice Descriptor
func (dscptr *SpDscptr) AvailDscptr(bitn *bitter.Bitn) {
	dscptr.Name = "Avail Descriptor"
	dscptr.ProviderAvailID = bitn.AsUInt64(32)
}

// DTMFDscptr DTMF Splice Descriptor
func (dscptr *SpDscptr) DTMFDscptr(bitn *bitter.Bitn) {
	dscptr.Name = "DTMF Descriptor"
	dscptr.PreRoll = bitn.AsUInt8(8)
	dscptr.DTMFCount = bitn.AsUInt64(3)
	bitn.Forward(5)
	var dchars [256]string
	dscptr.DTMFChars = dchars[0:dscptr.DTMFCount]
	for i := range dscptr.DTMFChars {
		dscptr.DTMFChars[i] = string(bitn.AsUInt8(8))
	}
}

// TimeDscptr Time Splice DSescriptor
func (dscptr *SpDscptr) TimeDscptr(bitn *bitter.Bitn) {
	dscptr.Name = "Time Descriptor"
	dscptr.TAISeconds = bitn.AsUInt64(48)
	dscptr.TAINano = bitn.AsUInt64(32)
	dscptr.UTCOffset = bitn.AsUInt64(16)
}

// SegmentDscptr Segmentation Descriptor
func (dscptr *SpDscptr) SegmentDscptr(bitn *bitter.Bitn) {
	dscptr.Name = "Segmentation Descriptor"
	dscptr.SegmentationEventID = bitn.AsHex(32)
	dscptr.SegmentationEventCancelIndicator = bitn.AsBool()
	bitn.Forward(7)
	if !dscptr.SegmentationEventCancelIndicator {
		dscptr.decodeSegFlags(bitn)
		if !dscptr.ProgramSegmentationFlag {
			dscptr.decodeSegCmpnts(bitn)
		}
		dscptr.decodeSegmentation(bitn)
	}
}

func (dscptr *SpDscptr) decodeSegFlags(bitn *bitter.Bitn) {
	dscptr.ProgramSegmentationFlag = bitn.AsBool()
	dscptr.SegmentationDurationFlag = bitn.AsBool()
	dscptr.DeliveryNotRestrictedFlag = bitn.AsBool()
	if !dscptr.DeliveryNotRestrictedFlag {
		dscptr.WebDeliveryAllowedFlag = bitn.AsBool()
		dscptr.NoRegionalBlackoutFlag = bitn.AsBool()
		dscptr.ArchiveAllowedFlag = bitn.AsBool()
		// dscptr.DeviceRestrictions = table20[bitn.AsUInt64(2)]
		return
	}
	bitn.Forward(5)
}

func (dscptr *SpDscptr) decodeSegCmpnts(bitn *bitter.Bitn) {
	ccount := bitn.AsUInt8(8)
	for ccount > 0 { // 6 bytes each
		ccount--
		ct := bitn.AsUInt8(8)
		bitn.Forward(7)
		po := bitn.As90k(33)
		dscptr.Components = append(dscptr.Components, SegCmpt{ct, po})
	}
}

func (dscptr *SpDscptr) decodeSegmentation(bitn *bitter.Bitn) {
	if dscptr.SegmentationDurationFlag {
		dscptr.SegmentationDuration = bitn.As90k(40)
	}
	dscptr.SegmentationUpidType = bitn.AsUInt8(8)
	dscptr.SegmentationUpidLength = bitn.AsUInt8(8)
	/**
	        dscptr.SegmentationUpidTypeName, dscptr.SegmentationUpid = UpidDecoder(
	            bitn, dscptr.SegmentationUpidType, dscptr.SegmentationUpidLength
	        )
	**/

	dscptr.SegmentationTypeID = bitn.AsUInt8(8)

	/**
	        if dscptr.SegmentationTypeID in Table22.keys(){
	            dscptr.SegmentationMessage = Table22[dscptr.SegmentationTypeID]
	            dscptr._decode_segments(bitbin)

	        }
	**/
}
