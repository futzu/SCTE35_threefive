class Scte35:
    def __init__(self,bitsize):
        self.bitsize = bitsize
        self.valu = None

 
class S3590K(Scte35): 
    def do(self,bitbin):
        self.value = bitbin.as90k(self.bitsize)  


class S35DeHex(Scte35): 
    def do(self,bitbin):
        self.value = bitbin.asdecodedhex(self.bitsize) 

    
class S35Flag(Scte35):       
    def do(self,bitbin):
        self.value = bitbin.asflag(self.bitsize)


class S35Hex(Scte35): 
    def do(self,bitbin):
        self.value = bitbin.ashex(self.bitsize) 

      
class S35Int(Scte35):       
    def do(self,bitbin):
        self.value = bitbin.asint(self.bitsize)
