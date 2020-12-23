'''
SCTE35 DTMF Descriptor Example

Usage:
    pypy3 dtmf.py

Output:

{
  "info_section": {
    "table_id": "0xfc",
    "section_syntax_indicator": false,
    "private": false,
    "reserved": "0x3",
    "section_length": 44,
    "protocol_version": 0,
    "encrypted_packet": false,
    "encryption_algorithm": 0,
    "pts_adjustment": 0.0,
    "cw_index": "0x0",
    "tier": "0xfff",
    "splice_command_length": 15,
    "splice_command_type": 5,
    "descriptor_loop_length": 12,
    "crc": "0x11a8966d"
  },
  "command": {
    "name": "Splice Insert",
    "time_specified_flag": true,
    "pts_time": 38203.125478,
    "splice_event_id": 94,
    "splice_event_cancel_indicator": false,
    "out_of_network_indicator": false,
    "program_splice_flag": true,
    "duration_flag": false,
    "splice_immediate_flag": false,
    "unique_program_id": 0,
    "avail_num": 0,
    "avail_expected": 0,
    "splice_command_length": 15
  },
  "descriptors": [
    {
      "tag": 1,
      "identifier": "CUEI",
      "name": "DTMF Descriptor",
      "preroll": 177,
      "dtmf_count": 4,
      "dtmf_chars": [
        "1",
        "2",
        "1",
        "#"
      ],
      "descriptor_length": 10
    }
  ]
}

'''


from threefive import decode

dtmf =b'/DAsAAAAAAAAAP/wDwUAAABef0/+zPACTQAAAAAADAEKQ1VFSbGfMTIxIxGolm3/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////'

decode(dtmf)
