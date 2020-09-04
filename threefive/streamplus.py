from bitn import BitBin
from .splice import Splice
from .stream import Stream


class StreamPlus(Stream):
    '''
    StreamPlus adds PID and PTS for the SCTE 35 packets
    to the Stream class.
    '''
    NON_PTS_STREAM_IDS = [188, 190, 191, 240, 241, 242, 248]

    def __init__(self, tsdata, show_null = False):
        self.PTS = False
        super().__init__(tsdata,show_null)

    def parse_pts(self,bitbin):
        '''
        This is the process described in the official
        Mpeg-ts specification.
        '''
        a = bitbin.asint(3) << 30
        bitbin.forward(1)           
        b = bitbin.asint(15) << 15
        bitbin.forward(1)          
        c = bitbin.asint(15)
        d = (a+b+c)/90000.0
        # self.PTS is updated when we find a pts.
        self.PTS=round(d,6)
    
    def parse_pusi(self, packetdata):
        '''
        If the pusi data contains these markers,
        we can pull a PTS value..
        '''
        if packetdata[2] == 1: 
            if packetdata[3] not in self.NON_PTS_STREAM_IDS:  
                if (packetdata[6] >> 6) == 2: 
                    if (packetdata[7] >> 6) == 2:
                        if (packetdata[9] >> 4) == 2: 
                            bitbin = BitBin(packetdata[9:])
                            bitbin.forward(4)
                            self.parse_pts(bitbin)

    def parse_packet(self,packet):
        two_bytes = int.from_bytes(packet[1:3],byteorder='big')
        pid = hex(two_bytes & 0x1fff)
        if (two_bytes >> 14 & 0x1):
            self.parse_pusi(packet[4:20])
        if self.chk_magic(packet[:20]):
            packet_data = {'pid':pid,'pts':self.PTS}
            tf = Splice(packet,packet_data)
            tf.show()

    def parse_packet_return(self, packet):
        two_bytes = int.from_bytes(packet[1:3],byteorder='big')
        pid = hex(two_bytes & 0x1fff)
        if (two_bytes >> 14 & 0x1):
            self.parse_pusi(packet[4:20])
        if self.chk_magic(packet[:20]):
            packet_data = {'pid':pid,'pts':self.PTS}
            tf = Splice(packet,packet_data)
            return tf.get()
    
    def parse(self,packets):
        [self.parse_packet(packet) for packet in packets]

    def parse_return(self,packets):
        return [self.parse_packet_return(packet) for packet in packets]

    def decode_until_found(self):
        '''
        Split data into 188 byte packets
        '''
        pkt_sz = 188  # mpegts packet size
        pkt_ct = 384 # packet count
        chunk_sz = pkt_sz * pkt_ct
        while self.tsdata:
            first_byte = self.tsdata.read(1)
            if not first_byte: break
            if first_byte == self.sync_byte:
                chunk = first_byte + self.tsdata.read(chunk_sz -1)
                if not chunk: break
                parsed_packets = self.parse_return([chunk[i:i+pkt_sz]
                        for i in range(0,len(chunk),pkt_sz)])
                filtered_packets = list(filter(lambda var: var is not None, parsed_packets))
                if filtered_packets:
                    return filtered_packets
