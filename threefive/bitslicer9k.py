class BitSlicer9k:
    def __init__(self,bites):
        '''
        From bytes to bits
        '''
        if not isinstance(bites,bytes):
            raise TypeError('bites needs to be type bytes')
        self.idx=(len(bites)*8)
        self.bits=int.from_bytes(bites,byteorder='big')
           
    def slice(self,num_bits):
        '''
        Starting at self.bit_idx of self.bits, slice off num_bits of bits.
        ''' 
        bitslice= (self.bits >> (self.idx-num_bits)) & ~(~0 << num_bits)
        self.idx -=num_bits
        return bitslice
        
    def hexed(self,num_bits):
        '''
        return the hex value of a bitslice
        '''
        return hex(self.slice(num_bits))
        
    def boolean(self,num_bits=1):
        '''
        returns one bit as True or False
        '''
        return  self.slice(num_bits) ==1
