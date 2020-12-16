"""
threefive.Cue Class
"""

import json
from base64 import b64decode
from bitn import BitBin
from .segmentation import SegmentationDescriptor
from .section import SpliceInfoSection
from .descriptors import (
    AvailDescriptor,
    DtmfDescriptor,
    TimeDescriptor,
    AudioDescriptor,
)
from .commands import (
    BandwidthReservation,
    PrivateCommand,
    SpliceNull,
    SpliceInsert,
    TimeSignal,
)
from .tools import (
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

    # map of known descriptors and associated classes
    _descriptor_map = {
        0: AvailDescriptor,
        1: DtmfDescriptor,
        2: SegmentationDescriptor,
        3: TimeDescriptor,
        4: AudioDescriptor,
    }
    # map of known splice commands and associated classes
    _command_map = {
        0: SpliceNull,
        5: SpliceInsert,
        6: TimeSignal,
        7: BandwidthReservation,
        255: PrivateCommand,
    }

    def __init__(self, data, packet_data=None):
        """
        data may be packet payload or encoded string
        packet_data is a dict passed from a Stream instance
        """
        self.info_section = None
        self.command = None
        self.descriptors = []
        data = self._strip_header(data)
        self.payload = self._mk_bits(data)
        self.packet_data = packet_data

    def __repr__(self):
        return str(self.get())

    def decode(self):
        """
        Cue.decode() parses for SCTE35 data
        """
        payload = self.mk_info_section(self.payload)
        payload = self._mk_command(payload)
        payload = self._mk_descriptors(payload)
        self.info_section.crc = hex(ifb(payload[0:4]))

    def _descriptorloop(self, payload, dll):
        """
        parse all splice descriptors
        """
        while dll:
            spliced = self._set_splice_descriptor(payload)
            if not spliced:
                return
            sdl = spliced.descriptor_length
            bump = sdl + 2
            dll -= bump
            payload = payload[bump:]
            self.descriptors.append(spliced)

    def get(self):
        """
        Returns a dict of dicts for all three parts
        of a SCTE 35 message.
        """
        scte35 = {
            "info_section": self.get_info_section(),
            "command": self.get_command(),
            "descriptors": self.get_descriptors(),
        }
        if self.packet_data:
            scte35.update(self.get_packet_data())
        return scte35

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
        return json.dumps(self.get(), indent=2)

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
        if data[:2].lower() == "0x":
            data = data[2:]
        if data[:2].lower() == "fc":
            return bytes.fromhex(data)
        try:
            return b64decode(data)
        except Exception:
            return data

    def _mk_command(self, payload):
        """
        parses the command section
        of a SCTE35 cue.
        """
        cmdbb = BitBin(payload)
        bit_start = cmdbb.idx
        self._set_splice_command(cmdbb)
        bit_end = cmdbb.idx
        cmdl = int((bit_start - bit_end) >> 3)
        self.command.splice_command_length = cmdl
        self.info_section.splice_command_length = cmdl
        return payload[cmdl:]

    def _mk_descriptors(self, payload):
        """
        parse descriptor loop length,
        then call Cue._descriptorloop
        """
        dll = ifb(payload[0:2])
        self.info_section.descriptor_loop_length = dll
        payload = payload[2:]
        self._descriptorloop(payload, dll)
        return payload[dll:]

    def mk_info_section(self, payload):
        """
        parses the Splice Info Section
        of a SCTE35 cue.
        """
        info_size = 14
        info_payload = payload[:info_size]
        self.info_section = SpliceInfoSection()
        self.info_section.decode(info_payload)
        return payload[info_size:]

    def _set_splice_command(self, cmdbb):
        """
        Splice Commands looked up in self._command_map
        and decoded.
        """
        sct = self.info_section.splice_command_type
        if sct not in self._command_map:
            to_stderr("Unknown Splice Command Type")
            return False
        self.command = self._command_map[sct]()
        self.command.decode(cmdbb)

    def _set_splice_descriptor(self, payload):
        """
        Splice Descriptor looked up in self._descriptor_map
        and decoded.
        """
        # splice_descriptor_tag 8 uimsbf
        tag = payload[0]
        desc_len = payload[1]
        payload = payload[2:]
        bitbin = BitBin(payload[:desc_len])
        payload = payload[desc_len:]
        if tag in self._descriptor_map:
            spliced = self._descriptor_map[tag](tag)
            spliced.decode(bitbin)
            spliced.descriptor_length = desc_len
            return spliced
        return False

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
