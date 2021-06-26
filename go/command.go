package threefive

import "github.com/futzu/bitter"

// Command is an interface for Splice Commands
type Command interface {
	Decode(bitn *bitter.Bitn)
}

// SpliceNull is the Splice Null Command
type SpliceNull struct {
	Name string
}

// Decode for the Command interface
func (cmd *SpliceNull) Decode(bitn *bitter.Bitn) {
	cmd.Name = "Splice Null"
	bitn.Forward(0)
}

// SpliceInsert handles SCTE 35 splice insert commands.
type SpliceInsert struct {
	Name                       string
	SpliceEventID              string
	SpliceEventCancelIndicator bool
	OutOfNetworkIndicator      bool
	ProgramSpliceFlag          bool
	DurationFlag               bool
	BreakAutoReturn            bool
	BreakDuration              float64
	SpliceImmediateFlag        bool
	TimeSpecifiedFlag          bool
	PTS                        float64
	ComponentCount             uint8
	Components                 []uint8
	UniqueProgramID            uint64
	AvailNum                   uint8
	AvailExpected              uint8
}

// Decode for the Command interface
func (cmd *SpliceInsert) Decode(bitn *bitter.Bitn) {
	cmd.Name = "Splice Insert"
	cmd.SpliceEventID = bitn.AsHex(32)
	cmd.SpliceEventCancelIndicator = bitn.AsBool()
	bitn.Forward(7)
	if !cmd.SpliceEventCancelIndicator {
		cmd.OutOfNetworkIndicator = bitn.AsBool()
		cmd.ProgramSpliceFlag = bitn.AsBool()
		cmd.DurationFlag = bitn.AsBool()
		cmd.SpliceImmediateFlag = bitn.AsBool()
		bitn.Forward(4)
	}
	if cmd.ProgramSpliceFlag {
		if !cmd.SpliceImmediateFlag {
			cmd.spliceTime(bitn)
		}
	} else {
		cmd.ComponentCount = bitn.AsUInt8(8)
		var Components [256]uint8
		cmd.Components = Components[0:cmd.ComponentCount]
		for i := range cmd.Components {
			cmd.Components[i] = bitn.AsUInt8(8)
		}
		if !cmd.SpliceImmediateFlag {
			cmd.spliceTime(bitn)
		}
	}
	if cmd.DurationFlag {
		cmd.parseBreak(bitn)
	}
	cmd.UniqueProgramID = bitn.AsUInt64(16)
	cmd.AvailNum = bitn.AsUInt8(8)
	cmd.AvailExpected = bitn.AsUInt8(8)
}

func (cmd *SpliceInsert) spliceTime(bitn *bitter.Bitn) {
	cmd.TimeSpecifiedFlag = bitn.AsBool()
	if cmd.TimeSpecifiedFlag {
		bitn.Forward(6)
		cmd.PTS = bitn.As90k(33)
	} else {
		bitn.Forward(7)
	}
}

// ParseBreak parses out the ad break duration values.
func (cmd *SpliceInsert) parseBreak(bitn *bitter.Bitn) {
	cmd.BreakAutoReturn = bitn.AsBool()
	bitn.Forward(6)
	cmd.BreakDuration = bitn.As90k(33)
}
