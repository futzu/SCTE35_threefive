"""
streamedit.py

An example of how to edit SCTE35 data
in MPEGTS packets on the fly and pass
the modifiied stream to stdout.

Use like:

pypy3 streamedit.py https://futzu.com/xaa.ts | pypy3 -c 'import threefive; threefive.decode()'

"""


from functools import partial
import sys

from threefive import Stream


class Stream2(Stream):
    """
    Stream2 is a subclass of threefive.Stream
    to demonstrate editing SCTE35 Cues in a MPEGTS stream.

    Use like:

    pypy3 streamedit.py myvideo.ts >> myvideoedited.ts




            BEFORE:
        {
            "info_section": {
                "table_id": "0xfc",
                "section_syntax_indicator": false,
                "private": false,
                "sap_type": "0x3",
                "sap_details": "No Sap Type",
                "section_length": 42,
                "protocol_version": 0,
                "encrypted_packet": false,
                "encryption_algorithm": 0,
                "pts_adjustment": 0.0,
                "cw_index": "0xff",
                "tier": "0xfff",
                "splice_command_length": 15,
                "splice_command_type": 5,
                "descriptor_loop_length": 10,
                "crc": "0xd7165c79"
            },
            "command": {
                "command_length": 15,
                "command_type": 5,
                "name": "Splice Insert",
                "time_specified_flag": true,
                "pts_time": 23683.480033,
                "splice_event_id": 5690,
                "splice_event_cancel_indicator": false,
                "out_of_network_indicator": true,
                "program_splice_flag": true,
                "duration_flag": false,
                "splice_immediate_flag": false,
                "unique_program_id": 0,
                "avail_num": 0,
                "avail_expected": 0
            },
            "descriptors": [
                {
                    "tag": 0,
                    "descriptor_length": 8,
                    "name": "Avail Descriptor",
                    "identifier": "CUEI",
                    "provider_avail_id": 0
                }
            ],
            "packet_data": {
                "pid": "0x40b",
                "program": 1030,
                "pcr": 23677.003267,
                "pts": 23677.030189
            }
        }
        AFTER:

        {
            "info_section": {
                "table_id": "0xfc",
                "section_syntax_indicator": false,
                "private": false,
                "sap_type": "0x3",
                "sap_details": "No Sap Type",
                "section_length": 42,
                "protocol_version": 0,
                "encrypted_packet": false,
                "encryption_algorithm": 0,
                "pts_adjustment"                          # <-- Changed
                "cw_index": "0xff",
                "tier": "0xfff",
                "splice_command_length": 15,
                "splice_command_type": 5,
                "descriptor_loop_length": 10,
                "crc": "0x82fd33d9"
            },
            "command": {
                "command_length": 15,
                "command_type": 5,
                "name": "Splice Insert",
                "time_specified_flag": true,
                "pts_time": 23683.480033,
                "splice_event_id": 5690,
                "splice_event_cancel_indicator": false,
                "out_of_network_indicator": true,
                "program_splice_flag": true,
                "duration_flag": false,
                "splice_immediate_flag": false,
                "unique_program_id": 999,            # <-- Changed
                "avail_num": 0,
                "avail_expected": 0
            },
            "descriptors": [
                {
                    "tag": 0,
                    "descriptor_length": 8,
                    "name": "Avail Descriptor",
                    "identifier": "FUEI",                     # <-- Changed
                    "provider_avail_id": 0
                }
            ],
            "packet_data": {
                "pid": "0x40b",
                "program": 1030,
                "pcr": 23677.003267,
                "pts": 23677.030189
            }
        }

        #    The Changed cues will be in myvideoedited.ts,
        #     Check it like this:

    from threefive import decode

     decode('myvideoedited.ts')


    """

    _PAD = b"\xff"

    @staticmethod
    def edit_cue(cue):
        """
        edit_cue sets cue.info_section.pts_adjustment
        and then re-encodes the SCTE35 Cue.
        """
        print("BEFORE:", file=sys.stderr)
        cue.to_stderr()
        cue.info_section.pts_adjustment = 109.55  # Changed
        cue.command.unique_program_id = 999  # Changed
        if cue.descriptors:
            cue.descriptors[0].identifier = "FUEI"  # Changed
        cue.encode()
        print("AFTER:\n", file=sys.stderr)
        cue.to_stderr()

    def repack_pkt(self, pkt, cue):
        """
        repack_pkt recreates the SCTE35 packet
        with the edited SCTE35 Cue as the payload
        adds padding as needed and then
        writes the new_packet to stdout
        """
        pay_idx = pkt.index(cue.bites)
        header = pkt[:pay_idx]
        self.edit_cue(cue)
        new_payload = cue.bites
        new_pkt = header + new_payload
        new_pkt += (self._PACKET_SIZE - len(new_pkt)) * self._PAD
        sys.stdout.buffer.write(new_pkt)

    def edit_scte35(self):
        """
        edit_scte35 applies Stream2.edit_cue(cue)
        on SCTE35 data before writing all packets
        to stdout.
        """
        if self._find_start():
            for pkt in iter(partial(self._tsdata.read, self._PACKET_SIZE), b""):
                cue = self._parse_plus(pkt)
                if cue:
                    self.repack_pkt(pkt, cue)
                else:
                    sys.stdout.buffer.write(pkt)
        self._tsdata.close()


if __name__ == "__main__":
    args = sys.argv[1:]
    for arg in args:
        strm = Stream2(arg)
        strm.edit_scte35()
