"""
threefive.Cue Class
"""
from base64 import b64decode, b64encode
import json
from sys import stderr
import crcmod.predefined
from .bitn import NBin
from .section import SpliceInfoSection
from .commands import command_map
from .descriptors import splice_descriptor, descriptor_map


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

    def encode(self):
        """
        Cue.encode() converts SCTE35 data
        to a base64 encoded string.
        """
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
        self.bites = self.info_section.encode()
        self.bites += cmd_bites
        self.bites += int.to_bytes(
            self.info_section.descriptor_loop_length, 16, byteorder="big"
        )
        self.bites += dscptr_bites
        self._encode_crc()
        return b64encode(self.bites)

    def _encode_crc(self):
        crc32_func = crcmod.predefined.mkCrcFun("crc-32-mpeg")
        crc_int = crc32_func(self.bites)
        self.crc = hex(crc_int)
        self.bites += int.to_bytes(crc_int, 32, byteorder="big")

    def load_info_section(self, isec):
        """
        load_info_section loads data for Cue.info_section
        isec should be a dict.
        if 'splice_command_type' is included,
        an empty command instance will be created for Cue.command
        """
        self.info_section.load(isec)
        if "splice_command_type" in isec:
            cmd_type = isec["splice_command_type"]
            command_map[cmd_type]()

    def load_command(self, cmd):
        """
        load_command loads data for Cue.command
        cmd should be a dict.
        if 'command_type' is included,
        the command instance will be created.
        """
        if "command_type" in cmd:
            self.command = command_map[cmd["command_type"]]()
        if self.command:
            self.command.load(cmd)

    def load_descriptors(self, dlist):
        """
        Load_descriptors loads descriptor data.
        dlist is a list of dicts
        if 'tag' is included in each dict,
        a descriptor instance will be created.
        """
        if not isinstance(dlist, list):
            raise Exception("descriptors should be a list")
        for dstuff in dlist:
            if "tag" in dstuff:
                dscptr = descriptor_map[dstuff["tag"]]()
                dscptr.load(dstuff)
                self.descriptors.append(dscptr)

    def load(self, stuff):
        """
        Cue.load loads SCTE35 data for encoding.
        stuff is a dict or json
        with any or all of these keys
        stuff = {
            'info_section': {dict} ,
            'command': {dict},
            'descriptors': [list of {dicts}],
            }
        """
        if isinstance(stuff, str):
            stuff = json.loads(stuff)
        if "info_section" in stuff:
            self.load_info_section(stuff["info_section"])
        if "command" in stuff:
            self.load_command(stuff["command"])
        if "descriptors" in stuff:
            self.load_descriptors(stuff["descriptors"])

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
                "info_section": self.info_section.get(),
                "command": self.command.get(),
                "descriptors": self.get_descriptors(),
                "crc": self.crc,
            }
            try:
                scte35.update(self.packet_data)
            except:
                pass
            return scte35
        return False

    def get_descriptors(self):
        """
        Returns a list of SCTE 35
        splice descriptors as dicts.
        """
        return [d.get() for d in self.descriptors]

    def get_json(self):
        """
        get_json returns the Cue instance
        data in json.
        """
        return json.dumps(self.get(), indent=4)

    @staticmethod
    def _mk_bits(data):
        """
        Convert Hex and Base64 strings into bytes.
        """
        try:
            # Handles hex byte strings
            i = int(data, 16)
            i_len = i.bit_length() >> 3
            bites = int.to_bytes(i, i_len, byteorder="big")
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
        self.info_section.decode(info_bites)
        return bites[info_size:]

    def _set_splice_command(self, bites):
        """
        parses the command section
        of a SCTE35 cue.
        """
        sct = self.info_section.splice_command_type
        if sct not in command_map:
            return False
        self.command = command_map[sct](bites)
        self.command.decode()
        del self.command.bites
        self.info_section.splice_command_length = self.command.command_length
        bites = bites[self.command.command_length :]
        return bites

    def show(self):
        """
        pretty prints the SCTE 35 message
        """
        print(self.get_json())

    def to_stderr(self):
        """
        Wrapper for printing to sys.stderr
        """
        print(self.get_json(), file=stderr)

    @staticmethod
    def _strip_header(data):
        """
        _strip_header strips off packet headers
        when present
        """
        if data[0] == 0x47:
            return data[5:]
        return data
