from base64 import b64decode
import json
import sys
from bitn import BitBin
from threefive.segmentation import SegmentationDescriptor
from threefive.section import SpliceInfoSection
from threefive.descriptors import (
    AvailDescriptor,
    DtmfDescriptor,
    TimeDescriptor,
    AudioDescriptor
    )
from threefive.commands import (
    SpliceNull,
    SpliceSchedule,
    SpliceInsert,
    TimeSignal,
    BandwidthReservation,
    PrivateCommand
    )


def _kvclean(obj):
    '''
    _kvclean removes items from a dict if the value is None
    '''
    return {k: v for k, v in obj.items() if v is not None}

def _kvprint(obj):
    print(json.dumps(obj, indent=2), file=sys.stderr)

def _mkbits(s):
    '''
    Convert Hex and Base64 strings into bytes.
    '''
    if s[:2].lower() == '0x':
        s = s[2:]
    if s[:2].lower() == 'fc':
        return bytes.fromhex(s)
    try:
        return b64decode(s)
    except Exception:
        return s

def _mkpayload(data):
    '''
    mkpayload strips off packet headers
    when present
    '''
    if data[0] == 0x47:
        payload = data[5:]
    else:
        payload = _mkbits(data)
    return payload


class Cue:
    '''
    The threefive.Splice class handles parsing
    SCTE 35 message strings.
    '''
    # map of known descriptors and associated classes
    _descriptor_map = {0: AvailDescriptor,
                       1: DtmfDescriptor,
                       2: SegmentationDescriptor,
                       3: TimeDescriptor,
                       4: AudioDescriptor}

    # map of known splice commands and associated classes
    _command_map = {0: SpliceNull,
                    4: SpliceSchedule,
                    5: SpliceInsert,
                    6: TimeSignal,
                    7: BandwidthReservation,
                    255: PrivateCommand}

    def __init__(self, data, packet_data=None):
        self.info_section = None
        self.command = None
        self.descriptors = []
        payload = _mkpayload(data)
        self.packet_data = packet_data
        self._parse(payload)

    def _parse(self, payload):
        payload = self._mk_info_section(payload)
        payload = self._mk_command(payload)
        payload = self._mk_descriptors(payload)
        self.info_section.crc = hex(int.from_bytes(payload[0:4],
                                                   byteorder='big'))

    def _mk_info_section(self, payload):
        info_size = 14
        info_payload = payload[:info_size]
        self.info_section = SpliceInfoSection()
        self.info_section.decode(info_payload)
        return payload[info_size:]

    def _mk_command(self, payload):
        cmdbb = BitBin(payload)
        bit_start = cmdbb.idx
        self._set_splice_command(cmdbb)
        bit_end = cmdbb.idx
        cmdl = int((bit_start - bit_end) >>3)
        self.command.splice_command_length = cmdl
        self.info_section.splice_command_length = cmdl
        return payload[cmdl:]

    def _mk_descriptors(self, payload):
        '''
        parse descriptor loop length,
        then call Cue._descriptorloop
        '''
        dll = int.from_bytes(payload[0:2], byteorder='big')
        self.info_section.descriptor_loop_length = dll
        payload = payload[2:]
        self._descriptorloop(payload, dll)
        return payload[dll:]

    def __repr__(self):
        return str(self.get())

    def _descriptorloop(self, payload, dll):
        '''
        parses all splice descriptors
        '''
        while dll > 0:
            try:
                sd = self._set_splice_descriptor(payload)
                sdl = sd.descriptor_length
                bump = sdl + 2
                dll -= bump
                payload = payload[bump:]
                self.descriptors.append(sd)
            except:
                dll = -1

    def get(self):
        '''
        Returns a dict of dicts for all three parts
        of a SCTE 35 message.
        '''
        scte35 = {'info_section':self.get_info_section(),
                  'command':self.get_command(),
                  'descriptors':self.get_descriptors()}

        if self.packet_data:
            scte35.update(self.get_packet_data())
        return scte35

    def get_command(self):
        '''
        returns the SCTE 35
        splice command data as a dict.
        '''
        return _kvclean(vars(self.command))

    def get_descriptors(self):
        '''
        Returns a list of SCTE 35
        splice descriptors as dicts.
        '''
        return [_kvclean(vars(d)) for d in self.descriptors]

    def get_info_section(self):
        '''
        Returns SCTE 35
        splice info section as a dict
        '''
        return _kvclean(vars(self.info_section))

    def get_json(self):
        '''
        Cue.get_json()
        returns Cue.get() as json.
        '''
        return json.dumps(self.get(), indent=2)

    def get_packet_data(self):
        '''
        returns cleaned Cue.packet_data
        '''
        return _kvclean(self.packet_data)

    def _set_splice_command(self, cmdbb):
        '''
        Splice Commands looked up in self._command_map
        '''
        sct = self.info_section.splice_command_type
        if sct not in self._command_map.keys():
            print('Unknown Splice Command Type', file=sys.stderr)
            return False
        self.command = self._command_map[sct]()
        self.command.decode(cmdbb)

    def _set_splice_descriptor(self, payload):
        '''
        Splice Descriptors looked up in self._descriptor_map
        '''
        # splice_descriptor_tag 8 uimsbf
        tag = payload[0]
        desc_len = payload[1]
        payload = payload[2:]
        bitbin = BitBin(payload[:desc_len])
        payload = payload[desc_len:]
        if tag in self._descriptor_map.keys():
            sd = self._descriptor_map[tag](tag)
            sd.decode(bitbin)
            sd.descriptor_length = desc_len
            return sd
        return False

    def show(self):
        '''
        pretty prints the SCTE 35 message
        '''
        _kvprint(self.get())
