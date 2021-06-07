[![Go Report Card](https://goreportcard.com/badge/github.com/FUTZU/threefive/go)](https://goreportcard.com/report/github.com/FUTZU/threefive/go)
# threefive/go			
The threefive Parser in Go.

##### Heads up, work in progress.

#### What is working:



| SCTE35 Formats    |   |
|-------------------|-----|
| MPEG-TS           | ✓ |
| Base64 Strings    |   ✓ |
   


| Splice Commands         |   |
|-------------------------|-------|
|   Splice Insert         |  ✓    |
|  Splice Null            |  ✓    |
|  Time Signal            |  ✓    |
|     Private Command     |   ✓   |
|  Bandwidth Reservation  |    ✓  |


|Splice Descriptors        |    |
|--------------------------|-----|
| Avail Descriptors        |   ✓ |
| DTMF descriptors         |   ✓ |
| Time Descriptors         |    ✓|
| Segmentation Descriptors | x    |


#### Installation
```sh
go get -u github.com/futzu/scte35
```
#### Parsing MPEGTS files 
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
*  Use.
```sh	
~$ :~$  ./test mpegts/udp.livetv.ts 

Next File: mpegts/udp.livetv.ts
{
    "InfoSection": {
        "Name": "Splice Info Section",
        "TableId": "0xfc",
        "SectionSyntaxIndicator": false,
        "Private": false,
        "Reserved": "0x3",
        "SectionLength": 49,
        "ProtocolVersion": 0,
        "EncryptedPacket": false,
        "EncryptionAlgorithm": 0,
        "PtsAdjustment": 0,
        "CwIndex": "0x0",
        "Tier": "0xfff",
        "SpliceCommandLength": 20,
        "SpliceCommandType": 5,
        "DescriptorLoopLength": 12
    },
    "Command": {
        "Name": "Splice Insert",
        "SpliceEventId": "0x5d",
        "SpliceEventCancelIndicator": false,
        "OutOfNetworkIndicator": true,
        "ProgramSpliceFlag": true,
        "DurationFlag": true,
        "BreakAutoReturn": false,
        "BreakDuration": 90.023266,
        "SpliceImmediateFlag": false,
        "TimeSpecifiedFlag": true,
        "PTS": 38113.135577,
        "UniqueProgramId": 0,
        "AvailNum": 0,
        "AvailExpected": 0,
        "Identifier": 0
    },
    "Descriptors": [
        {
            "DescriptorType": 1,
            "DescriptorLen": 10,
            "Identifier": "0x43554549",
            "Name": "DTMF Descriptor",
            "ProviderAvailId": 0,
            "PreRoll": 177,
            "DTMFCount": 4,
            "DTMFChars": [
                "1",
                "2",
                "1",
                "*"
            ]
        }
    ],
    "Pid": 515,
    "Program": 51,
    "Pts": 38103.872111,
    "Pcr": 38103.868588
}
{
    "InfoSection": {
        "Name": "Splice Info Section",
        "TableId": "0xfc",
        "SectionSyntaxIndicator": false,
        "Private": false,
        "Reserved": "0x3",
        "SectionLength": 44,
        "ProtocolVersion": 0,
        "EncryptedPacket": false,
        "EncryptionAlgorithm": 0,
        "PtsAdjustment": 0,
        "CwIndex": "0x0",
        "Tier": "0xfff",
        "SpliceCommandLength": 15,
        "SpliceCommandType": 5,
        "DescriptorLoopLength": 12
    },
    "Command": {
        "Name": "Splice Insert",
        "SpliceEventId": "0x5e",
        "SpliceEventCancelIndicator": false,
        "OutOfNetworkIndicator": false,
        "ProgramSpliceFlag": true,
        "DurationFlag": false,
        "BreakAutoReturn": false,
        "SpliceImmediateFlag": false,
        "TimeSpecifiedFlag": true,
        "PTS": 38203.125477,
        "UniqueProgramId": 0,
        "AvailNum": 0,
        "AvailExpected": 0,
        "Identifier": 0
    },
    "Descriptors": [
        {
            "DescriptorType": 1,
            "DescriptorLen": 10,
            "Identifier": "0x43554549",
            "Name": "DTMF Descriptor",
            "ProviderAvailId": 0,
            "PreRoll": 177,
            "DTMFCount": 4,
            "DTMFChars": [
                "1",
                "2",
                "1",
                "#"
            ]
        }
    ],
    "Pid": 515,
    "Program": 51,
    "Pts": 38199.872111,
    "Pcr": 38199.918911
}



``` 	

#### Parsing a base64 string
```go
/** call this file test1.go

    go build test1.go 
    
   ./test1 "/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo="
**/

package main

import (
	"os"
	"fmt"
	"github.com/futzu/threefive/go"
)

func main() {


	args := os.Args[1:]
	for i := range args{
		bites := threefive.DeB64(args[i])
		fmt.Println(args[i])
		threefive.SCTE35Parser(bites)
	}
}
```  
---
##### Output 
*(Now in json format)*
```js
}
1035
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
        "SpliceEventId": "0x163a",
        "SpliceEventCancelIndicator": false,
        "OutOfNetworkIndicator": true,
        "ProgramSpliceFlag": true,
        "DurationFlag": false,
        "BreakAutoReturn": false,
        "SpliceImmediateFlag": false,
        "TimeSpecifiedFlag": true,
        "PTS": 23683.480033,
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
            "ProviderAvailId": 0
        }
    ]
}

	
```
