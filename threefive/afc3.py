from bitn import BitBin

"""
afc3.py
Parses Packet Headers and Program Association Tables.
It's the ISO13818 spec, stripped down to only the parts
needed to parse SCTE35. The afc3 technique parses video
four times faster.
"""


class Header:
    """
    Header is a class to parse packet header data.
    """

    def __init__(self):
        self.pid = None
        self.adapt_field_flag = None
        self.afl = None
        self.head = b""
        self.payload = b""

    def decode(self, pkt):
        bitbin = BitBin(pkt)
        bitbin.forward(11)
        self.pid = bitbin.asint(13)
        # self.scramble = bitbin.asint(2)
        bitbin.forward(2)
        self.adapt_field_flag = bitbin.asflag(1)
        bitbin.forward(5)
        if self.adapt_field_flag:
            self.afl = bitbin.asint(8)  # pkt[4]
            bitbin.forward(self.afl << 3)
        bitbin.forward(8)  # pkt[4]
        head_bites = (bitbin.bitsize - bitbin.idx) >> 3
        self.head, self.payload = pkt[:head_bites], pkt[head_bites:]
        return bitbin

    def show(self):
        print(vars(self))


class Pat:
    """
    Pat is a class to parse Program Association Tables
    """

    def __init__(self):
        self.section_length = None
        self.program_number = None
        self.network_pid = None
        self.pmt_pids = set()

    def decode(self, pkt):
        head = Header()
        bitbin = head.decode(pkt)
        # self.table_id = bitbin.asint(8)
        # self.section_syntax_indicator = bitbin.asflag(1)
        bitbin.forward(9)
        if bitbin.asflag(1):
            return
        # reserved
        bitbin.forward(2)
        self.section_length = bitbin.asint(12)
        secl = self.section_length << 3
        # self.transport_stream_id = bitbin.asint(16)
        bitbin.forward(40)
        secl -= 40
        while secl > 32:  # self.crc = bitbin.asint(32)
            self.program_number = bitbin.asint(16)  # 16
            bitbin.forward(3)  # 3
            secl -= 19  # 16 + 3  = 19
            if self.program_number == 0:
                self.network_pid = bitbin.asint(13)
            else:
                self.pmt_pids.add(bitbin.asint(13))
            secl -= 13
        bitbin = None

    def show(self):
        print(vars(self))
