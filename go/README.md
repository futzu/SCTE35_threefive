[![Go Report Card](https://goreportcard.com/badge/github.com/FUTZU/threefive/go)](https://goreportcard.com/report/github.com/FUTZU/threefive/go)
# threefive/go			
The threefive Parser in Go.
* __threefive/go__ is __Fast__.
	* __Full decode of 3.7GB of MPEGTS video in 1.187 seconds__ on my [__laptop__](https://www.samsung.com/us/computing/windows-laptops/notebook-series-7/notebook-7-spin-np730qaa-k02us/#specs)  running Debian [__Sid__](https://www.debian.org/releases/sid/).

##### Heads up, work in progress.


| Working           | |
|-------------------|-|
| MPEG-TS          | ✓ |
| Base64 Strings   | ✓ |
| Splice Info Section  | ✓ | 
| Splice Commands  | ✓ |
| Splice Descriptors  | 70% |


|Not Working       	   | |
|--------------------------|-|
| Segmentation Descriptors |x|


#### Installation
```sh
go get -u github.com/futzu/threefive/go
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
