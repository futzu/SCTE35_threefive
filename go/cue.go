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
	dtags := []uint8{0, 1, 2, 3, 4}
	var i uint64
	i = 0
	l := cue.InfoSection.DescriptorLoopLength
	for i < l {
		//fmt.Printf("%v -- %v\n", i, cue.InfoSection.DescriptorLoopLength)

		tag := bitn.AsUInt8(8)
		i += 1
		length := bitn.AsUInt64(8)
		i += 1
		i += length
		if isIn8(dtags, tag) {

			var sd Descriptor

			if tag == 0 {
				sd = &AvailDscptr{}
			}
			if tag == 1 {
				sd = &DTMFDscptr{}
			}
			if tag == 2 {
				sd = &SegmentDscptr{}
			}
			if tag == 3 {
				sd = &TimeDscptr{}
			}
			if tag == 4 {
				sd = &AudioDscptr{}

			}

			sd.Decode(bitn, tag, uint8(length))
			cue.Descriptors = append(cue.Descriptors, sd)
		}
	}
}

//Show display SCTE-35 data as JSON.
func (cue *Cue) Show() {
	fmt.Println(MkJson(&cue))
}
