#coding:utf-8
import random
import numpy as np
import defenselayer_ideal_climber as dl ####修改导入文件切换磨损均衡策略
import sys
##############################
##############################
tracepath = 'whb_trace.dat'
endstatpath = 'whb_type2_ideal_endstat.dat'
logpath = 'whb_type2_ideal_log.dat'
endlifepath = 'whb_type2_ideal_endlife.dat'
initlifepath = 'whb_type2_ideal_initlife.dat'
areashift = 0 #4kB 粒度
maxpagenums = (4194304>>2) >> areashift #16GB
isbreak = 0###结束标志
attacktype = 2
filelength = 0
pageshift = 12
attackpp = 1
endnums = 200001000
climbershift = 17
attacksize = 1
##########################################################
class AcListGenerator:
    def __init__(self, type, areasize, attackpp,randomenable, reverseenable, stallenable):
        if areasize <= 2:
            print('error:memorysize too small')
        self.type = type
        self.areasize = areasize
        self.attackpp = attackpp
        self.maplist = [0 for x in range(self.areasize)]###模拟页表:虚页->物理页
        self.revlist = [0 for x in range(self.areasize)]###攻击者维护：物理页：虚页
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
    def getindex(self, addr_temp):####round 0：hot：self.hot+2 cold : 0 other:1
        raddr = 0
        if self.writelist2p != self.writelistp:
            raddr = self.writelist[self.writelist2p]
            self.writelist2p = self.writelist2p + 1
            if self.writelist2p == self.writelistp:
                self.writelist2p = 0
                self.writelistp = 0
            return raddr
        return self.maplist[addr_temp]
    def gethotaddr(self,sortedlist):
        ans = sortedlist[-1][0]
        return ans
    def getcoldaddr(self,sortedlist):
        #ans = sortedlist[0][0]
        for i in range(len(sortedlist)):
            if sortedlist[len(sortedlist) - 1 - i][1] == 0:
                return (sortedlist[len(sortedlist) - 1 - i][0],len(sortedlist) - 1 - i)
        return (sortedlist[0][0],0)
    def dowhenswap(self, memorystat):
        if memorystat[0] == 1:
            self.cycles = self.cycles - 1
            #sortedlist = sorted(memorystat, key = lambda x:x[1])
            if self.attackp() == 1:###概率攻击
                #sortedlist = memorystat[1]
                sortedlist =sorted(self.visittable, key = lambda x:x[1])
                hotaddr = self.gethotaddr(sortedlist)
                coldaddrpair = self.getcoldaddr(sortedlist)
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
            visitcountnow = visitcountnow + 1
            addr_temp = temp % maxpagenums
            while g1.writelist2p != g1.writelistp:
                visitcountnow = visitcountnow + 1
                addr = g1.getindex(addr_temp)
                g1.visittable[addr][1] = g1.visittable[addr][1] + 1
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
            if visitcountnow == endnums:
                print('cycles = 0 flagend')
                g1.d1.m1.printstat()
                isbreak = 1
                break
            if memorystat[0] == -1:
                g1.d1.m1.printstat()
                isbreak = 1
                break
        print("visitcountnow = " + str(visitcountnow))
        flagend = 0
print("end");