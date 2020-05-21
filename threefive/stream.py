from .splice import Splice

class Stream:
    '''
    Parse mpegts files and streams for SCTE 35 packets
    '''
    PACKET_SIZE = 188
    PACKET_COUNT = 256
    TID = 0xfc # SCTE 35 Table id
    RES = 0x3 # Reserved value in Splice.info_section
    PROTO = 0x0 # Protocol value in Splice,info_section
    cmd_types = [4,5,6,7,255] # SCTE 35 splice command types

    def __init__(self,tsdata, show_null = False):
        if show_null:
            cmd_types.append(0) 
        self.tsdata = tsdata
        
    def decode(self):
        '''
        split data into
        chunks of 188 byte packets
        '''
        while self.tsdata:
            chunky = self.tsdata.read(self.PACKET_SIZE * self.PACKET_COUNT)
            if not chunky: break
            self.packets = [chunky[i:i+self.PACKET_SIZE]
                     for i in range(0, len(chunky), self.PACKET_SIZE)]
            self.parse_packets()

    def chk_tid(self,pkt):
        '''
        SCTE 35 packets
        require a table Id of 0xfc
        '''
        return pkt[5] == self.TID
    
    def chk_res(self,ten):
        if ten[6] >> 4 ==self.RES:
            return self.chk_proto(ten[8])
        return False

    def chk_proto(self,eight):
        return eight == self.PROTO

    def chk_type(self,pkt):
        if self.chk_res(pkt[:10]):
            return  pkt[18] in self.cmd_types
    

    def scte35_packets(self):
        good =filter(self.chk_type,filter(self.chk_tid,self.packets))
        [Splice(packet).show() for packet in good]
    						
    def parse_packets(self):
        self.scte35_packets()
    	    
