package threefive

import (
	"bytes"
	"encoding/base64"
	"encoding/json"
	"fmt"
)

// PktSz is the size of an MPEG-TS packet in bytes.
const PktSz = 188

// BufferSize is the size of a read when parsing files.
const BufferSize = 13000 * PktSz

//Chk generic catchall error checking
func Chk(e error) {
	if e != nil {
		fmt.Println(e)
	}
}

// MkJson structs to JSON
func MkJson(i interface{}) string {
	jason, err := json.MarshalIndent(&i, "", "    ")
	Chk(err)
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

func splitByIdx(payload, sep []byte) []byte {
	idx := bytes.Index(payload, sep)
	if idx == -1 {
		return []byte("")
	}
	return payload[idx:]
}
