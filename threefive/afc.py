from bitn import BitBin
import sys
from functools import partial


class Header:
    def decode(self, bitbin):
        self.sync_byte = bitbin.asint(8)
        self.tei = bitbin.asflag(1)
        self.pusi = bitbin.asflag(1)
        self.ts_priority = bitbin.asflag(1)
        self.pid = bitbin.asint(13)
        self.scamble = bitbin.asint(2)
        self.adapt_field_flag = bitbin.asflag(1)
        self.payload_flag = bitbin.asflag(1)
        self.continuity_count = bitbin.asint(4)
        if self.adapt_field_flag:
            af = AdaptationFields()
            af.decode(bitbin, self.pid)
            print(vars(af))
        bitbin.forward(8)
        if self.pid == 0:
            p = Pas()
            p.decode(bitbin)
            # print(vars(p))


class Pas:
    def decode(self, bitbin):
        self.table_id = bitbin.asint(8)  # 1 byte
        self.section_syntax_indicator = bitbin.asflag(1)
        if bitbin.asflag(1):
            return
        reserved = bitbin.asint(2)
        self.section_length = bitbin.asint(12)  # 3 bytes
        sl = self.section_length * 8
        self.transport_stream_id = bitbin.asint(16)  # 5 bytes
        sl -= 16
        reserved = bitbin.asint(2)
        sl -= 2
        self.version_number = bitbin.asint(5)
        sl -= 5
        self.current_next_indicator = bitbin.asflag(1)  # 6 bytes
        sl -= 1
        self.section_number = bitbin.asint(8)  # 7 bytes
        sl -= 8
        self.last_section_number = bitbin.asint(8)  # 8 bytes
        sl -= 8
        while sl > 32:
            program_number = bitbin.asint(16)
            print("PROGRAM:", program_number)
            sl -= 16
            bitbin.forward(3)
            sl -= 3
            if program_number == 0:
                network_pid = bitbin.asint(13)
                sl -= 13
                print(f"\tNet Pid  {network_pid}")
            else:
                pmap_pid = bitbin.asint(13)
                sl -= 13
                print(f"\tProgram Map Table Pid {pmap_pid}")
        self.crc = bitbin.asint(32)
        # print(vars(self))


def parser(bitbin):
    head = Header()
    head.decode(bitbin)


class AdaptationFields:
    def decode(self, bitbin, pid):
        afl = self.adaptation_field_length = bitbin.asint(8)
        print(
            f"Packet Pid: {pid} Adaptation Field Length: {self.adaptation_field_length}"
        )
        afl >>= 3
        if self.adaptation_field_length < 1:
            return
        self.iscontinuity_indicator = bitbin.asflag(1)  # start of 1 byte
        self.random_access_indicator = bitbin.asflag(1)
        self.elementary_stream_priority_indicator = bitbin.asflag(1)
        self.PCR_flag = bitbin.asflag(1)
        self.OPCR_flag = bitbin.asflag(1)
        self.splicing_point_flag = bitbin.asflag(1)
        self.transport_private_data_flag = bitbin.asflag(1)
        self.adaptation_field_extension_flag = bitbin.asflag(1)  # 1 byte
        afl -= 8
        if self.PCR_flag:
            self.program_clock_reference_base = bitbin.as90k(33)  # start of 6 bytes
            self.reserved = bitbin.forward(6)
            self.program_clock_reference_extension = bitbin.asint(9)  # 6 bytes
            print(f"PID: {pid} PCR {self.program_clock_reference_base}")
            afl -= 48
        if self.OPCR_flag:
            self.original_program_clock_reference_base = bitbin.as90k(
                33
            )  # start of 6 bytes
            reserved = bitbin.forward(6)
            self.original_program_clock_reference_extension = bitbin.asint(9)  # 6 bytes
            print(f"PID: {pid} OPCR {self.original_program_clock_reference_base}")
            afl -= 48
        if self.splicing_point_flag:
            self.splice_countdown = bitbin.asint(8)  # 1 byte
            print(f"PID: {pid} Splice Countdown: {self.splice_countdown} ")
            afl -= 8

        if self.transport_private_data_flag:
            tpdl = self.transport_private_data_length = bitbin.asint(8)  # 1 byte
            self.private_data_bytes = []
            while tpdl:
                tpdl -= 1
                self.private_data_bytes.append(bitbin.asint(8))

        if not self.adaptation_field_extension_flag:
            return
        self.adaptation_field_extension_length = bitbin.asint(8)  # 1 byte
        self.ltw_flag = bitbin.asflag(1)
        self.piecewise_rate_flag = bitbin.asflag(1)
        self.seamless_splice_flag = bitbin.asflag(1)
        reserved = bitbin.forward(5)
        if self.ltw_flag:
            self.ltw_valid_flag = bitbin.asflag(1)
            self.ltw_offset = bitbin.asint(15)

        if self.piecewise_rate_flag:
            reserved = bitbin.forward(2)
            self.piecewise_rate = bitbin.asint(22)

        if seamless_splice_flag:
            self.splice_type = bitbin.asint(4)
            self.DTS_next_AU = bitbin.asint(3)  # 31-29
            marker_bit = bitbin.asflag(1)
            self.DTS_next_AU = bitbin.asint(15)  # 29 - 15
            marker_bit = bitbin.asflag(1)
            self.DTS_next_AU = bitbin.asint(15)  # 14-0
            marker_bit = bitbin.asflag(1)

            #  for (i = 0; i < N; i++)
            #      reserved = bitbin.asint(8)


def do():
    with open(sys.argv[1], "rb") as tsdata:
        for pkt in iter(partial(tsdata.read, 188), b""):
            bitbin = BitBin(pkt)
            parser(bitbin)


if __name__ == "__main__":
    do()
