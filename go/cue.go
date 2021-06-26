package threefive

import (
	"fmt"
	"github.com/futzu/bitter"
)

// Cue a SCTE35 cue.
type Cue struct {
	InfoSection SpInfo
	Command
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
	cmdList := []uint16{0, 5, 6}
	if !IsIn16(cmdList, uint16(cue.InfoSection.SpliceCommandType)) {
		return false
	}
	if cue.InfoSection.SpliceCommandType == 0 {
		cue.Command = &SpliceNull{}
	}
	if cue.InfoSection.SpliceCommandType == 5 {
		cue.Command = &SpliceInsert{}
	}
	if cue.InfoSection.SpliceCommandType == 6 {
		cue.Command = &TimeSignal{}
	}
	cue.Command.Decode(&bitn)
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
