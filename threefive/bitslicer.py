
class BitSlicer:
    def __init__(self,data):
        self.data=data
        self.bit_idx=(len(self.data)*8)-1
     
        
    def slice(self,num_bits):
        pre=self.data
        if type(pre) == bytes: pre=int.from_bytes(pre,byteorder='big')
        bitslice= (pre >> (self.bit_idx+1-num_bits)) & ~(~0 << num_bits)
        self.bit_idx -=num_bits
        return bitslice
        
    def hexed(self,num_bits):
        return hex(self.slice(num_bits))
            
    def boolean(self,num_bits=1):
        return  self.slice(num_bits) ==1
