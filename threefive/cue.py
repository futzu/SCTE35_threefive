"""
threefive.Cue Class
"""
import json
from base64 import b64decode, b64encode
import crcmod.predefined
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
        isb = bytearray(self.bites[:-4])
        bites = self.mk_info_section(self.bites)
        if not bites:
            raise Exception("Boom! self.mk_info_section(self.bites)")
        bites = self._set_splice_command(bites)
        if not bites:
            raise Exception("Boom! self._set_splice_command(bites) ")
        bites = self._mk_descriptors(bites)
        if not bites:
            raise Exception("Boom! self._mk_descriptors(bites)")
        self.crc = hex(ifb(bites[0:4]))
        return True

    def encode(self):
        dscptr_bites = self._unloop_descriptors()
        dll = len(dscptr_bites)
        self.info_section.descriptor_loop_length = dll
        if not self.command:
            raise Exception("A splice command is required")
        cmd_bites = self.command.encode()
        cmdl = self.command.command_length = len(cmd_bites)
        self.info_section.splice_command_length = cmdl
        self.info_section.splice_command_type = self.command.command_type
        # 11 bytes for info section + command + 2 descriptor loop length
        # + descriptor loop + 4 for crc
        self.info_section.section_length = 11 + cmdl + 2 + dll + 4
        cuebin = NBin()
        info_bites = self.info_section.encode()
        info_bitlen = len(info_bites) << 3
        cuebin.add_bites(info_bites, info_bitlen)
        cmd_bitlen = cmdl << 3
        cuebin.add_bites(cmd_bites, cmd_bitlen)
        cuebin.add_int(self.info_section.descriptor_loop_length, 16)
        cuebin.add_bites(dscptr_bites, (dll << 3))
        crc32_func = crcmod.predefined.mkCrcFun("crc-32-mpeg")
        self.crc = hex(crc32_func(cuebin.bites))
        cuebin.add_hex(self.crc, 32)
        be64 = b64encode(cuebin.bites)
        self.bites = cuebin.bites
        return be64

    def _unloop_descriptors(self):
        """
        _unloop_descriptors
        for each descriptor in self.descriptors
        encode descriptor tag, descriptor length,
        and the descriptor into all_bites.bites
        """
        all_bites = NBin()
        dbite_chunks = [d.encode() for d in self.descriptors]
        for chunk, d in zip(dbite_chunks, self.descriptors):
            d.descriptor_length = len(chunk)
            all_bites.add_int(d.tag, 8)
            all_bites.add_int(d.descriptor_length, 8)
            dbits = d.descriptor_length << 3
            all_bites.add_bites(chunk, dbits)
        return all_bites.bites

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
                "crc": self.crc,
            }
            try:
                scte35.update(self.get_packet_data())
            except:
                pass
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
        # self.info_section = SpliceInfoSection()
        self.info_section.decode(info_bites)
        return bites[info_size:]

    def _set_splice_command(self, bites):
        """
        parses the command section
        of a SCTE35 cue.
        """
        sct = self.info_section.splice_command_type
        self.command = splice_command(sct, bites)
        if self.command:
            del self.command.bites
            self.info_section.splice_command_length = self.command.command_length
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
