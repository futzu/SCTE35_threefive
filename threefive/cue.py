"""
threefive.Cue Class
"""

import json
import pprint
from base64 import b64decode
from bitn import NBin
from .section import SpliceInfoSection
from .commands import splice_command
from .descriptors import splice_descriptor
from .tools import (
    i2b,
    ifb,
    to_stderr,
)


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

    def __init__(self, data, packet_data=None):
        """
        data may be packet bites or encoded string
        packet_data is a dict passed from a Stream instance
        """
        self.info_section = None
        self.command = None
        self.descriptors = []
        self.data = self._strip_header(data)
        self.bites = self._mk_bits(self.data)
        self.packet_data = packet_data

    def __repr__(self):
        return str(self.get())

    def decode(self):
        """
        Cue.decode() parses for SCTE35 data
        """
        bites = self.mk_info_section(self.bites)
        if not bites:
            raise Exception("Boom! self.mk_info_section(self.bites)")
        bites = self._set_splice_command(bites)
        if not bites:
            raise Exception("Boom! self._set_splice_command(bites) ")
        bites = self._mk_descriptors(bites)
        if not bites:
            raise Exception("Boom! self._mk_descriptors(bites)")
        self.info_section.crc = hex(ifb(bites[0:4]))
        # self.encode()
        return True

    def encode(self):
        nbin = NBin()
        self.info_section.encode(nbin)
        self.command.encode(nbin)
        nbin.add_int(self.info_section.descriptor_loop_length, 16)
        [d.encode(nbin) for d in self.descriptors]
        nbin.add_hex(self.info_section.crc, 32)
        # if nbin.bites != self.bites:
        to_stderr(f" Cue.bites --->>> {self.bites}\n")
        to_stderr(f" Encoded   --->>> {nbin.bites}\n")

    def _descriptorloop(self, bites, dll):
        """
        parse all splice descriptors
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
        Returns a dict of dicts for all three parts
        of a SCTE 35 message.
        """
        if self.command and self.info_section:
            scte35 = {
                "info_section": self.get_info_section(),
                "command": self.get_command(),
                "descriptors": self.get_descriptors(),
            }
            if self.packet_data:
                scte35.update(self.get_packet_data())
            return scte35
        return False

    def get_command(self):
        """
        returns the SCTE 35
        splice command data as a dict.
        """
        return self._kv_clean(vars(self.command))

    def get_descriptors(self):
        """
        Returns a list of SCTE 35
        splice descriptors as dicts.
        """
        return [self._kv_clean(vars(d)) for d in self.descriptors]

    def get_info_section(self):
        """
        Returns SCTE 35
        splice info section as a dict
        """
        return self._kv_clean(vars(self.info_section))

    def get_json(self):
        """
        get_json returns the Cue instance
        data in json.
        """
        return json.dumps(self.get(), indent=4)

    def get_packet_data(self):
        """
        returns cleaned Cue.packet_data
        """
        return self._kv_clean(self.packet_data)

    @staticmethod
    def _kv_clean(obj):
        """
        kv_clean removes items from a dict if the value is None
        """
        return {k: v for k, v in obj.items() if v is not None}

    @staticmethod
    def _mk_bits(data):
        """
        Convert Hex and Base64 strings into bytes.
        """
        try:
            # Handles hex byte strings
            i = int(data, 16)
            i_len = i.bit_length() >> 3
            bites = i2b(i, i_len)
            return bites
        except:
            if data[:2].lower() == "0x":
                data = data[2:]
            if data[:2].lower() == "fc":
                return bytes.fromhex(data)
        try:
            return b64decode(data)
        except Exception:
            return data

    def _mk_descriptors(self, bites):
        """
        parse descriptor loop length,
        then call Cue._descriptorloop
        """
        try:
            dll = (bites[0] << 8) | bites[1]
        except:
            return False
        self.info_section.descriptor_loop_length = dll
        bites = bites[2:]
        self._descriptorloop(bites, dll)
        return bites[dll:]

    def mk_info_section(self, bites):
        """
        parses the Splice Info Section
        of a SCTE35 cue.
        """
        info_size = 14
        info_bites = bites[:info_size]
        self.info_section = SpliceInfoSection()
        self.info_section.decode(info_bites)
        return bites[info_size:]

    def pretty_print(self):
        pp = pprint.PrettyPrinter(indent=2, compact=True)
        pp.pprint(self.get())

    def _set_splice_command(self, bites):
        """
        parses the command section
        of a SCTE35 cue.
        """
        sct = self.info_section.splice_command_type
        self.command = splice_command(sct, bites)
        if self.command:
            del self.command.bites
            bites = bites[self.command.command_length :]
        return bites

    def show(self):
        """
        pretty prints the SCTE 35 message
        """
        to_stderr(self.get_json())

    @staticmethod
    def _strip_header(data):
        """
        _strip_header strips off packet headers
        when present
        """
        if data[0] == 0x47:
            return data[5:]
        return data
