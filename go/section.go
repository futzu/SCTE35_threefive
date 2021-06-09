package threefive

import "github.com/futzu/bitter"

// SpInfo is the splice info section of the SCTE 35 cue.
type SpInfo struct {
	Name                   string
	TableId                string
	SectionSyntaxIndicator bool
	Private                bool
	Reserved               string
	SectionLength          uint64
	ProtocolVersion        uint64
	EncryptedPacket        bool
	EncryptionAlgorithm    uint64
	PtsAdjustment          float64
	CwIndex                string
	Tier                   string
	SpliceCommandLength    uint64
	SpliceCommandType      uint64
	DescriptorLoopLength   uint64
}

// Decode splice info section values.
func (spi *SpInfo) Decode(bitn *bitter.Bitn) bool {
	spi.Name = "Splice Info Section"
	spi.TableId = bitn.AsHex(8)
	if spi.TableId != "0xfc" {
		return false
	}
	spi.SectionSyntaxIndicator = bitn.AsBool()
	if spi.SectionSyntaxIndicator {
		return false
	}
	spi.Private = bitn.AsBool()
	spi.Reserved = bitn.AsHex(2)
	spi.SectionLength = bitn.AsUInt64(12)
	spi.ProtocolVersion = bitn.AsUInt64(8)
if spi.ProtocolVersion != 0 {
		return false
	}
	spi.EncryptedPacket = bitn.AsBool()
	spi.EncryptionAlgorithm = bitn.AsUInt64(6)
	spi.PtsAdjustment = bitn.As90k(33)
	spi.CwIndex = bitn.AsHex(8)
	spi.Tier = bitn.AsHex(12)
	spi.SpliceCommandLength = bitn.AsUInt64(12)
	spi.SpliceCommandType = bitn.AsUInt64(8)
	return true
}
