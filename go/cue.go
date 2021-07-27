package threefive

import (
	"fmt"
	"github.com/futzu/bitter"
)

// Cue a SCTE35 cue.
type Cue struct {
	InfoSection
	Command
	Descriptors  []Descriptor `json:",omitempty"`
	PacketNumber int          `json:",omitempty"`
	Pid          uint16       `json:",omitempty"`
	Program      uint16       `json:",omitempty"`
	Pcr          float64      `json:",omitempty"`
	Pts          float64      `json:",omitempty"`
}

// Decode extracts bits for the Cue values.
func (cue *Cue) Decode(bites []byte) bool {
	var bitn bitter.Bitn
	bitn.Load(bites)
	if !cue.InfoSection.Decode(&bitn) {
		return false
	}
	cmd, ok := cmdMap[cue.InfoSection.SpliceCommandType]
	if ok {
		cue.Command = cmd
		cue.Command.Decode(&bitn)
		cue.InfoSection.DescriptorLoopLength = bitn.AsUInt64(16)
		cue.dscptrLoop(&bitn)
		return true
	}
	return false
}

// DscptrLoop loops over any splice descriptors
func (cue *Cue) dscptrLoop(bitn *bitter.Bitn) {
	var i uint64
	i = 0
	for i < cue.InfoSection.DescriptorLoopLength {
		tag := bitn.AsUInt8(8)
		length := bitn.AsUInt8(8)
		id := bitn.AsAscii(32)
		sd, ok := dscptrMap[tag]
		if ok {
			var Dscptr Descriptor
			Dscptr = sd
			Dscptr.MetaData(tag, length, id)
			Dscptr.Decode(bitn)
			i += uint64(length) + 2
			cue.Descriptors = append(cue.Descriptors, Dscptr)
		}
	}
}

//Show display SCTE-35 data as JSON.
func (cue *Cue) Show() {
	fmt.Println(MkJson(&cue))
}
