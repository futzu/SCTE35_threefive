package threefive

import "github.com/futzu/bitter"

// InfoSection is the splice info section of the SCTE 35 cue.
type InfoSection struct {
	Name                   string
	TableID                string
	SectionSyntaxIndicator bool
	Private                bool
	Reserved               string
	SectionLength          uint64
	ProtocolVersion        uint8
	EncryptedPacket        bool
	EncryptionAlgorithm    uint8
	PtsAdjustment          float64
	CwIndex                string
	Tier                   string
	SpliceCommandLength    uint64
	SpliceCommandType      uint8
	DescriptorLoopLength   uint64
}

// Decode splice info section values.
func (infosec *InfoSection) Decode(bitn *bitter.Bitn) bool {
	infosec.Name = "Splice Info Section"
	infosec.TableID = bitn.AsHex(8)
	if infosec.TableID != "0xfc" {
		return false
	}
	infosec.SectionSyntaxIndicator = bitn.AsBool()
	if infosec.SectionSyntaxIndicator {
		return false
	}
	infosec.Private = bitn.AsBool()
	infosec.Reserved = bitn.AsHex(2)
	infosec.SectionLength = bitn.AsUInt64(12)
	infosec.ProtocolVersion = bitn.AsUInt8(8)
	if infosec.ProtocolVersion != 0 {
		return false
	}
	infosec.EncryptedPacket = bitn.AsBool()
	infosec.EncryptionAlgorithm = bitn.AsUInt8(6)
	infosec.PtsAdjustment = bitn.As90k(33)
	infosec.CwIndex = bitn.AsHex(8)
	infosec.Tier = bitn.AsHex(12)
	infosec.SpliceCommandLength = bitn.AsUInt64(12)
	infosec.SpliceCommandType = bitn.AsUInt8(8)
	return true
}
