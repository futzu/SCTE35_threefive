from base64 import b64decode
import json
import sys
from bitn import BitBin
from threefive.segmentation import Segmentation_Descriptor
from threefive.section import SpliceInfoSection
from threefive.descriptors import (
    Avail_Descriptor,
    Dtmf_Descriptor,
    Time_Descriptor,
    Audio_Descriptor
    )
from threefive.commands import (
    Splice_Null,
    Splice_Schedule,
    Splice_Insert,
    Time_Signal,
    Bandwidth_Reservation,
    Private_Command
    )


def kvclean(obj):
    '''
    kvclean removes items from a dict if the value is None
    '''
    return {k: v for k, v in obj.items() if v is not None}

def kvprint(obj):
    print(json.dumps(obj, indent=2), file=sys.stderr)

def mkbits(s):
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

def mkpayload(data):
    '''
    mkpayload strips off packet headers
    when present
    '''
    if data[0] == 0x47:
        payload = data[5:]
    else:
        payload = mkbits(data)
    return payload


class Cue:
    '''
    The threefive.Splice class handles parsing
    SCTE 35 message strings.
    '''
    # map of known descriptors and associated classes
    descriptor_map = {0: Avail_Descriptor,
                      1: Dtmf_Descriptor,
                      2: Segmentation_Descriptor,
                      3: Time_Descriptor,
                      4: Audio_Descriptor}

    # map of known splice commands and associated classes
    command_map = {0: Splice_Null,
                   4: Splice_Schedule,
                   5: Splice_Insert,
                   6: Time_Signal,
                   7: Bandwidth_Reservation,
                   255: Private_Command}

    def __init__(self, data, packet_data=None):
        self.info_section = None
        self.command = None
        self.descriptors = []
        payload = mkpayload(data)
        self.packet_data = packet_data
        self.parse(payload)

    def parse(self, payload):
        payload = self.mk_info_section(payload)
        payload = self.mk_command(payload)
        payload = self.mk_descriptors(payload)
        self.info_section.crc = hex(int.from_bytes(payload[0:4],
                                                   byteorder='big'))

    def mk_info_section(self, payload):
        info_size = 14
        info_payload = payload[:info_size]
        self.info_section = SpliceInfoSection()
        self.info_section.decode(info_payload)
        return payload[info_size:]

    def mk_command(self, payload):
        cmdbb = BitBin(payload)
        bit_start = cmdbb.idx
        self.set_splice_command(cmdbb)
        bit_end = cmdbb.idx
        cmdl = int((bit_start - bit_end) >>3)
        self.command.splice_command_length = cmdl
        self.info_section.splice_command_length = cmdl
        return payload[cmdl:]

    def mk_descriptors(self, payload):
        dll = int.from_bytes(payload[0:2], byteorder='big')
        self.info_section.descriptor_loop_length = dll
        payload = payload[2:]
        self.descriptorloop(payload, dll)
        return payload[dll:]

    def __repr__(self):
        return str(self.get())

    def descriptorloop(self, payload, dll):
        '''
        parses all splice descriptors
        '''
        while dll > 0:
            try:
                sd = self.set_splice_descriptor(payload)
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
        return kvclean(vars(self.command))

    def get_descriptors(self):
        '''
        Returns a list of SCTE 35
        splice descriptors as dicts.
        '''
        return [kvclean(vars(d)) for d in self.descriptors]

    def get_info_section(self):
        '''
        Returns SCTE 35
        splice info section as a dict
        '''
        return kvclean(vars(self.info_section))

    def get_json(self):
        '''
        Cue.get_json()
        returns Cue.get() as json.
        '''
        return json.dumps(self.get(), indent=2)

    def get_packet_data(self):
        return kvclean(self.packet_data)

    def set_splice_command(self, cmdbb):
        '''
        Splice Commands looked up in self.command_map
        '''
        sct = self.info_section.splice_command_type
        if sct not in self.command_map.keys():
            print('Unknown Splice Command Type', file=sys.stderr)
            return False
        self.command = self.command_map[sct]()
        self.command.decode(cmdbb)

    def set_splice_descriptor(self, payload):
        '''
        Splice Descriptors looked up in self.descriptor_map
        '''
        # splice_descriptor_tag 8 uimsbf
        tag = payload[0]
        desc_len = payload[1]
        payload = payload[2:]
        bitbin = BitBin(payload[:desc_len])
        payload = payload[desc_len:]
        if tag in self.descriptor_map.keys():
            sd = self.descriptor_map[tag](bitbin, tag)
            sd.descriptor_length = desc_len
            return sd
        return False

    def show(self):
        '''
        pretty prints the SCTE 35 message
        '''
        kvprint(self.get())
