import sys

from .cue import Cue
from functools import partial
from .tools import CMD_TYPES, parse_pid


class StreamB:
    """
    threefive.StreamB(tsdata, show_null = False)
    Fast parse mpegts files and streams
    for SCTE 35 packets

    tsdata should be a _io.BufferedReader instance:
    example:
        import threefive
        with open('vid.ts','rb') as tsdata:
            threefive.StreamB(tsdata)

    SCTE-35 Splice null packets are ignored by default.
    Set show_null = True to show splice null.

    """

    _CMD_TYPES = CMD_TYPES
    _PACKET_SIZE = 188

    def __init__(self, tsdata, show_null=False):
        # set show_null to parse splice null packets
        if show_null:
            self.cmd_types.append(0)
        self._tsdata = tsdata
        self.packet_data = {}
        self.get_next = False

    def decode(self):
        """
        StreamB.decode() reads MPEG-TS
        to find SCTE-35 packets.
        """
        self._find_start()
        for packet in iter(partial(self._tsdata.read, self._PACKET_SIZE), b""):
            try:
                packet = packet[:5] + b"\xfc0" + packet.split(b"\x00\xfc0")[1]
            except:
                continue
            if self.chk_magic(packet):
                self.packet_data["pid"] = parse_pid(packet[1], packet[2])
                cuep = Cue(packet, self.packet_data)
                if self.get_next:
                    return cuep
                cuep.show()

    def decode_next(self):
        """
        StreamB.decode_next() reads MPEG-TS
        to find a SCTE-35 packet and returns the packet
        when found.
        """
        self.get_next = True
        cuep = self.decode()
        if cuep:
            return cuep
        return False

    def chk_magic(self, packet):
        """
        Stream.chk_magic(packet)
        does fast SCTE-35 packet detection
        """
        if len(packet) < 20:
            return False
        if packet[5] == 0xFC:
            if packet[6] == 48:
                if packet[8] == 0:
                    if packet[15] == 255:
                        return packet[18] in self._CMD_TYPES

    def _find_start(self):
        """
        handles partial packets
        """
        pkt = self._tsdata.read(self._PACKET_SIZE)
        if pkt[0] == 71:  # charcode for 'G'
            return
        sync_byte = b"G"  #
        while self._tsdata:
            one_byte = self._tsdata.read(1)
            if not one_byte:
                sys.exit()
            if one_byte == sync_byte:
                self._tsdata.read(self._PACKET_SIZE - 1)
                if self._tsdata.read(1) is sync_byte:
                    self._tsdata.read(self._PACKET_SIZE - 1)
                    return
