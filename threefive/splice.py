from base64 import b64decode
from bitn import BitBin
import json
from threefive.segmentation import SegmentationDescriptor
from threefive.section import SpliceInfoSection
from threefive.descriptor import SpliceDescriptor
from threefive.command import SpliceCommand

class Header:
    def __init__(self,packet_data):
        self.pid = self.pts = None
        if 'pid' in packet_data.keys():
            self.pid = packet_data['pid']
        if 'pts' in packet_data.keys():
            self.pts = packet_data['pts']

    def __repr__(self):
        return str(vars(self))
    

class Splice:
    '''
    The threefive.Splice class handles parsing
    SCTE 35 message strings.
    '''
    # splice descriptor tags
    sd_tags = [0,1,2,3,4]
    # splice command types
    cmd_types = [0,4,5,6,7,255] 

    def __init__(self, data, packet_data={}):
        # clear any existing values.
        self.info_section = self.command = False
        self.descriptors = []
        # split off headers, if any.
        payload = self.mk_payload(data)
        # threefive.Stream passes packet_data. 
        self.bitbin = BitBin(payload)
        self.header = Header(packet_data)
        self.info_section = SpliceInfoSection()
        self.info_section.parse(self.bitbin)
        self.set_command()
        self.info_section.descriptor_loop_length = self.bitbin.asint(16)
        self.descriptorloop()
        self.info_section.crc = hex(int.from_bytes(payload[0:4],
                                            byteorder = 'big'))
                
    def mk_payload(self,data):
        '''
        Splice.mk_payload trims the
        header if data is a full SCTE-35 packet
        '''
        if data[0] == 0x47:
            payload = data[5:]
        else:
            payload = self.mkbits(data)
        return payload
  
    def __repr__(self):
        return str(self.get())
    
    def descriptorloop(self):
        '''
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
        Returns a dict of dicts for all three parts
        of a SCTE 35 message.
        '''
        try:
            scte35 = {}
            scte35['header'] = self.kvclean(vars(self.header))
            scte35['info_section'] = self.kvclean(vars(self.info_section))
            scte35['command'] = self.kvclean(vars(self.command))
            scte35['descriptors'] = [self.kvclean(vars(d)) for d in self.descriptors]

        except:
            scte35 = False
        finally:
            return scte35

    def kvclean(self,obj):
        '''
        kvclean removes items from a dict if the value is None
        '''
        return {k: v for k, v in obj.items() if v is not None}

    def kvprint(self, obj):
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

    def set_command(self):
        '''
        threefive.Splice.set_command
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

        threefive.Splice.set_splice_descriptor
        is called by
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
