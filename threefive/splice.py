from base64 import b64decode
from bitn import BitBin
from threefive import (splice_commands as spcmd,
    descriptors as dscprs, splice_info_section as spinfo)


class Splice:
    '''
    the threefive.Splice class handles parsing
    SCTE 35 message strings.
    The data may come as a mpegts packet payload,
    a hex encoded string, or base64 encoded string.
    '''
    # map of known descriptors and associated classes
    descriptor_map = {0: dscprs.Avail_Descriptor,
                      1: dscprs.Dtmf_Descriptor,
                      2: dscprs.Segmentation_Descriptor,
                      3: dscprs.Time_Descriptor,
                      4: dscprs.Audio_Descriptor}
    
    # map of known splice commands and associated classes
    command_map = {0: spcmd.Splice_Null,
                   4: spcmd.Splice_Schedule,
                   5: spcmd.Splice_Insert,
                   6: spcmd.Time_Signal,
                   7: spcmd.Bandwidth_Reservation,
                   255: spcmd.Private_Command}

    def __init__(self, mesg):
        mesg = self.mkbits(mesg)
        self.infobb= BitBin(mesg[:14])
        self.bitbin=BitBin(mesg[14:])
        self.descriptors = []
        self.info_section = None
        self.command = None
        self.do()

    def do(self):
        self.info_section = spinfo.Splice_Info_Section()
        self.info_section.decode(self.infobb)
        self.set_splice_command()
        self.descriptorloop()
        self.info_section.crc = self.bitbin.ashex(32)

    def descriptorloop(self):
        self.info_section.descriptor_loop_length = self.bitbin.asint(16)
        dll = self.info_section.descriptor_loop_length
        tag_plus_header_size = 2  # 1 byte for descriptor_tag, 1 byte for header?
        while dll > 0:
            try:
                sd = self.set_splice_descriptor()
                sdl = sd.descriptor_length
                self.descriptors.append(sd)
            except:
                sdl = 0
            bit_move = sdl + tag_plus_header_size
            dll -= bit_move

    def kvprint(self, obj):
        print(vars(obj))

    def sectionstart(self, section_name):
        print(f'{section_name}')

    def mkbits(self, s):
        '''
        trim, decode, and sanitize
        SCTE 35 messages so
        they can be passed into an
        instance of bitn.BitBin 
        '''
        if s[:2].lower() == '0x':
            s = s[2:]
        if s[:2].lower() == 'fc':
            return bytes.fromhex(s)
        try:
            return b64decode(s)
        except:
            return s

    def set_splice_command(self):
        '''
        splice commands looked up in self.command_map
        '''
        sct = self.info_section.splice_command_type
        if sct not in self.command_map.keys():
            raise ValueError('unknown splice command type')
            return False
        self.command = self.command_map[sct]()
        self.command.decode(self.bitbin)

    def set_splice_descriptor(self):
        '''
        splice descriptors looked up in self.descriptor_map
        '''
        # splice_descriptor_tag 8 uimsbf
        tag = self.bitbin.asint(8)
        if tag in self.descriptor_map.keys():
            return self.descriptor_map[tag](self.bitbin, tag)
        else: return False

    def show_info_section(self):
        if self.info_section:
            self.sectionstart('Splice Info Section')
            self.kvprint(self.info_section)
        else: return False

    def show_command(self):
        if self.command:
            self.sectionstart('Splice Command')
            self.kvprint(self.command)
        else: return False

    def show_descriptors(self):
        if len(self.descriptors) > 0:
            for d in self.descriptors:
                idx = self.descriptors.index(d)
                self.sectionstart(f'Splice Descriptor [ {idx} ]')
                self.kvprint(d)

    def show(self):
        self.show_info_section()
        self.show_command()
        self.show_descriptors()
