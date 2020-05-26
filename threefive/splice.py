from base64 import b64decode
from bitn import BitBin
import json
from threefive.segmentation import Segmentation_Descriptor
from threefive.splice_info_section import Splice_Info_Section
from threefive.descriptors import (
    Avail_Descriptor,
    Dtmf_Descriptor,
    Time_Descriptor,
    Audio_Descriptor
    )
from threefive.splice_commands import (
    Splice_Null,
    Splice_Schedule,
    Splice_Insert,
    Time_Signal,
    Bandwidth_Reservation,
    Private_Command 
    )


class Splice:
    '''
    The threefive.Splice class handles parsing
    SCTE 35 message strings.
    '''
    # map of known descriptors and associated classes
    descriptor_map = { 0: Avail_Descriptor,
                       1: Dtmf_Descriptor,
                       2: Segmentation_Descriptor,
                       3: Time_Descriptor,
                       4: Audio_Descriptor }

    # map of known splice commands and associated classes
    command_map = { 0: Splice_Null,
                    4: Splice_Schedule,
                    5: Splice_Insert,
                    6: Time_Signal,
                    7: Bandwidth_Reservation,
                  255: Private_Command }

    def __init__(self, data, packet_data=None):
        payload = self.mk_payload(data)
        self.packet_data = packet_data
        self.decode(payload)
 
    def decode(self,payload):
        payload = self.mk_info_section(payload)
        payload = self.mk_command(payload)
        payload = self.mk_descriptors(payload)
        self.info_section.crc = hex(int.from_bytes(payload[0:4],
                                             byteorder = 'big'))
        
    def mk_payload(self,data):
        if data[0] == 0x47:
            payload = data[5:]
        else:
            payload = self.mkbits(data)  
        return payload

    def mk_info_section(self,payload):
        info_size = 14
        info_payload = payload[:info_size]
        self.info_section = Splice_Info_Section()
        self.info_section.decode(info_payload)
        return payload[info_size:]

    def mk_command(self,payload):
        cmdl = self.info_section.splice_command_length
        # fix for bad self.info_section.splice_command_length
        cmdbb = BitBin(payload)
        self.set_splice_command(cmdbb)
        cmdl = self.info_section.splice_command_length = self.command.splice_command_length
        return payload[cmdl:]

    def mk_descriptors(self,payload):
        self.descriptors = []
        dll = self.info_section.descriptor_loop_length = int.from_bytes(payload[0:2],byteorder = 'big')
        payload = payload[2:]
        self.descriptorloop(payload,dll)
        return payload[dll:]
        
    def __repr__(self):
        return str(self.get())

    def descriptorloop(self,payload,dll):
        '''
        parses all splice descriptors
        '''
        while dll > 0:
            try:
                sd = self.set_splice_descriptor(payload)
                sdl = sd.descriptor_length
                dll-= sdl+2
                payload = payload[sdl+2:]
                self.descriptors.append(sd)
            except:
                dll = -1

    def get(self):
        '''
        Returns a dict of dicts for all three parts
        of a SCTE 35 message.
        '''
        scte35 = {  'info_section':self.get_info_section(),
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
        return self.kvclean(vars(self.command))

    def get_descriptors(self):
        '''
        Returns a list of SCTE 35
        splice descriptors as dicts.
        '''
        return [self.kvclean(vars(d)) for d in self.descriptors]
    
    def get_info_section(self):
        '''
        Returns SCTE 35
        splice info section as a dict
        '''
        return self.kvclean(vars(self.info_section))

    def get_packet_data(self):
        return self.kvclean(self.packet_data)

    def kvclean(self,obj):
        '''
        kvclean removes items from a dict if the value is None
        '''
        return {k: v for k, v in obj.items() if v is not None}

    def kvprint(self, obj):
        print('\n')
        print(json.dumps(obj,indent = 2))

    def mkbits(self, s):
        '''
        Convert Hex and Base64 strings into bytes.
        '''
        if s[:2].lower() == '0x':
            s = s[2:]
        if s[:2].lower() == 'fc':
            return bytes.fromhex(s)
        try:
            return b64decode(s)
        except:
            return s

    def set_splice_command(self,cmdbb):
        '''
        Splice Commands looked up in self.command_map
        '''
        sct = self.info_section.splice_command_type
        if sct not in self.command_map.keys():
            raise ValueError('Unknown Splice Command Type')
            return False
        self.command = self.command_map[sct]()
        self.command.decode(cmdbb)

    def set_splice_descriptor(self,payload):
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
            sd = self.descriptor_map[tag](bitbin,tag)
            sd.descriptor_length = desc_len
            return sd
        else:
            return False

    def show(self):
        '''
        pretty prints the SCTE 35 message
        '''
        self.kvprint(self.get())

    def show_command(self):
        '''
        pretty prints SCTE 35 splice command
        '''
        self.kvprint(self.get_command())

    def show_descriptors(self):
        '''
        pretty prints SCTE 35 splice descriptors
        '''
        self.kvprint(self.get_descriptors())

    def show_info_section(self):
        '''
        pretty prints SCTE 35 splice info section
        '''
        self.kvprint(self.get_info_section())
