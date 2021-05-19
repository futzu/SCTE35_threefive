"""
threefive.Cue Class
"""
from base64 import b64decode
import json
from sys import stderr
from .section import SpliceInfoSection
from .commands import command_map
from .descriptors import splice_descriptor


class Cue:
    """
    The threefive.Splice class handles parsing
    SCTE 35 message strings.
    Example usage:

    from threefive import Cue

    Base64 = "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g="
    scte35 = Cue(Base64)
    scte35.decode()
    scte35.show()
    """

    def __init__(self, data=None, packet_data=None):
        """
        data may be packet bites or encoded string
        packet_data is a dict passed from a Stream instance
        """
        self.info_section = SpliceInfoSection()
        self.command = None
        self.descriptors = []
        self.crc = None
        if data:
            self.data = self._strip_header(data)
            self.bites = self._mk_bits(self.data)
            self.packet_data = packet_data

    def __repr__(self):
        return str(vars(self))

    def decode(self):
        """
        Cue.decode() parses for SCTE35 data
        """
        self.descriptors = []
        # self.bites after_info section decoding
        after_info = self.mk_info_section(self.bites)
        if after_info:
            after_cmd = self._set_splice_command(after_info)
            if after_cmd:
                after_dscrptrs = self._mk_descriptors(after_cmd)
                if after_dscrptrs:
                    self.crc = hex(int.from_bytes(after_dscrptrs[0:4], byteorder="big"))
                    return True
        return False

    def _descriptorloop(self, bites, dll):
        """
        Cue._descriptorloop parses all splice descriptors
        """
        tag_n_len_bites = 2  # 1 byte for descriptor tag,
        # 1 byte for descriptor length
        while dll:
            spliced = splice_descriptor(bites)
            if not spliced:
                return
            sdl = spliced.descriptor_length
            sd_size = tag_n_len_bites + sdl
            dll -= sd_size
            bites = bites[sd_size:]
            del spliced.bites
            self.descriptors.append(spliced)

    def get(self):
        """
        Cue.get returns a dict of dicts
        for all three parts of a SCTE 35 message.
        """
        if self.command and self.info_section:
            scte35 = {
                "info_section": self.info_section.get(),
                "command": self.command.get(),
                "descriptors": self.get_descriptors(),
                "crc": self.crc,
            }
            if self.packet_data is not None:
                scte35.update(self.packet_data)
            return scte35
        return False

    def get_descriptors(self):
        """
        Cue.get_descriptors returns a list of
        SCTE 35 splice descriptors as dicts.
        """
        return [d.get() for d in self.descriptors]

    def get_json(self):
        """
        Cue.get_json returns the Cue instance
        data in json.
        """
        return json.dumps(self.get(), indent=4)

    @staticmethod
    def _mk_bits(data):
        """
        cue._mk_bits Converts
        Hex and Base64 strings into bytes.
        """
        try:
            # Handles hex byte strings
            i = int(data, 16)
            i_len = i.bit_length() >> 3
            bites = int.to_bytes(i, i_len, byteorder="big")
            return bites
        except (LookupError, TypeError, ValueError):
            if data[:2].lower() == "0x":
                data = data[2:]
            if data[:2].lower() == "fc":
                return bytes.fromhex(data)
        try:
            return b64decode(data)
        except (LookupError, TypeError, ValueError):
            return data

    def _mk_descriptors(self, bites):
        """
        Cue._mk_descriptors parses
        Cue.info_section.descriptor_loop_length,
        then call Cue._descriptorloop
        """
        try:
            dll = (bites[0] << 8) | bites[1]
        except (LookupError, TypeError, ValueError):
            return False
        self.info_section.descriptor_loop_length = dll
        bites = bites[2:]
        self._descriptorloop(bites, dll)
        return bites[dll:]

    def mk_info_section(self, bites):
        """
        Cue.mk_info_section parses the
        Splice Info Section
        of a SCTE35 cue.
        """
        info_size = 14
        info_bites = bites[:info_size]
        self.info_section.decode(info_bites)
        return bites[info_size:]

    def _set_pts(self):
        """
        Cue._set_pts applies pts adjustment
        and calculates preroll if needed.
        """
        if self.command.name in ["Splice Insert", "Time Signal"]:
            if self.command.pts_time:
                self.command.pts_time += self.info_section.pts_adjustment

    def _set_splice_command(self, bites):
        """
        Cue._set_splice_command parses
        the command section of a SCTE35 cue.
        """
        sct = self.info_section.splice_command_type
        if sct not in command_map:
            return False
        self.command = command_map[sct](bites)
        self.command.decode()
        del self.command.bites
        bites = bites[self.command.calculated_length :]
        self._set_pts()
        return bites

    def show(self):
        """
        Cue.show pretty prints the SCTE 35 message
        """
        print(self.get_json())

    def to_stderr(self):
        """
        Cue.to_stderr is a Wrapper
        for printing to sys.stderr
        """
        print(self.get_json(), file=stderr)

    @staticmethod
    def _strip_header(data):
        """
        Cue._strip_header strips off
        packet headers when present
        """
        if data[0] == 0x47:
            return data[5:]
        return data
