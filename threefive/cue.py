"""
threefive.Cue Class
"""

from base64 import b64decode, b64encode
import json
from .stuff import print2
from .bitn import NBin
from .base import SCTE35Base
from .section import SpliceInfoSection
from .commands import command_map
from .descriptors import splice_descriptor, descriptor_map
from .crc import crc32


class Cue(SCTE35Base):
    """
    The threefive.Splice class handles parsing
    SCTE 35 message strings.
    Example usage:

    >>>> import threefive
    >>>> Base64 = "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g="
    >>>> cue = threefive.Cue(Base64)

    # cue.decode() returns True on success,or False if decoding failed

    >>>> cue.decode()
    True

    # After Calling cue.decode() the instance variables can be accessed via dot notation.

    >>>> cue.command
    {'command_length': 5, 'name': 'Time Signal', 'time_specified_flag': True,
    'pts_time': 21695.740089}

    >>>> cue.command.pts_time
    21695.740089

    >>>> cue.info_section.table_id

    '0xfc'

    """

    def __init__(self, data=None, packet_data=None):
        """
        data may be packet bites or encoded string
        packet_data is a instance passed from a Stream instance
        """
        self.bites = None
        if data:
            self.bites = self._mk_bits(data)
        self.info_section = SpliceInfoSection()
        self.command = None
        self.descriptors = []
        self.packet_data = packet_data

    def __repr__(self):
        return str(self.__dict__)

    # decode

    def decode(self):
        """
        Cue.decode() parses for SCTE35 data
        """
        bites = self.bites
        self.descriptors = []
        while bites:
            bites = self.mk_info_section(bites)
            bites = self._set_splice_command(bites)
            bites = self._mk_descriptors(bites)
            crc = hex(int.from_bytes(bites[0:4], byteorder="big"))
            self.info_section.crc = crc
            return True
        return False

    def _descriptor_loop(self, loop_bites):
        """
        Cue._descriptor_loop parses all splice descriptors
        """
        tag_n_len = 2
        while loop_bites:
            spliced = splice_descriptor(loop_bites)
            if not spliced:
                return
            sd_size = tag_n_len + spliced.descriptor_length
            loop_bites = loop_bites[sd_size:]
            del spliced.bites
            self.descriptors.append(spliced)

    def get(self):
        """
        Cue.get returns the SCTE-35 Cue
        data as a dict of dicts.
        """
        if self.command and self.info_section:
            scte35 = {
                "info_section": self.info_section.get(),
                "command": self.command.get(),
                "descriptors": self.get_descriptors(),
            }
            if self.packet_data is not None:
                scte35["packet_data"] = self.packet_data.get()
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
    def fix_bad_b64(data):
        while len(data) % 4 != 0:
            data = data + "="
        return data

    def _mk_bits(self,data):
        """
        cue._mk_bits Converts
        Hex and Base64 strings into bytes.
        """
        if isinstance(data, bytes):
            return data[data.index(b"\xfc") :]
        # handles int and unquoted hex
        if isinstance(data, int):
            length = data.bit_length() >> 3
            bites = int.to_bytes(data, length, byteorder="big")
            return bites
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
            return b64decode(self.fix_bad_b64(data))
        except (LookupError, TypeError, ValueError):
            return data

    def _mk_descriptors(self, bites):
        """
        Cue._mk_descriptors parses
        Cue.info_section.descriptor_loop_length,
        then call Cue._descriptor_loop
        """
        dll = (bites[0] << 8) | bites[1]
        self.info_section.descriptor_loop_length = dll
        bites = bites[2:]
        self._descriptor_loop(bites[:dll])
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
        self.info_section.splice_command_length = self.command.command_length
        bites = bites[self.command.command_length :]
        return bites

    def show(self):
        """
        Cue.show prints the Cue as JSON
        """
        print2(self.get_json())

    def to_stderr(self):
        """
        Cue.to_stderr prints the Cue
        as JSON to sys.stderr
        """
        # print(self.get_json(), file=stderr)
        self.show()

    # encode related

    def encode(self):
        """
        Cue.encode() converts SCTE35 data
        to a base64 encoded string.
        """
        dscptr_bites = self._unloop_descriptors()
        dll = len(dscptr_bites)
        self.info_section.descriptor_loop_length = dll
        if not self.command:
            err_mesg = "\033[7mA splice command is required\033[27m"
            raise ValueError(err_mesg)
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
            self.info_section.descriptor_loop_length, 2, byteorder="big"
        )
        self.bites += dscptr_bites
        self._encode_crc()
        return b64encode(self.bites).decode()

    def encode_as_int(self):
        """
        encode_as_int returns self.bites as an int.
        """
        self.encode()
        return int.from_bytes(self.bites, byteorder="big")

    def encode_as_hex(self):
        """
        encode_as_hex returns self.bites as
        a hex string
        """
        return hex(self.encode_as_int())

    def _encode_crc(self):
        """
        _encode_crc encode crc32
        """
        crc_int = crc32(self.bites)
        self.info_section.crc = hex(crc_int)
        self.bites += int.to_bytes(crc_int, 4, byteorder="big")

    def _unloop_descriptors(self):
        """
        _unloop_descriptors
        for each descriptor in self.descriptors
        encode descriptor tag, descriptor length,
        and the descriptor into all_bites.bites
        """
        all_bites = NBin()
        dbite_chunks = [dsptr.encode() for dsptr in self.descriptors]
        for chunk, dsptr in zip(dbite_chunks, self.descriptors):
            dsptr.descriptor_length = len(chunk)
            all_bites.add_int(dsptr.tag, 8)
            all_bites.add_int(dsptr.descriptor_length, 8)
            all_bites.add_bites(chunk)
        return all_bites.bites

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
        if not isinstance(cmd, dict):
            try:
                cmd = cmd.get()
            except:
                print2(f" cmd is a {type(cmd)} should be a dict,")
                return
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
            if not isinstance(dstuff, dict):
                try:
                    dstuff = dstuff.get()
                except:
                    print(f" dstuff is a {type(dstuff)} should be a dict,")
                    return
            if "tag" in dstuff:
                dscptr = descriptor_map[dstuff["tag"]]()
                dscptr.load(dstuff)
                self.descriptors.append(dscptr)
