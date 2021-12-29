package threefive

import "github.com/futzu/bitter"

// AudioCmpt is a struct for AudioDscptr Components
type AudioCmpt struct {
	ComponentTag  uint8
	ISOCode       uint64
	BitstreamMode uint8
	NumChannels   uint8
	FullSrvcAudio bool
}

// SegCmpt Segmentation Descriptor Component
type SegCmpt struct {
	ComponentTag uint8
	PtsOffset    float64
}

type SpliceDescriptor struct {
	Tag                              uint8
	Length                           uint8
	Identifier                       string
	Name                             string
	AudioComponents                  []AudioCmpt `json:",omitempty"`
	ProviderAvailID                  uint64      `json:",omitempty"`
	PreRoll                          uint8       `json:",omitempty"`
	DTMFCount                        uint8       `json:",omitempty"`
	DTMFChars                        uint64      `json:",omitempty"`
	TAISeconds                       uint64      `json:",omitempty"`
	TAINano                          uint64      `json:",omitempty"`
	UTCOffset                        uint64      `json:",omitempty"`
	SegmentationEventID              string      `json:",omitempty"`
	SegmentationEventCancelIndicator bool        `json:",omitempty"`
	ProgramSegmentationFlag          bool        `json:",omitempty"`
	SegmentationDurationFlag         bool        `json:",omitempty"`
	DeliveryNotRestrictedFlag        bool        `json:",omitempty"`
	WebDeliveryAllowedFlag           bool        `json:",omitempty"`
	NoRegionalBlackoutFlag           bool        `json:",omitempty"`
	ArchiveAllowedFlag               bool        `json:",omitempty"`
	DeviceRestrictions               string      `json:",omitempty"`
	Components                       []SegCmpt   `json:",omitempty"`
	SegmentationDuration             float64     `json:",omitempty"`
	SegmentationMessage              string      `json:",omitempty"`
	SegmentationUpidType             uint8       `json:",omitempty"`
	SegmentationUpidLength           uint8       `json:",omitempty"`
	SegmentationUpid                 Upid        `json:",omitempty"`
	SegmentationTypeID               uint8       `json:",omitempty"`
	SegmentNum                       uint64      `json:",omitempty"`
	SegmentsExpected                 uint64      `json:",omitempty"`
	SubSegmentNum                    uint64      `json:",omitempty"`
	SubSegmentsExpected              uint64      `json:",omitempty"`
}

// DescriptorDecoder returns a Descriptor by tag
func (dscptr *SpliceDescriptor) Decoder(bitn *bitter.Bitn, tag uint8, length uint8) {
	switch tag {
	case 0:
		dscptr.Tag = 0
		dscptr.Avail(bitn, tag, length)
	case 1:
		dscptr.Tag = 1
		dscptr.DTMF(bitn, tag, length)
	case 2:
		dscptr.Tag = 2
		dscptr.Segmentation(bitn, tag, length)
	case 3:
		dscptr.Tag = 3
		dscptr.Time(bitn, tag, length)
	case 4:
		dscptr.Tag = 4
		dscptr.Audio(bitn, tag, length)
	}
}

func (dscptr *SpliceDescriptor) Audio(bitn *bitter.Bitn, tag uint8, length uint8) {
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
		dscptr.AudioComponents = append(dscptr.AudioComponents, AudioCmpt{ct, iso, bsm, nc, fsa})
	}
}

// Decode for the Avail
func (dscptr *SpliceDescriptor) Avail(bitn *bitter.Bitn, tag uint8, length uint8) {
	dscptr.Tag = tag
	dscptr.Length = length
	dscptr.Identifier = bitn.AsAscii(32)
	dscptr.Name = "Avail Descriptor"
	dscptr.ProviderAvailID = bitn.AsUInt64(32)
}

//  DTMF Splice Descriptor
func (dscptr *SpliceDescriptor) DTMF(bitn *bitter.Bitn, tag uint8, length uint8) {
	dscptr.Tag = tag
	dscptr.Length = length
	dscptr.Identifier = bitn.AsAscii(32)
	dscptr.Name = "DTMF Descriptor"
	dscptr.PreRoll = bitn.AsUInt8(8)
	dscptr.DTMFCount = bitn.AsUInt8(3)
	//bitn.Forward(5)
	dscptr.DTMFChars = bitn.AsUInt64(uint(8 * dscptr.DTMFCount))

}

// Decode for the Time Descriptor
func (dscptr *SpliceDescriptor) Time(bitn *bitter.Bitn, tag uint8, length uint8) {
	dscptr.Tag = tag
	dscptr.Length = length
	dscptr.Identifier = bitn.AsAscii(32)
	dscptr.Name = "Time Descriptor"
	dscptr.TAISeconds = bitn.AsUInt64(48)
	dscptr.TAINano = bitn.AsUInt64(32)
	dscptr.UTCOffset = bitn.AsUInt64(16)
}

// Decode for the Segmentation Descriptor
func (dscptr *SpliceDescriptor) Segmentation(bitn *bitter.Bitn, tag uint8, length uint8) {
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

func (dscptr *SpliceDescriptor) decodeSegFlags(bitn *bitter.Bitn) {
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

func (dscptr *SpliceDescriptor) decodeSegCmpnts(bitn *bitter.Bitn) {
	ccount := bitn.AsUInt8(8)
	for ccount > 0 { // 6 bytes each
		ccount--
		ct := bitn.AsUInt8(8)
		bitn.Forward(7)
		po := bitn.As90k(33)
		dscptr.Components = append(dscptr.Components, SegCmpt{ct, po})
	}
}

func (dscptr *SpliceDescriptor) decodeSegmentation(bitn *bitter.Bitn) {
	if dscptr.SegmentationDurationFlag == true {
		dscptr.SegmentationDuration = bitn.As90k(40)
	}
	dscptr.SegmentationUpidType = bitn.AsUInt8(8)
	dscptr.SegmentationUpidLength = bitn.AsUInt8(8)
	dscptr.SegmentationUpid = UpidDecoder(dscptr.SegmentationUpidType)
	dscptr.SegmentationUpid.Decode(bitn, dscptr.SegmentationUpidLength)
	dscptr.SegmentationTypeID = bitn.AsUInt8(8)

	mesg, ok := table22[dscptr.SegmentationTypeID]
	if ok {
		dscptr.SegmentationMessage = mesg
	}
	bitn.Forward(16)
}
