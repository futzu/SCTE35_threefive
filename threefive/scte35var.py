class Scte35:
    def __init__(self,bitsize):
        self.bitsize = bitsize
        self.value= None
 
class S3590K(Scte35): 
    def do(self,bitbin):
        self.value=bitbin.as90k(self.bitsize)  


class S35DeHex(Scte35): 
    def do(self,bitbin):
        self.value=bitbin.asdecodedhex(self.bitsize) 

    
class S35Flag: 
    bitsize = 1
    def __init__(self):
        self.value= None      
    
    def do(self,bitbin):
        self.value=bitbin.asflag(self.bitsize)


class S35Hex8:
    bitsize = 8 
    def __init__(self):
        self.value= None
    
    def do(self,bitbin):
        self.value=bitbin.ashex(self.bitsize) 


class S35Hex12(S35Hex8):
    bitsize = 12 


class S35Int2:
    bitsize=2    
    def __init__(self):
        self.value= None
               
    def do(self,bitbin):
        self.value=bitbin.asint(self.bitsize)

        
class S35Int4(S35Int2):
    bitsize=4       


class S35Int6(S35Int2):
    bitsize=6       

        
class S35Int8(S35Int2):
    bitsize=8
    
        
class S35Int10(S35Int2):
    bitsize=10       


class S35Int12(S35Int2):
    bitsize=12      

        
class S35Int16(S35Int2):
    bitsize=16
    
