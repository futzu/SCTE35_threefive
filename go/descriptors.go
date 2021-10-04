package threefive

import "github.com/futzu/bitter"

// DescriptorTags array of valid descriptor tags
var DescriptorTags = []uint8{0, 1, 2, 3, 4}

//DescriptorIsValid checks if tag is in DescriptorTags
func DescriptorIsValid(tag uint8) bool {
	return isIn8(DescriptorTags, tag)
}

// DescriptorDecoder returns a Descriptor by tag
func DescriptorDecoder(tag uint8) Descriptor {
	var sd Descriptor
	switch tag {
	case 0:
		sd = &AvailDscptr{}
	case 1:
		sd = &DTMFDscptr{}
	case 2:
		sd = &SegmentDscptr{}
	case 3:
		sd = &TimeDscptr{}
	case 4:
		sd = &AudioDscptr{}
	}
	return sd
}

// Descriptor is the interface for all Splice Descriptors
type Descriptor interface {
	Decode(bitn *bitter.Bitn, tag uint8, length uint8)
}

// AudioCmpt is a struct for AudioDscptr Components
type AudioCmpt struct {
	ComponentTag  uint8
	ISOCode       uint64
	BitstreamMode uint8
	NumChannels   uint8
	FullSrvcAudio bool
}

// AudioDscptr Audio Splice Descriptor
type AudioDscptr struct {
	Tag    uint8 `json:",omitempty"`
	Length uint8 `json:",omitempty"`
	// identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
	Identifier string
	Name       string
	Components []AudioCmpt `json:",omitempty"`
}

// Decode for the Descriptor interface
func (dscptr *AudioDscptr) Decode(bitn *bitter.Bitn, tag uint8, length uint8) {
	dscptr.Tag = tag
	dscptr.Length = length
	dscptr.Identifier = bitn.AsAscii(32)
	ccount := bitn.AsUInt8(4)
	bitn.Forward(4)
	for ccount > 0 {
		ccount--
		ct := bitn.AsUInt8(8)
		iso := bitn.AsUInt64(24)
		bsm := bitn.AsUInt8(3)
		nc := bitn.AsUInt8(4)
		fsa := bitn.AsBool()
		dscptr.Components = append(dscptr.Components, AudioCmpt{ct, iso, bsm, nc, fsa})
	}
}

// AvailDscptr Avail Splice Descriptor
type AvailDscptr struct {
	Tag    uint8 `json:",omitempty"`
	Length uint8 `json:",omitempty"`
	// identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
	Identifier      string
	Name            string
	ProviderAvailID uint64
}

// Decode for the Descriptor interface
func (dscptr *AvailDscptr) Decode(bitn *bitter.Bitn, tag uint8, length uint8) {
	dscptr.Tag = tag
	dscptr.Length = length
	dscptr.Identifier = bitn.AsAscii(32)
	dscptr.Name = "Avail Descriptor"
	dscptr.ProviderAvailID = bitn.AsUInt64(32)
}

// DTMFDscptr DTMF Splice Descriptor
type DTMFDscptr struct {
	Tag    uint8 `json:",omitempty"`
	Length uint8 `json:",omitempty"`
	// identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
	Identifier string
	Name       string
	PreRoll    uint8
	DTMFCount  uint8
	DTMFChars  uint64 `json:",omitempty"`
}

// Decode for the Descriptor interface
func (dscptr *DTMFDscptr) Decode(bitn *bitter.Bitn, tag uint8, length uint8) {
	dscptr.Tag = tag
	dscptr.Length = length
	dscptr.Identifier = bitn.AsAscii(32)
	dscptr.Name = "DTMF Descriptor"
	dscptr.PreRoll = bitn.AsUInt8(8)
	dscptr.DTMFCount = bitn.AsUInt8(3)
	//bitn.Forward(5)
	dscptr.DTMFChars = bitn.AsUInt64(uint(8 * dscptr.DTMFCount))

}

// TimeDscptr Time Splice DSescriptor
type TimeDscptr struct {
	Tag    uint8 `json:",omitempty"`
	Length uint8 `json:",omitempty"`
	// identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
	Identifier string
	Name       string
	TAISeconds uint64
	TAINano    uint64
	UTCOffset  uint64
}

