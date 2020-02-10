class Scte35:
    bitsize = 0
    def __init__(self):
        self.value= None
 
class t90K33(Scte35):
    bitsize = 33 
    def do(self,bitbin):
        self.value=bitbin.as90k(self.bitsize)  


class DeHexed(Scte35):
    bitsize = 0 
    def do(self,bitbin):
        self.value=bitbin.asdecodedhex(self.bitsize) 

    
class Flag: 
    bitsize = 1
    def do(self,bitbin):
        self.value=bitbin.asflag(self.bitsize)


class Hexed(Scte35):
    bitsize = 1 
    def do(self,bitbin):
        self.value=bitbin.ashex(self.bitsize) 


class Hexed2(Hexed):
    bitsize = 2 

class Hexed8(Hexed):
    bitsize = 8 


class Hexed12(Hexed):
    bitsize = 12 


class Hexed32(Hexed):
    bitsize = 32 

class Hexed64(Hexed):
    bitsize = 64

class uInt(Scte35):
   bitsize = 1               
   def do(self,bitbin):
        self.value=bitbin.asint(self.bitsize)


class uInt2(uInt):
    bitsize=2    
 

class uInt3(uInt):
    bitsize=3       

        
class uInt4(uInt):
    bitsize=4       

class uInt5(uInt):
    bitsize=5       

class uInt6(uInt):
    bitsize=6       

class uInt7(uInt):
    bitsize=7       


class uInt8(uInt):
    bitsize=8
    
        
class uInt10(uInt):
    bitsize=10       


class uInt12(uInt):
    bitsize=12      


class uInt13(uInt):
    bitsize=13
    
           
class uInt16(uInt):
    bitsize=16
    

class uInt32(uInt):
    bitsize=32