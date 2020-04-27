from base64 import b64decode
from bitn import BitBin
import json
import pprint
from threefive import (
    descriptors as dscprs,
    splice_info_section as spinfo,
    splice_commands as spcmd)


class Splice:
    '''
    The threefive.Splice class handles parsing
    SCTE 35 message strings.
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

    def __init__(self, mesg,pid=False,pts=False):
        mesg = self.mkbits(mesg)
        self.pid = pid
        self.pts = pts
        self.infobb= BitBin(mesg[:14])
        self.bitbin=BitBin(mesg[14:])
        self.descriptors = []
        self.info_section = None
        self.command = None
        self.do()

    def __repr__(self):
        return str(self.get())

    def do(self):
        '''
        called by __init__ to parse SCTE 35 data
        '''
        self.info_section = spinfo.Splice_Info_Section()
        self.info_section.decode(self.infobb)
        self.set_splice_command()
        self.descriptorloop()
        self.info_section.crc = self.bitbin.ashex(32)

    def descriptorloop(self):
        '''
        parses all splice descriptors
        '''
        self.info_section.descriptor_loop_length = self.bitbin.asint(16)
        dll = self.info_section.descriptor_loop_length
        d_tag = 1  # 1 byte for descriptor_tag
        while dll > 4:
            try:
                sd = self.set_splice_descriptor()
                sdl = sd.descriptor_length
                self.descriptors.append(sd)
            except:
                break
            bit_move = sdl + d_tag
            dll -= bit_move

    def get(self,obj=False):
        '''
        returns obj as dict. if obj is False,
        Returns a dict of dicts for all three parts
        of a SCTE 35 message.
        '''
        if not obj:
            scte35 = {'Info_Section' : vars(self.info_section),
                    'Splice_Command': vars(self.command),
                    'Splice_Descriptors': self.list_descriptors()}
            if self.pid or self.pts:
                packet = {}
                if self.pid: packet['pid'] = hex(self.pid)
                if self.pts: packet['pts'] = self.pts
                scte35['Packet'] = packet
        else:
            scte35 = vars(obj)
        return scte35    

    def get_command(self):
        '''
        returns the SCTE 35
        splice command data as a dict.
        '''  
        return self.get(self.command)

    def get_descriptors(self):
        '''
        Returns a list of SCTE 35
        splice descriptors as dicts.
        '''
        return self.list_descriptors()
     
    def get_info_section(self):
        '''
        Returns SCTE 35
        splice info section as a dict
        '''
        return self.get(self.info_section)

    def kvprint(self, obj):
        pprint.pprint(obj,width=30,indent=2)

    def list_descriptors(self):
        '''
        returns SCTE 35 splice descriptors in list
        '''
        return [vars(d) for d in self.descriptors]

    def mkbits(self, s):
        '''
        Convert Hex and Base64 strings into bytes.
        '''
        if s[:2].lower() == '0x': s = s[2:]
        if s[:2].lower() == 'fc': return bytes.fromhex(s)
        try: return b64decode(s)
        except: return s

    def set_splice_command(self):
        '''
        Splice Commands looked up in self.command_map
        '''
        sct = self.info_section.splice_command_type
        if sct not in self.command_map.keys():
            raise ValueError('Unknown Splice Command Type')
            return False
        self.command = self.command_map[sct]()
        self.command.decode(self.bitbin)

    def set_splice_descriptor(self):
        '''
        Splice Descriptors looked up in self.descriptor_map
        '''
        # splice_descriptor_tag 8 uimsbf
        tag = self.bitbin.asint(8)
        if tag in self.descriptor_map.keys():
            return self.descriptor_map[tag](self.bitbin, tag)
        else: return False

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
