# threefive/go	 [![Go Report Card](https://goreportcard.com/badge/github.com/FUTZU/threefive)](https://goreportcard.com/report/github.com/FUTZU/threefive)
		
The threefive Parser in Go.

##### Heads up, work in progress.

|Not Working      	   	  | |
|---------------------------------|-|
| Splice Schedule Command 	  |x|
| Splice Segmentation Descriptors |x|


#### Installation
---
```sh
go get -u github.com/futzu/threefive/go
```

#### Parsing MPEGTS files 
---

* Make a file test.go

```go

package main

import (
	"os"
	"fmt"
	"github.com/futzu/threefive/go"
)

func main(){

	args := os.Args[1:]
	for i := range args{
		fmt.Printf( "\nNext File: %s\n\n",args[i] )
		var stream   threefive.Stream
		stream.Decode(args[i])
	}
}     
```
*  Build
```sh 
go build test.go
```
*  Run.
```sh	
~$ ./test threefive/plp0.ts
Next File: threefive/plp0.ts
{
    "InfoSection": {
        "Name": "Splice Info Section",
        "TableId": "0xfc",
        "SectionSyntaxIndicator": false,
        "Private": false,
        "Reserved": "0x3",
        "SectionLength": 42,
        "ProtocolVersion": 0,
        "EncryptedPacket": false,
        "EncryptionAlgorithm": 0,
        "PtsAdjustment": 0,
        "CwIndex": "0xff",
        "Tier": "0xfff",
        "SpliceCommandLength": 15,
        "SpliceCommandType": 5,
        "DescriptorLoopLength": 10
    },
    "Command": {
        "Name": "Splice Insert",
        "SpliceEventId": "0x400004f7",
        "SpliceEventCancelIndicator": false,
        "OutOfNetworkIndicator": false,
        "ProgramSpliceFlag": true,
        "DurationFlag": false,
        "BreakAutoReturn": false,
        "SpliceImmediateFlag": false,
        "TimeSpecifiedFlag": true,
        "PTS": 23696.827655,
        "UniqueProgramId": 1,
        "AvailNum": 12,
        "AvailExpected": 255,
        "Identifier": 0
    },
    "Descriptors": [
        {
            "DescriptorType": 0,
            "DescriptorLen": 8,
            "Identifier": "0x43554549",
            "Name": "Avail Descriptor",
            "ProviderAvailId": 12
        }
    ],
    "PacketNumber": 20038146,
    "Pid": 1015,
    "Program": 1010,
    "Pcr": 23690.340577,
    "Pts": 23690.393066
}
...

``` 	

#### Parsing a base64 string
---

* Make a file test1.go

