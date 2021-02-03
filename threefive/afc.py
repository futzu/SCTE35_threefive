from bitn import BitBin
import sys
from functools import partial
from threefive.streamtype import stream_type_map


class Header:
    def decode(self, bitbin):
        af = None
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
        #    print(vars(af))
        else:
            bitbin.forward(8)


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
        reserved = bitbin.asint(2)
        self.version_number = bitbin.asint(5)
        self.current_next_indicator = bitbin.asflag(1)  # 6 bytes
        self.section_number = bitbin.asint(8)  # 7 bytes
        self.last_section_number = bitbin.asint(8)  # 8 bytes
        sl -= 40
        pmt_pids = set()
        while sl > 32:
            program_number = bitbin.asint(16)
            print("PROGRAM:", program_number)
            bitbin.forward(3)
            sl -= 19
            if program_number == 0:
                network_pid = bitbin.asint(13)
                sl -= 13
                print(f"\tNet Pid  {network_pid}")
            else:
                pmap_pid = bitbin.asint(13)
                sl -= 13
                pmt_pids.add(pmap_pid)
                print(f"\tProgram Map Table Pid {pmap_pid}")
        self.crc = bitbin.asint(32)
        return pmt_pids


class Pmt:
    def decode(self, bitbin):
        self.table_id = bitbin.asint(8)
        self.section_syntax_indicator = bitbin.asflag(1)
        zero = bitbin.asflag(1)
        reserved = bitbin.forward(2)
        self.section_length = bitbin.asint(12)
        slb = self.section_length << 3
        self.program_number = bitbin.asint(16)
        slb -= 16

        bitbin.forward(27)
        slb -= 27
        """
        reserved  = bitbin.asint(2) 
        slb -=2
        self.version_number   = bitbin.asint(5)
        slb -= 5
        self.current_next_indicator  = bitbin.asflag(1)
        slb -= 1
        self.section_number   = bitbin.asint(8)
        slb -= 8
        self.last_section_number  = bitbin.asint(8)                               
        slb -= 8
        reserved = bitbin.asint(3)                                                              
        slb -= 3
        """
        self.PCR_PID = bitbin.asint(13)  # 13
        reserved = bitbin.forward(4)  # +4 = 17
        self.program_info_length = bitbin.asint(12)  # + 29
        slb -= 29
        pil = self.program_info_length << 3
        bitbin.forward(pil)  # Skip descriptors
        slb -= pil
        print(f"Program {self.program_number} Streams")
        while slb > 40:
            stream_type = bitbin.ashex(8)  # 8
            reserved = bitbin.asint(3)  # +3 =11
            elementary_PID = bitbin.asint(13)  # +13 =24
            reserved = bitbin.asint(4)  # +4 = 28
            ES_info_length = bitbin.asint(12)  # +12 =40
            slb -= 40
            slb -= ES_info_length << 3
            bitbin.forward(ES_info_length << 3)
            streaminfo = f"[{stream_type}] Reserved or Private"
            if stream_type in stream_type_map:
                streaminfo = f"[{stream_type}] {stream_type_map[stream_type]}"
            if elementary_PID == self.PCR_PID:
                streaminfo = f" {streaminfo} ( PCR_PID )"
            print(f"\t{elementary_PID }: {streaminfo}")
        self.CRC_32 = bitbin.asint(32)


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

        # AdaptationFields seems correct up to this point,
        # the rest needs to be checked.

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


class StreamParser:
    def __init__(self):
        self.pmt_pids = set()

    def parse(self):
        with open(sys.argv[1], "rb") as tsdata:
            for pkt in iter(partial(tsdata.read, 188), b""):
                bitbin = BitBin(pkt)
                head = Header()
                head.decode(bitbin)
                if head.pid == 0:
                    p = Pas()
                    self.pmt_pids |= p.decode(bitbin)
                if head.pid in self.pmt_pids:
                    pmt = Pmt()
                    pmt.decode(bitbin)


def do():
    sparser = StreamParser()
    sparser.parse()


if __name__ == "__main__":
    do()
