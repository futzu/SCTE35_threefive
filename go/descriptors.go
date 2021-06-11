package threefive

import "github.com/futzu/bitter"

// Splice descriptor
type SpDscptr struct {
	DescriptorType uint64
	DescriptorLen  uint64
	// identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
	Identifier      string
	Name            string
	ProviderAvailID uint64
	PreRoll         uint64   `json:",omitempty"`
	DTMFCount       uint64   `json:",omitempty"`
	DTMFChars       []string `json:",omitempty"`
	TAISeconds      uint64   `json:",omitempty"`
	TAINano         uint64   `json:",omitempty"`
	UTCOffset       uint64   `json:",omitempty"`
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
	  Segments_expected          uint64
	  SubSegmentNum              uint64
	  SubSegmentsExpected        uint64
	  **/
}

// MetaData for splice descriptors
func (dscptr *SpDscptr) MetaData(bitn *bitter.Bitn) {
	dscptr.DescriptorType = bitn.AsUInt64(8)
	dscptr.DescriptorLen = bitn.AsUInt64(8)
	dscptr.Identifier = bitn.AsHex(32)
}

// Decode splice descriptor values
func (dscptr *SpDscptr) Decode(bitn *bitter.Bitn) {
	ddt := dscptr.DescriptorType
	if ddt == 0 {
		dscptr.AvailDscptr(bitn)
	}
	if ddt == 1 {
		dscptr.DTMFDscptr(bitn)
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
