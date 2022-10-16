import TNormal

class Cara:
    
    a=0
    b=0
    c=0
    normal=TNormal.TNormal()

    #normal=None es que este parámetro es opcional
    def __init__(self, vA, vB, vC, normal=None):
        self.a=vA
        self.b=vB
        self.c=vC
        self.normal=normal

    def getA(self):
        return self.a
    
    def setA(self,a):
        self.a=a

    def getB(self):
        return self.b
    
    def setB(self,b):
        self.b=b

    def getC(self):
        return self.c
    
    def setC(self,c):
        self.c=c

    def getNormal(self):
        return self.normal
    
    def setNormal(self,normal):
        self.normal=normal