# Command Line Encoding

### [Encoding from JSON](#encoding) 

### [Converting SCTE-35 formats](#converting)


## Encoding

The threefive cli tool can now encode JSON to SCTE-35. The JSON needs to be in threefive format. 

*  `a@fu:~$ threefive '/DAWAAAAAAAAAP/wBQb+ABt4xwAAwhCGHw==' 2> json.txt`

*  `cat json.txt`

```json
 {
    "info_section": {
        "table_id": "0xfc",
        "section_syntax_indicator": false,
        "private": false,
        "sap_type": "0x03",
        "sap_details": "No Sap Type",
        "section_length": 22,
        "protocol_version": 0,
        "encrypted_packet": false,
        "encryption_algorithm": 0,
        "pts_adjustment": 0.0,
        "cw_index": "0x00",
        "tier": "0x0fff",
        "splice_command_length": 5,
        "splice_command_type": 6,
        "descriptor_loop_length": 0,
        "crc": "0xc210861f"
    },
    "command": {
        "command_length": 5,
        "command_type": 6,
        "name": "Time Signal",
        "time_specified_flag": true,
        "pts_time": 20.004344
    },
    "descriptors": []
}

```
* Change the pts_time 
    * Here I do it with sed, you can use any editor 

```js
sed -i 's/20.004344/60.0/' json.txt
```
* Re-encode as Base64
```lua
a@fu:~$ cat json.txt | threefive encode

/DAWAAAAAAAAAP/wBQb+AFJlwAAAZ1PBRA==
```

* Re-encode as Hex
```lua
a@fu:~$ cat json.txt | threefive encode hex
0xfc301600000000000000fff00506fe005265c000006753c144
```

* Re-encode as an integer
```lua
a@fu:~$ cat json.txt | threefive encode int
1583008701074197245727019716796221242034694813189400685691204
```
* Re-encode as bytes
 ```lua
a@fu:~$ cat json.txt | threefive encode bytes
b'\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00Re\xc0\x00\x00gS\xc1D'
```

___

## Converting
* Converting involves piping one threefive command into another.
* `From`:
  * Base64
  * Hex
* `To`
  * Base64
  * Bytes
  * Hex
  * Int 

* `Base64` to `hex`
```js
a@fu:~$ threefive '/DAWAAAAAAAAAP/wBQb+ABt4xwAAwhCGHw==' 2>&1 | threefive encode hex
```
```js
0xfc301600000000000000fff00506fe001b78c70000c210861f
```
* `Hex` to `Integer`
```js
a@fu:~$ threefive '0xfc301600000000000000fff00506fe001b78c70000c210861f' 2>&1| threefive encode int
```

```js
1583008701074197245727019716796221242033681613329959740278303
```

* `Hex` to `Bytes`
```js

a@fu:~$ threefive '0xfc301600000000000000fff00506fe001b78c70000c210861f' 2>&1| threefive encode bytes
```
```js
b'\xfc0\x16\x00\x00\x00\x00\x00\x00\x00\xff\xf0\x05\x06\xfe\x00\x1bx\xc7\x00\x00\xc2\x10\x86\x1f'
```
