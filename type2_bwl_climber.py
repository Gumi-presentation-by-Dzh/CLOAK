#coding:utf-8
import random
import numpy as np
import defenselayer_bwl_climber as dl 
import sys
##############################
##############################
tracepath = 'trace.dat'
endstatpath = 'endstat.dat'
logpath = 'log.dat'
endlifepath = 'endlife.dat'
initlifepath = 'initlife.dat'
areashift = 0 
maxpagenums = (4194304>>2) >> areashift 
isbreak = 0
attacktype = 2
filelength = 0
pageshift = 12
attackpp = 1
endnums = 200001000
climbershift = 17
attacksize = 1
##########################################################
class AcListGenerator:
    def __init__(self, type1, areasize, attackpp,randomenable, reverseenable, stallenable):
        if areasize <= 2:
            print('error:memorysize too small')
        self.type = type1
        self.areasize = areasize
        self.attackpp = attackpp
        self.maplist = [0 for x in range(self.areasize)]
        self.revlist = [0 for x in range(self.areasize)]
        self.flag = 0
        self.index = 0
        self.round = 0
        self.count = 0
        self.cycles = 10
        self.hot = 1000000
        self.d1 = dl.DefenseLayer(self.areasize, self.type,randomenable, reverseenable, stallenable,climbershift)
        self.writelist = [-1 for x in range(self.areasize + 10)]
        self.writelistp = 0
        self.writelist2p = 0
        self.coldpoint = self.areasize
        print("map begin")
        for i in range(self.areasize):
            self.maplist[i] = i
            self.revlist[i] = i
        print("map end")
        self.visittable = [[0,0] for y in range(self.areasize)]
        for i in range(self.areasize):
            self.visittable[i][0] = i
    def attackp(self):
        rn = random.random()
        if rn > self.attackpp:
            return 0
        else:
            return 1
    def getindex(self, addr_temp):
        raddr = 0
        if self.writelist2p != self.writelistp:
            raddr = self.writelist[self.writelist2p]
            self.writelist2p = self.writelist2p + 1
            if self.writelist2p == self.writelistp:
                self.writelist2p = 0
                self.writelistp = 0
            return raddr
        return self.maplist[addr_temp]
    def gethotgroup(self,sortedlist):
        ans = -1
        return ans
    def gethotaddr(self,hotgroup,sortedlist):
        ans = sortedlist[-1][0]
        return ans
    def getcoldaddr(self,hotgroup,sortedlist):
        #i = 0
        for i in range(len(sortedlist)):
            if sortedlist[len(sortedlist) - 1 - i][1] == 0:
                return (sortedlist[len(sortedlist) - 1 - i][0],len(sortedlist) - 1 - i)
        return (sortedlist[0][0],0)

    def dowhenswap(self, memorystat):
        if memorystat[0] == 1:
            self.cycles = self.cycles - 1
            if self.attackp() == 1:#
                sortedlist =sorted(self.visittable, key = lambda x:x[1])
                hotaddr = self.gethotaddr(-1,sortedlist)
                coldaddrpair = self.getcoldaddr(-1,sortedlist)
                print('attackaddr:%d'%(coldaddrpair[0]))
                for i in range(attacksize):
                    hotaddr = sortedlist[-1-i][0]
                    if coldaddrpair[1] - i >= 0:
                        coldaddr = sortedlist[coldaddrpair[1] - i][0]
                    else:
                        coldaddr = sortedlist[i][0]
                    self.maplist[self.revlist[coldaddr]] = hotaddr
                    self.writelist[self.writelistp] = hotaddr
                    self.writelistp = self.writelistp + 1
                    self.maplist[self.revlist[hotaddr]] = coldaddr
                    self.writelist[self.writelistp] = coldaddr
                    self.writelistp = self.writelistp + 1
                    if self.writelistp > self.areasize + 10:
                        print('error in writelist')
                    swap_temp = self.revlist[hotaddr]
                    self.revlist[hotaddr] = self.revlist[coldaddr]
                    self.revlist[coldaddr] = swap_temp
            for i in range(len(self.visittable)):
                self.visittable[i][1] = 0
            self.coldpoint = self.areasize
                
with open(tracepath) as tracefile:
    for line in tracefile:
        filelength = filelength + 1
visitlist = [0 for i in range(filelength)]
filelength = 0
with open(tracepath) as tracefile:
    for line in tracefile:
        temp = int(line)
        visitlist[filelength] = ((temp>>pageshift)>>areashift)
        filelength = filelength + 1
if len(sys.argv) == 1:
    g1 = AcListGenerator(attacktype,maxpagenums,attackpp,0,0,0)
elif len(sys.argv) == 2:
    g1 = AcListGenerator(attacktype,maxpagenums,attackpp,int(sys.argv[1]),0,0)
elif len(sys.argv) == 3:
    g1 = AcListGenerator(attacktype,maxpagenums,attackpp,int(sys.argv[1]),int(sys.argv[2]),0)
elif len(sys.argv) == 4:
    g1 = AcListGenerator(attacktype,maxpagenums,attackpp,int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
flagend = 1
visitcountnow = 0
with open(logpath,'w') as logfile:
    while isbreak != 1:
        for temp in visitlist:
            visitcountnow =  visitcountnow + 1
            addr_temp = temp % maxpagenums
            #g1.visittable[addr_temp][1] = g1.visittable[addr_temp][1] + 1
            while g1.writelist2p != g1.writelistp:
                visitcountnow =  visitcountnow + 1
                addr = g1.getindex(addr_temp)
                #g1.visittable[addr][1] = g1.visittable[addr][1] + 1
                memorystat = g1.d1.access(addr)
                g1.dowhenswap(memorystat)
                if memorystat[0] == -1:
                    g1.d1.m1.printstat()
                    isbreak = 1
                    break
            addr = g1.getindex(addr_temp)
            g1.visittable[addr][1] = g1.visittable[addr][1] + 1
            memorystat = g1.d1.access(addr)
            g1.dowhenswap(memorystat)
            #if(g1.cycles == 0 and flagend == 0):
            if visitcountnow == endnums:
                print('visitcount = 0 flagend')
                g1.d1.m1.printstat()
                isbreak = 1
                break
            if memorystat[0] == -1:
                g1.d1.m1.printstat()
                isbreak = 1
                break
        #isbreak = 1
        print("visitcountnow = " + str(visitcountnow))
        flagend = 0
print("end");
