import json

from base64 import b64decode
from bitn import BitBin
from threefive.command import SpliceCommand
from threefive.descriptor import SpliceDescriptor
from threefive.section import SpliceInfoSection
from threefive.segmentation import SegmentationDescriptor


class Cue:
    '''
    The threefive.Cue class handles parsing
    SCTE 35 message strings.
    '''
    # splice descriptor tags
    sd_tags = [0,1,2,3,4]
    # splice command types
    cmd_types = [0,4,5,6,7,255] 

    def __init__(self, data, packet_data={}):
        self.info_section = self.command = False
        self.descriptors = []
        # split off headers, if any.
        payload = self.mk_payload(data)
        # threefive.Stream passes packet_data.
        self.packet_data = packet_data
        self.bitbin = BitBin(payload)
        self.info_section = SpliceInfoSection()
        self.info_section.parse(self.bitbin)
        self.set_command()
        self.info_section.descriptor_loop_length = self.bitbin.asint(16)
        self.descriptor_loop()
        self.info_section.crc = hex(int.from_bytes(payload[0:4],
                                            byteorder = 'big'))
                
    def __repr__(self):
        return str(self.get())
    
    def descriptor_loop(self):
        '''
        Cue.descriptor_loop 
        parses all splice descriptors
        '''
        dll = self.info_section.descriptor_loop_length
        while dll > 0:
            try:
                sd = self.set_splice_descriptor()
                sdl = sd.descriptor_length
                dll-= sdl+2
                self.descriptors.append(sd)
            except:
                dll = -1

    def get(self):
        '''
        Returns a dict of 
        the SCTE 35 message data.
        '''
        scte35 = {}
        if len(self.packet_data.keys()) > 0:
            scte35['packet_data'] = self.kv_clean(self.packet_data)
        scte35['info_section'] = self.get_info_section()
        scte35['command'] = self.get_command()
        if len(self.descriptors)  > 0:
                scte35['descriptors'] = self.get_descriptors()
        return scte35

    def get_command(self):
        return self.kv_clean(vars(self.command))

    def get_descriptors(self):
        return [self.kv_clean(vars(d)) for d in self.descriptors]

    def get_info_section(self):
        return self.kv_clean(vars(self.info_section))       
    
    def kv_clean(self,obj):
        '''
        kv_clean removes items from a dict if the value is None
        '''
        return {k: v for k, v in obj.items() if v is not None}

    def kv_print(self, obj):
        print(json.dumps(obj,indent = 2))

    def mk_bits(self, s):
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
        
    def mk_payload(self,data):
        '''
        Cue.mk_payload trims the packet
        header if data is a full SCTE-35 packet
        '''
        if data[0] == 0x47:
            payload = data[5:]
        else:
            payload = self.mk_bits(data)
        return payload
    
    def set_command(self):
        '''
        threefive.Cue.set_command
        checks the command type and if valid,
        the splice command data is parsed.
        '''
        sct = self.info_section.splice_command_type
        if sct not in self.cmd_types:
            raise ValueError('Unknown Splice Command Type')
            return False
        self.command = SpliceCommand()
        self.command.parse(sct,self.bitbin)

    def set_splice_descriptor(self):
        '''

        threefive.Cue.set_splice_descriptor
        is called by threefive.Cue.descriptorloop.
        '''
        # splice_descriptor_tag 8 uimsbf
        tag = self.bitbin.asint(8)
        desc_len = self.bitbin.asint(8)
        if tag in self.sd_tags:
            if tag == 2:
                sd = SegmentationDescriptor()
            else:
                sd = SpliceDescriptor()
            sd.parse(self.bitbin,tag)
            sd.descriptor_length = desc_len
            return sd
        else:
            return False

    def show(self):
        '''
        pretty prints the SCTE 35 message
        '''
        self.kv_print(self.get())

    def show_command(self):
        '''
        pretty prints SCTE 35 splice command
        '''
        self.kv_print(self.get_command())

    def show_descriptors(self):
        '''
        pretty prints SCTE 35 splice descriptors
        '''
        self.kv_print(self.get_descriptors())

    def show_info_section(self):
        '''
        pretty prints SCTE 35 splice info section
        '''
        self.kv_print(self.get_info_section())