```go
package main

import (
    "os"
	"github.com/futzu/threefive/go"
)
func main(){
	args := os.Args[1:]
	for i := range args{
        bites := threefive.DeB64(args[i])
        var cue threefive.Cue
        if cue.Decode(bites){
            cue.Show()
        }
    }
}
```  
* Build
```sh
  go build test1.go 
```
* Run
```js
   ./test1 "/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo="

{
    "InfoSection": {
        "Name": "Splice Info Section",
        "TableId": "0xfc",
        "SectionSyntaxIndicator": false,
        "Private": false,
        "Reserved": "0x3",
        "SectionLength": 47,
        "ProtocolVersion": 0,
        "EncryptedPacket": false,
        "EncryptionAlgorithm": 0,
        "PtsAdjustment": 0,
        "CwIndex": "0xff",
        "Tier": "0xfff",
        "SpliceCommandLength": 20,
        "SpliceCommandType": 5,
        "DescriptorLoopLength": 10
    },
    "Command": {
        "Name": "Splice Insert",
        "SpliceEventId": "0x4800008f",
        "SpliceEventCancelIndicator": false,
        "OutOfNetworkIndicator": true,
        "ProgramSpliceFlag": true,
        "DurationFlag": true,
        "BreakAutoReturn": true,
        "BreakDuration": 60.293566,
        "SpliceImmediateFlag": false,
        "TimeSpecifiedFlag": true,
        "PTS": 21514.559088,
        "UniqueProgramId": 0,
        "AvailNum": 0,
        "AvailExpected": 0,
        "Identifier": 0
    },
    "Descriptors": [
        {
            "DescriptorType": 0,
            "DescriptorLen": 8,
            "Identifier": "0x43554549",
            "Name": "Avail Descriptor",
            "ProviderAvailId": 309
        }
    ]
}
```
### Docs
```
a@fumatica:~/go/src/github.com/futzu/threefive/go$ go doc -all .
package threefive // import "github.com/futzu/threefive/go"


CONSTANTS

const BufferSize = 13000 * PktSz
    BufferSize is the size of a read when parsing files.

const PktSz = 188
    PktSz is the size of an MPEG-TS packet in bytes.


VARIABLES

var CmdMap = map[uint8]Command{
	0: &SpliceNull{},
	5: &SpliceInsert{},
	6: &TimeSignal{}}
    CmdMap maps Splice Command Types to the Command interface

var DscptrMap = map[uint8]Descriptor{
	0: &AvailDscptr{},
	1: &DTMFDscptr{},
	2: &SegmentDscptr{},
	3: &TimeDscptr{},
	4: &AudioDscptr{}}
    DscptrMap maps Splice Descriptor Tags to a Descriptor interface


FUNCTIONS

func Chk(e error)
    Chk generic catchall error checking

func DeB64(b64 string) []byte
    DeB64 decodes base64 strings.

func IsIn16(slice []uint16, val uint16) bool
    IsIn16 is a test for slice membership

func IsIn8(slice []uint8, val uint8) bool
    IsIn8 is a test for slice membership

func MkJson(i interface{}) string
    MkJson structs to JSON


TYPES

type AudioCmpt struct {
	ComponentTag  uint8
	ISOCode       uint64
	BitstreamMode uint8
	NumChannels   uint8
	FullSrvcAudio bool
}
    AudioCmpt is a struct for AudioDscptr Components

type AudioDscptr struct {
	SpliceDscptr
	Name       string
	Components []AudioCmpt `json:",omitempty"`
}
    AudioDscptr Audio Splice Descriptor

func (dscptr *AudioDscptr) Decode(bitn *bitter.Bitn)
    Decode for the Descriptor interface

type AvailDscptr struct {
	SpliceDscptr
	Name            string
	ProviderAvailID uint64
}
    AvailDscptr Avail Splice Descriptor

func (dscptr *AvailDscptr) Decode(bitn *bitter.Bitn)
    Decode for the Descriptor interface

type Command interface {
	Decode(bitn *bitter.Bitn)
}
    Command is an interface for Splice Commands

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
    Cue a SCTE35 cue.

func (cue *Cue) Decode(bites []byte) bool
    Decode extracts bits for the Cue values.

func (cue *Cue) DscptrLoop(bitn *bitter.Bitn)
    DscptrLoop loops over any splice descriptors

func (cue *Cue) Show()
    Show display SCTE-35 data as JSON.

type DTMFDscptr struct {
	SpliceDscptr
	Name      string
	PreRoll   uint8
	DTMFCount uint64
	DTMFChars []string `json:",omitempty"`
}
    DTMFDscptr DTMF Splice Descriptor

func (dscptr *DTMFDscptr) Decode(bitn *bitter.Bitn)
    Decode for the Descriptor interface

type Descriptor interface {
	MetaData(t uint8, l uint8, i string)
	Decode(bitn *bitter.Bitn)
}
    Descriptor is the interface for all Splice Descriptors

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
    InfoSection is the splice info section of the SCTE 35 cue.

func (infosec *InfoSection) Decode(bitn *bitter.Bitn) bool
    Decode splice info section values.

type Pids struct {
	// Has unexported fields.
}
    Pids holds collections of pids by type for threefive.Stream.

type SegCmpt struct {
	ComponentTag uint8
	PtsOffset    float64
}
    SegCmpt Segmentation Descriptor Component

type SegmentDscptr struct {
	SpliceDscptr
	Name                             string
	SegmentationEventID              string
	SegmentationEventCancelIndicator bool
	ProgramSegmentationFlag          bool
	SegmentationDurationFlag         bool
	DeliveryNotRestrictedFlag        bool
	WebDeliveryAllowedFlag           bool
	NoRegionalBlackoutFlag           bool
	ArchiveAllowedFlag               bool
	DeviceRestrictions               string    `json:",omitempty"`
	Components                       []SegCmpt `json:",omitempty"`
	SegmentationDuration             float64
	SegmentationMessage              string
	SegmentationUpidType             uint8
	SegmentationUpidTypeName         string
	SegmentationUpidLength           uint8
	SegmentationUpid                 string
	SegmentationTypeID               uint8
	SegmentNum                       uint64
	SegmentsExpected                 uint64 `json:",omitempty"`
	SubSegmentNum                    uint64 `json:",omitempty"`
	SubSegmentsExpected              uint64 `json:",omitempty"`
}
    SegmentDscptr Segmentation Descriptor

func (dscptr *SegmentDscptr) Decode(bitn *bitter.Bitn)
    Decode for the Descriptor interface

type SpliceDscptr struct {
	Tag    uint8 `json:",omitempty"`
	Length uint8 `json:",omitempty"`
	// identiﬁer 32 uimsbf == 0x43554549 (ASCII “CUEI”)
	Identifier string `json:",omitempty"`
}
    SpliceDscptr is embedded in all Splice Descriptor structs

func (dscptr *SpliceDscptr) MetaData(t uint8, l uint8, i string)
    MetaData pass in Tag, Length and ID for Splice Descriptors

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
	TimeSignal
	ComponentCount  uint8   `json:",omitempty"`
	Components      []uint8 `json:",omitempty"`
	UniqueProgramID uint64
	AvailNum        uint8
	AvailExpected   uint8
}
    SpliceInsert handles SCTE 35 splice insert commands.

func (cmd *SpliceInsert) Decode(bitn *bitter.Bitn)
    Decode for the Command interface

type SpliceNull struct {
	Name string
}
    SpliceNull is the Splice Null Command

func (cmd *SpliceNull) Decode(bitn *bitter.Bitn)
    Decode for the Command interface

type Stream struct {
	Pkts int // packet count.

	// Has unexported fields.
}
    Stream for parsing MPEGTS for SCTE-35

func (stream *Stream) Decode(fname string)
    Decode fname (a file name) for SCTE-35

type TimeDscptr struct {
	SpliceDscptr
	Name       string
	TAISeconds uint64
	TAINano    uint64
	UTCOffset  uint64
}
    TimeDscptr Time Splice DSescriptor

func (dscptr *TimeDscptr) Decode(bitn *bitter.Bitn)
    Decode for the Descriptor interface

type TimeSignal struct {
	Name              string
	TimeSpecifiedFlag bool
	PTS               float64
}
    TimeSignal Splice Command

func (cmd *TimeSignal) Decode(bitn *bitter.Bitn)
    Decode for the Command interface


	
```