// Decode for the Descriptor interface
func (dscptr *TimeDscptr) Decode(bitn *bitter.Bitn, tag uint8, length uint8) {
	dscptr.Tag = tag
	dscptr.Length = length
	dscptr.Identifier = bitn.AsAscii(32)
	dscptr.Name = "Time Descriptor"
	dscptr.TAISeconds = bitn.AsUInt64(48)
	dscptr.TAINano = bitn.AsUInt64(32)
	dscptr.UTCOffset = bitn.AsUInt64(16)
}

// SegCmpt Segmentation Descriptor Component
type SegCmpt struct {
	ComponentTag uint8
	PtsOffset    float64
}

// SegmentDscptr Segmentation Descriptor
type SegmentDscptr struct {
	Tag    uint8 `json:",omitempty"`
	Length uint8 `json:",omitempty"`
	// identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
	Identifier                       string
	Name                             string
	SegmentationEventID              string
	SegmentationEventCancelIndicator bool
	ProgramSegmentationFlag          bool
	SegmentationDurationFlag         bool
	DeliveryNotRestrictedFlag        bool
	WebDeliveryAllowedFlag           bool
	NoRegionalBlackoutFlag           bool
	ArchiveAllowedFlag               bool
	DeviceRestrictions               string    `json:",omitempty"`
	Components                       []SegCmpt `json:",omitempty"`
	SegmentationDuration             float64   `json:",omitempty"`
	SegmentationMessage              string
	SegmentationUpidType             uint8
	SegmentationUpidLength           uint8
	SegmentationUpid                 Upid
	SegmentationTypeID               uint8
	SegmentNum                       uint64
	SegmentsExpected                 uint64 `json:",omitempty"`
	SubSegmentNum                    uint64 `json:",omitempty"`
	SubSegmentsExpected              uint64 `json:",omitempty"`
}

// Decode for the Descriptor interface
func (dscptr *SegmentDscptr) Decode(bitn *bitter.Bitn, tag uint8, length uint8) {
	dscptr.Tag = tag
	dscptr.Length = length
	dscptr.Identifier = bitn.AsAscii(32)
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

func (dscptr *SegmentDscptr) decodeSegFlags(bitn *bitter.Bitn) {
	dscptr.ProgramSegmentationFlag = bitn.AsBool()
	dscptr.SegmentationDurationFlag = bitn.AsBool()
	dscptr.DeliveryNotRestrictedFlag = bitn.AsBool()
	if dscptr.DeliveryNotRestrictedFlag == false {
		dscptr.WebDeliveryAllowedFlag = bitn.AsBool()
		dscptr.NoRegionalBlackoutFlag = bitn.AsBool()
		dscptr.ArchiveAllowedFlag = bitn.AsBool()
		dscptr.DeviceRestrictions = table20[bitn.AsUInt8(2)]
		return
	}
	bitn.Forward(5)
}

func (dscptr *SegmentDscptr) decodeSegCmpnts(bitn *bitter.Bitn) {
	ccount := bitn.AsUInt8(8)
	for ccount > 0 { // 6 bytes each
		ccount--
		ct := bitn.AsUInt8(8)
		bitn.Forward(7)
		po := bitn.As90k(33)
		dscptr.Components = append(dscptr.Components, SegCmpt{ct, po})
	}
}

func (dscptr *SegmentDscptr) decodeSegmentation(bitn *bitter.Bitn) {
	if dscptr.SegmentationDurationFlag == true {
		dscptr.SegmentationDuration = bitn.As90k(40)
	}
	dscptr.SegmentationUpidType = bitn.AsUInt8(8)
	dscptr.SegmentationUpidLength = bitn.AsUInt8(8)
	//if UpidIsValid(dscptr.SegmentationUpidType) {
	dscptr.SegmentationUpid = UpidDecoder(dscptr.SegmentationUpidType)
	dscptr.SegmentationUpid.Decode(bitn, dscptr.SegmentationUpidLength)
	//}
	dscptr.SegmentationTypeID = bitn.AsUInt8(8)

	mesg, ok := table22[dscptr.SegmentationTypeID]
	if ok {
		dscptr.SegmentationMessage = mesg

	}
	bitn.Forward(16)

}
