from threefive import Splice

class FastStream:
    '''
    Parse mpegts files and streams for SCTE 35 packets
    '''
    SYNC_BYTE = 0x47
    SCTE35_TID = 0xfc

    def __init__(self, tsdata, show_null = False):
        self.show_null = show_null
        self.parse_tsdata(tsdata)

    def parse_tsdata(self, tsdata):
        '''
         split tsdata into packets for parsing
        '''
        while tsdata:
            packet=tsdata.read(188)
            if not packet: break
            self.parse_tspacket(packet)
        return
  
    def parse_payload(self,payload):
        '''
        If you want to customize output,
        subclass Stream and change this method.
        '''
        try:
            tf = Splice(payload)
            tf.show()
        except: pass
        
    def parse_tspacket(self, packet):
        '''
        parse a mpegts packet for SCTE 35 and/or PTS
        '''
        if packet[0] != self.SYNC_BYTE: return
        if packet[5] != self.SCTE35_TID : return
        if not self.show_null:
            if packet[18] == 0: return
        self.parse_payload(packet[5:])
        return
