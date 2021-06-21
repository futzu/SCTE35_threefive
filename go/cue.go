package threefive

import (
	"fmt"
	"github.com/futzu/bitter"
)

// Cue a SCTE35 cue.
type Cue struct {
	InfoSection  SpInfo
	Command      SpCmd
	Descriptors  []SpDscptr `json:",omitempty"`
	PacketNumber int        `json:",omitempty"`
	Pid          uint16     `json:",omitempty"`
	Program      uint16     `json:",omitempty"`
	Pcr          float64    `json:",omitempty"`
	Pts          float64    `json:",omitempty"`
}

// Decode extracts bits for the Cue values.
func (cue *Cue) Decode(bites []byte) bool {
	var bitn bitter.Bitn
	bitn.Load(bites)
	if !cue.InfoSection.Decode(&bitn) {
		return false
	}
	if !cue.Command.Decode(&bitn, cue.InfoSection.SpliceCommandType) {
		return false
	}
	cue.InfoSection.DescriptorLoopLength = bitn.AsUInt64(16)
	cue.DscptrLoop(&bitn)
	return true
}

// DscptrLoop loops over any splice descriptors
func (cue *Cue) DscptrLoop(bitn *bitter.Bitn) {
	var i uint64
	i = 0
	for i < cue.InfoSection.DescriptorLoopLength {
		var sd SpDscptr
		sd.MetaData(bitn)
		sd.Decode(bitn)
		i += uint64(sd.Length) + 2
		cue.Descriptors = append(cue.Descriptors, sd)
	}
}

//Show display SCTE-35 data as JSON.
func (cue *Cue) Show() {
	fmt.Println(MkJson(&cue))
}
