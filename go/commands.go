package threefive

import "github.com/futzu/bitter"

type SpliceCommand struct {
	Name                       string
	CommandType                uint8
	Identifier                 uint64  `json:",omitempty"`
	Bites                      []byte  `json:",omitempty"`
	SpliceEventID              string  `json:",omitempty"`
	SpliceEventCancelIndicator bool    `json:",omitempty"`
	OutOfNetworkIndicator      bool    `json:",omitempty"`
	ProgramSpliceFlag          bool    `json:",omitempty"`
	DurationFlag               bool    `json:",omitempty"`
	BreakAutoReturn            bool    `json:",omitempty"`
	BreakDuration              float64 `json:",omitempty"`
	SpliceImmediateFlag        bool    `json:",omitempty"`
	ComponentCount             uint8   `json:",omitempty"`
	Components                 []uint8 `json:",omitempty"`
	UniqueProgramID            uint64  `json:",omitempty"`
	AvailNum                   uint8   `json:",omitempty"`
	AvailExpected              uint8   `json:",omitempty"`
	TimeSpecifiedFlag          bool    `json:",omitempty"`
	PTS                        float64 `json:",omitempty"`
}

// CommandDecoder returns a Command by cmdtype
func (cmd *SpliceCommand) Decoder(cmdtype uint8, bitn *bitter.Bitn) {
	cmd.CommandType = cmdtype
	switch cmdtype {
	case 0:
		cmd.SpliceNull(bitn)
	case 5:

		cmd.SpliceInsert(bitn)
	case 6:
		cmd.TimeSignal(bitn)
	case 7:
		cmd.BandwidthReservation(bitn)
	case 255:
		cmd.Private(bitn)
	}

}

// Decode for the Command interface
func (cmd *SpliceCommand) BandwidthReservation(bitn *bitter.Bitn) {
	cmd.Name = "Bandwidth Reservation"
	bitn.Forward(0)
}

// Decode for the Command interface
func (cmd *SpliceCommand) Private(bitn *bitter.Bitn) {
	cmd.Name = "Private Command"
	cmd.Identifier = bitn.AsUInt64(32)
	cmd.Bites = bitn.AsBytes(24)
}

// Decode for the Command interface
func (cmd *SpliceCommand) SpliceNull(bitn *bitter.Bitn) {
	cmd.Name = "Splice Null"
	bitn.Forward(0)
}

// Decode for the Command interface
func (cmd *SpliceCommand) SpliceInsert(bitn *bitter.Bitn) {
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
	if cmd.ProgramSpliceFlag == true {
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
	if cmd.DurationFlag == true {
		cmd.parseBreak(bitn)
	}
	cmd.UniqueProgramID = bitn.AsUInt64(16)
	cmd.AvailNum = bitn.AsUInt8(8)
	cmd.AvailExpected = bitn.AsUInt8(8)
}

func (cmd *SpliceCommand) parseBreak(bitn *bitter.Bitn) {
	cmd.BreakAutoReturn = bitn.AsBool()
	bitn.Forward(6)
	cmd.BreakDuration = bitn.As90k(33)
}

func (cmd *SpliceCommand) spliceTime(bitn *bitter.Bitn) {
	cmd.TimeSpecifiedFlag = bitn.AsBool()
	if cmd.TimeSpecifiedFlag {
		bitn.Forward(6)
		cmd.PTS = bitn.As90k(33)
	} else {
		bitn.Forward(7)
	}
}

// Decode for the Command interface
func (cmd *SpliceCommand) TimeSignal(bitn *bitter.Bitn) {
	cmd.Name = "Time Signal"
	cmd.spliceTime(bitn)
}
