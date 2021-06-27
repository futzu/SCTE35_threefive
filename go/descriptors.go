package threefive

import "github.com/futzu/bitter"

// Descriptor is the interface for all Splice Descriptors
type Descriptor interface {
	MetaData(t uint8, l uint8, i string)
	Decode(bitn *bitter.Bitn)
}

/**
// SegCmpt Segmentation Descriptor Component
type SegCmpt struct {
	ComponentTag uint8
	PtsOffset    float64
}

// SpDscptr Splice Descriptor


	ProviderAvailID uint64 `json:",omitempty"`


	SegmentationEventID              string    `json:",omitempty"`
	SegmentationEventCancelIndicator bool      `json:",omitempty"`
	ProgramSegmentationFlag          bool      `json:",omitempty"`
	SegmentationDurationFlag         bool      `json:",omitempty"`
	DeliveryNotRestrictedFlag        bool      `json:",omitempty"`
	WebDeliveryAllowedFlag           bool      `json:",omitempty"`
	NoRegionalBlackoutFlag           bool      `json:",omitempty"`
	ArchiveAllowedFlag               bool      `json:",omitempty"`
	DeviceRestrictions               string    `json:",omitempty"`
	Components                       []SegCmpt `json:",omitempty"`
	SegmentationDuration             float64   `json:",omitempty"`
	SegmentationMessage              string    `json:",omitempty"`
	SegmentationUpidType             uint8     `json:",omitempty"`
	SegmentationUpidTypeName         string    `json:",omitempty"`
	SegmentationUpidLength           uint8     `json:",omitempty"`
	SegmentationUpid                 string    `json:",omitempty"`
	SegmentationTypeID               uint8     `json:",omitempty"`
	SegmentNum                       uint64    `json:",omitempty"`
	SegmentsExpected                 uint64    `json:",omitempty"`
	SubSegmentNum                    uint64    `json:",omitempty"`
	SubSegmentsExpected              uint64    `json:",omitempty"`


	  DeviceRestrictions

	  **/

// SpliceDscptr is embedded in all Splice Descriptor structs
type SpliceDscptr struct {
	Tag    uint8 `json:",omitempty"`
	Length uint8 `json:",omitempty"`
	// identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
	Identifier string `json:",omitempty"`
}

// MetaData pass in Tag, Length and ID for Splice Descriptors
func (dscptr *SpliceDscptr) MetaData(t uint8, l uint8, i string) {
	dscptr.Tag = t
	dscptr.Length = l
	dscptr.Identifier = i
}

// AvailDscptr Avail Splice Descriptor
type AvailDscptr struct {
	SpliceDscptr
	Name            string
	ProviderAvailID uint64
}

// Decode for the Descriptor interface
func (dscptr *AvailDscptr) Decode(bitn *bitter.Bitn) {
	dscptr.Name = "Avail Descriptor"
	dscptr.ProviderAvailID = bitn.AsUInt64(32)
}

// DTMFDscptr DTMF Splice Descriptor
type DTMFDscptr struct {
	SpliceDscptr
	Name      string
	PreRoll   uint8    `json:",omitempty"`
	DTMFCount uint64   `json:",omitempty"`
	DTMFChars []string `json:",omitempty"`
}

// Decode for the Descriptor interface
func (dscptr *DTMFDscptr) Decode(bitn *bitter.Bitn) {
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
type TimeDscptr struct {
	SpliceDscptr
	Name       string
	TAISeconds uint64 `json:",omitempty"`
	TAINano    uint64 `json:",omitempty"`
	UTCOffset  uint64 `json:",omitempty"`
}

// Decode for the Descriptor interface
func (dscptr *TimeDscptr) Decode(bitn *bitter.Bitn) {
	dscptr.Name = "Time Descriptor"
	dscptr.TAISeconds = bitn.AsUInt64(48)
	dscptr.TAINano = bitn.AsUInt64(32)
	dscptr.UTCOffset = bitn.AsUInt64(16)
}

/**
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
		dscptr.DeviceRestrictions = table20[bitn.AsUInt8(2)]
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


	dscptr.SegmentationTypeID = bitn.AsUInt8(8)

	mesg, ok := table22[dscptr.SegmentationTypeID]
	if ok {
		dscptr.SegmentationMessage = mesg
		// dscptr._decode_segments(bitbin)

	}

}
**/
