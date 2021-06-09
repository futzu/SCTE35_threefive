package threefive

import (
	"bytes"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"github.com/futzu/bitter"
)

// PktSz is the size of an MPEG-TS packet in bytes.
const PktSz = 188

// BufferSize is the size of a read when parsing files.
const BufferSize = 13000 * PktSz

// Generic catchall error checking
func Chk(e error) {
	if e != nil {
		fmt.Println(e)
	}
}

// MkJson structs to JSON
func MkJson(i interface{}) string {
	jason, err := json.MarshalIndent(&i, "", "    ")
	if err != nil {
		fmt.Println(err)
	}
	return string(jason)
}

// DeB64 decodes base64 strings.
func DeB64(b64 string) []byte {
	deb64, err := base64.StdEncoding.DecodeString(b64)
	Chk(err)
	return deb64
}

// IsIn16 is a test for slice membership
func IsIn16(slice []uint16, val uint16) bool {
	for _, item := range slice {
		if item == val {
			return true
		}
	}
	return false
}

func mk90k(raw uint64) float64 {
	nk := float64(raw) / 90000.0
	return float64(uint64(nk*1000000)) / 1000000
}

func parseLen(byte1 byte, byte2 byte) uint16 {
	return uint16(byte1&0xf)<<8 | uint16(byte2)
}

func parsePid(byte1 byte, byte2 byte) uint16 {
	return uint16(byte1&0x1f)<<8 | uint16(byte2)
}

func parsePrgm(byte1 byte, byte2 byte) uint16 {
	return uint16(byte1)<<8 | uint16(byte2)
}

func splitByIdx(payload []byte, bite byte) []byte {
	idx := bytes.IndexByte(payload, bite)
	if idx == -1 {
		return []byte("")
	}
	return payload[idx:]
}

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
func (cue *Cue) Decode(bites []byte) {
	var bitn bitter.Bitn
	bitn.Load(bites)
	cue.InfoSection.Decode(&bitn)
	cue.Command.Decode(&bitn, cue.InfoSection.SpliceCommandType)
	cue.InfoSection.DescriptorLoopLength = bitn.AsUInt64(16)
	cue.DscptrLoop(&bitn)
	fmt.Println(MkJson(&cue))
}

// DscptrLoop loops over any splice descriptors
func (cue *Cue) DscptrLoop(bitn *bitter.Bitn) {
	var i uint64
	i = 0
	for i < cue.InfoSection.DescriptorLoopLength {
		var sd SpDscptr
		sd.MetaData(bitn)
		sd.Decode(bitn)
		i += sd.DescriptorLen + 2
		cue.Descriptors = append(cue.Descriptors, sd)
	}
}
