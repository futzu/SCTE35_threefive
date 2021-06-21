package threefive

import "github.com/futzu/bitter"

// SpCmd is the splice command for the SCTE35 cue.
type SpCmd struct {
	Name                       string
	SpliceEventID              string  `json:",omitempty"`
	SpliceEventCancelIndicator bool    `json:",omitempty"`
	OutOfNetworkIndicator      bool    `json:",omitempty"`
	ProgramSpliceFlag          bool    `json:",omitempty"`
	DurationFlag               bool    `json:",omitempty"`
	BreakAutoReturn            bool    `json:",omitempty"`
	BreakDuration              float64 `json:",omitempty"`
	SpliceImmediateFlag        bool    `json:",omitempty"`
	TimeSpecifiedFlag          bool    `json:",omitempty"`
	PTS                        float64 `json:",omitempty"`
	ComponentCount             uint8   `json:",omitempty"`
	Components                 []uint8 `json:",omitempty"`
	UniqueProgramID            uint64  `json:",omitempty"`
	AvailNum                   uint8   `json:",omitempty"`
	AvailExpected              uint8   `json:",omitempty"`
	Identifier                 uint64  `json:",omitempty"`
}

// Decode the splice command values.
func (cmd *SpCmd) Decode(bitn *bitter.Bitn, cmdtype uint8) bool {

	if int(cmdtype) == 0 {
		cmd.SpliceNull()
		return true
	}

	cmdmap := map[int]func(*bitter.Bitn){
		//  0: cmd.SpliceNull,
		5:   cmd.SpliceInsert,
		6:   cmd.TimeSignal,
		7:   cmd.BandwidthReservation,
		255: cmd.PrivateCommand}

	cmdfunc, ok := cmdmap[int(cmdtype)]
	if ok {
		cmdfunc(bitn)
		return true
	}
	return false
}

// ParseBreak parses out the ad break duration values.
func (cmd *SpCmd) ParseBreak(bitn *bitter.Bitn) {
	cmd.BreakAutoReturn = bitn.AsBool()
	bitn.Forward(6)
	cmd.BreakDuration = bitn.As90k(33)
}

// SpliceTime parses out the PTS value as needed.
func (cmd *SpCmd) SpliceTime(bitn *bitter.Bitn) {
	cmd.TimeSpecifiedFlag = bitn.AsBool()
	if cmd.TimeSpecifiedFlag {
		bitn.Forward(6)
		cmd.PTS = bitn.As90k(33)
	} else {
		bitn.Forward(7)
	}
}

// SpliceInsert handles SCTE 35 splice insert commands.
func (cmd *SpCmd) SpliceInsert(bitn *bitter.Bitn) {
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
			cmd.SpliceTime(bitn)
		}
	} else {
		cmd.ComponentCount = bitn.AsUInt8(8)
		var Components [256]uint8
		cmd.Components = Components[0:cmd.ComponentCount]
		for i := range cmd.Components {
			cmd.Components[i] = bitn.AsUInt8(8)
		}
		if !cmd.SpliceImmediateFlag {
			cmd.SpliceTime(bitn)
		}
	}
	if cmd.DurationFlag {
		cmd.ParseBreak(bitn)
	}
	cmd.UniqueProgramID = bitn.AsUInt64(16)
	cmd.AvailNum = bitn.AsUInt8(8)
	cmd.AvailExpected = bitn.AsUInt8(8)
}

// SpliceNull is a No-Op command.
func (cmd *SpCmd) SpliceNull() {
	cmd.Name = "Splice Null"
}

// TimeSignal splice command is a wrapper for SpliceTime.
func (cmd *SpCmd) TimeSignal(bitn *bitter.Bitn) {
	cmd.Name = "Time Signal"
	cmd.SpliceTime(bitn)
}

// BandwidthReservation splice command.
func (cmd *SpCmd) BandwidthReservation(bitn *bitter.Bitn) {
	cmd.Name = "Bandwidth Reservation"
}

// PrivateCommand splice command.
func (cmd *SpCmd) PrivateCommand(bitn *bitter.Bitn) {
	cmd.Name = "Private Command"
	cmd.Identifier = bitn.AsUInt64(32)
}

type AudioCmpnt struct {
	ComponentTag  string `json:"omitempty"`
	ISOCode       uint64 `json:"omitempty"`
	BitstreamMode uint64 `json:"omitempty"`
	NumChannels   uint64 `json:"omitempty"`
	FullSrvcAudio bool   `json:"omitempty"`
}
