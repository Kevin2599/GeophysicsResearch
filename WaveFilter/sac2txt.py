# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 19:26:51 2017

@author: LLL
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 16:39:10 2016
@author: Cangye
"""

#SAC File Read



import struct
class SacStreamIO():
    def __init__(self,fileName,mode="rb"):
        self.HRN=0
        self.GDN=0
        self.file=open(fileName,mode)
        if(mode=="rb"):
            self.ReadHead()
            self.ReadData()
            self.file.close()
        
    def WriteHead(self,npts):
        self.fileHeadB=[0.009999999776482582, -399.86651611328125, 424.1824951171875, -12345.0, -12345.0, 9670.0, 9700.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, 31.569414138793945, 103.42683410644531, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, 0.3598167896270752, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, -12345.0, 2015, 324, 0, 0, 0, 0, 6, -12345, -12345, 3001, -12345, -12345, -12345, -12345, -12345, 1, -12345, -12345, -12345, -12345, -12345, -12345, -12345, -12345, -12345, -12345, -12345, -12345, -12345, -12345, -12345, -12345, -12345, -12345, -12345, 1, 1, 1, 1, 0, 2314885531121513587, 2314908706781933869, 2314885530818453536, 2314908706781933869, 2314908706781933869, 2314908706781933869, 2314908706781933869, 2314908706781933869, 2314908706781933869, 2314908706781933869, 2314908706781933869, 2314908706781933869, 2314908706781933869, 2314908706781933869, 2314908706781933869, 2314908706781933869, 2314908706781933869, 2314908706781933869, 2314908706781933869, 2314908706781933869, 2314885530818453594, 236111107967183, 2314908706781933869, 2314908706781933869]
        self.file.seek(0,0)
        self.npts=self.fileHeadB[79]=npts
        outhead=struct.pack('<70f40i24q',tuple(self.fileHeadB))
        self.file.write(outhead)
    def WriteData(self,data):
        outdata=tuple(data)
        xVect=struct.pack('<'+str(self.npts)+'f',outdata)
        self.file.write(xVect)
    def CleanFile(self):
        self.file.close()
    def ReadHead(self):
        self.file.seek(0,0)
        self.fileHeadB=self.file.read(632)
        out=self.head=struct.unpack('<70f40i24q',self.fileHeadB)
        self.b=out[5]
        self.e=out[6]
        self.delta=out[0]
        self.npts=out[79]
        self.leven=out[105]
        self.nxsize=out[82]
        self.nysize=out[83]
        self.year=out[70]
        self.day=out[70] 
        self.HRN=1
        self.lat=out[31]
        self.lon=out[32]
    def ReadData(self):
        if(self.GDN==1):
            print('Data has read twice!')
            return
        import numpy as np
        if(self.leven==1):
            dataBy=self.file.read(4*self.npts)
            self.yVect=np.array(struct.unpack('<'+str(self.npts)+'f',dataBy))
            self.xVect=np.linspace(0,self.npts*self.delta,self.npts)
        elif(self.leven==0):
            dataBx=self.file.read(4*self.npts)
            dataBy=self.file.read(4*self.npts)
            self.xVect=np.array(struct.unpack('<'+str(self.npts)+'f',dataBx))
            self.yVect=np.array(struct.unpack('<'+str(self.npts)+'f',dataBy))
        self.GDN=1
    def DataDetrend(self):
        import scipy.signal as ssg
        self.yVect=ssg.detrend(self.yVect)
    def ViewHeadData(self):
        for ii in range(14):
            ii5=ii*5
            print("Line %2d :%16.3f %16.3f %16.3f %16.3f %16.3f"%(ii,self.head[ii5],self.head[ii5+1],self.head[ii5+2],self.head[ii5+3],self.head[ii5+4]))
        for ii in range(14,24):
            ii5=ii*5
            print("Line %2d :%16d %16d %16d %16d %16d"%(ii,self.head[ii5],self.head[ii5+1],self.head[ii5+2],self.head[ii5+3],self.head[ii5+4]))
        for ii in range(24,32):
            ii5=ii*3
            print("Line %2d :%16d %16d %16d"%(ii,self.head[ii5],self.head[ii5+1],self.head[ii5+2]))
    def ViewData(self):
        print("%10.3f %10.3f %10.3f\n...(%d dots)...\n%10.3f %10.3f %10.3f"%(self.yVect[0],self.yVect[1],self.yVect[2],self.npts,self.yVect[-3],self.yVect[-2],self.yVect[-1]))


        
if __name__ == '__main__':
    fileName=input("sac file name:")
    fileName="no_data0.sac"
    file=SacStreamIO(fileName,"rb") 
    out=open(fileName+".txt","w")
    for itr in range(len(file.xVect)):
        out.write(str(file.xVect[itr])+"\n")

        
        
        
        
        
        
        
        
        
        
        
        
    