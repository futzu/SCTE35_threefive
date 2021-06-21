package threefive

import "github.com/futzu/bitter"

// SpInfo is the splice info section of the SCTE 35 cue.
type SpInfo struct {
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
func (spi *SpInfo) Decode(bitn *bitter.Bitn) bool {
	spi.Name = "Splice Info Section"
	spi.TableID = bitn.AsHex(8)
	if spi.TableID != "0xfc" {
		return false
	}
	spi.SectionSyntaxIndicator = bitn.AsBool()
	if spi.SectionSyntaxIndicator {
		return false
	}
	spi.Private = bitn.AsBool()
	spi.Reserved = bitn.AsHex(2)
	spi.SectionLength = bitn.AsUInt64(12)
	spi.ProtocolVersion = bitn.AsUInt8(8)
	if spi.ProtocolVersion != 0 {
		return false
	}
	spi.EncryptedPacket = bitn.AsBool()
	spi.EncryptionAlgorithm = bitn.AsUInt8(6)
	spi.PtsAdjustment = bitn.As90k(33)
	spi.CwIndex = bitn.AsHex(8)
	spi.Tier = bitn.AsHex(12)
	spi.SpliceCommandLength = bitn.AsUInt64(12)
	spi.SpliceCommandType = bitn.AsUInt8(8)
	return true
}
