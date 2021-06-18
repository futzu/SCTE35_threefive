package threefive

import "github.com/futzu/bitter"

// Splice descriptor
type SpDscptr struct {
	Tag    uint64
	Length uint64
	Name   string
	// identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
	ID string

	ProviderAvailID uint64

	PreRoll                          uint64   `json:",omitempty"`
	DTMFCount                        uint64   `json:",omitempty"`
	DTMFChars                        []string `json:",omitempty"`
	TAISeconds                       uint64   `json:",omitempty"`
	TAINano                          uint64   `json:",omitempty"`
	UTCOffset                        uint64   `json:",omitempty"`
	SegmentationEventID              uint64   `json:",omitempty"`
	SegmentationEventCancelIndicator bool     `json:",omitempty"`
	ProgramSegmentationFlag          bool     `json:",omitempty"`
	SegmentationDurationFlag         bool     `json:",omitempty"`
	DeliveryNotRestrictedFlag        bool     `json:",omitempty"`
	WebDeliveryAllowedFlag           bool     `json:",omitempty"`
	NoRegionalBlackoutFlag           bool     `json:",omitempty"`
	ArchiveAllowedFlag               bool     `json:",omitempty"`
	//  DeviceRestrictions = table20[bitn.AsUInt64(2)]
	/**
	  SegmentationEventId
	  segmentation_event_cancel_indicator
	  components
	  ProgramSegmentationFlag     bool
	  SegmentationDurationFlag    bool
	  DeliveryNotRestrictedFlag   bool
	  WebDeliveryAllowedFlag      bool
	  NoRegionalBlackoutFlag      bool
	  ArchiveAllowedFlag          bool
	  DeviceRestrictions
	  SegmentationDuration
	  SegmentationMessage
	  SegmentationUpidType
	  SegmentationUpidTypeName   string
	  SegmentationUpidLength     uint64
	  SegmentationUpid
	  SegmentationTypeId
	  SegmentNum                 uint64
	  SegmentsExpected          uint64
	  SubSegmentNum              uint64
	  SubSegmentsExpected        uint64
	  **/
}

// MetaData for splice descriptors
func (dscptr *SpDscptr) MetaData(bitn *bitter.Bitn) {
	dscptr.Tag = bitn.AsUInt64(8)
	dscptr.Length = bitn.AsUInt64(8)
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
	dscptr.PreRoll = bitn.AsUInt64(8)
	dscptr.DTMFCount = bitn.AsUInt64(3)
	bitn.Forward(5)
	var dchars [256]string
	dscptr.DTMFChars = dchars[0:dscptr.DTMFCount]
	for i := range dscptr.DTMFChars {
		dscptr.DTMFChars[i] = string(bitn.AsUInt64(8))
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
	dscptr.SegmentationEventID = bitn.AsUInt64(32)
	dscptr.SegmentationEventCancelIndicator = bitn.AsBool()
	bitn.Forward(7)
	if !(dscptr.SegmentationEventCancelIndicator) {
		dscptr.DecodeSegFlags(bitn)
		// if !(dscptr.ProgramSegmentationFlag {
		//       dscptr.DecodeSegCmpnts(bitn)
	}
	//  dscptr.DecodeSeg(bitn)
}

func (dscptr *SpDscptr) DecodeSegFlags(bitn *bitter.Bitn) {
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

//func (dscptr *SpDscptr) DecodeSegCmpnts((bitn *bitter.Bitn) {
//    ccount = bitn.AsUint64(8)

//}
