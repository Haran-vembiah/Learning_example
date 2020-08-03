class Sample:
    def sam1(self,a,b):
        return a+b
    def sam2(self,x,y,z):
        valu = Sample.sam1(self,x,y)
        return valu

ss = Sample()
print(ss.sam2(2,3,4))