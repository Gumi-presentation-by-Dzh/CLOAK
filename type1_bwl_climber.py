#coding:utf-8
import random
import numpy as np
import defenselayer_bwl_climber as dl ####修改导入文件切换磨损均衡策略
import sys
##############################
##############################
#tracepath = 'whb_trace.dat'
endstatpath = 'whb_type1_bwl_endstat.dat'
logpath = 'whb_type1_bwl_log.dat'
endlifepath = 'whb_type1_bwl_endlife.dat'
initlifepath = 'whb_type1_bwl_initlife.dat'
areashift = 0 #4kB 粒度
maxpagenums = (4194304 >> 2) >> areashift #4GB
isbreak = 0###结束标志
attacktype = 1
attackpp = 1
bwlsize = 0
#endnums = 220001000 ##输出10个周期的结果
endnums = 200001000 ##输出140个周期的结果
climbershift = 10
attacknums = 0##记录经过了几次写操作
##########################################################
class AcListGenerator:
    def __init__(self, type1, areasize, attackpp,randomenable, reverseenable, stallenable):
        if areasize <= 2:
            print('error:memorysize too small')
        self.type = type1
        self.attackpp = attackpp
        self.areasize = areasize
        #self.attackarea = 256###256 = hotlis大小，12= groupshift
        self.attackarea = self.areasize
        self.attackflag = [0 for i in range(self.attackarea)]
        self.flag = 0
        self.index = 0
        self.round = 0
        self.initcycle = 0
        self.count = 0
        self.hot = 1000000
        self.d1 = dl.DefenseLayer(self.areasize, self.type,randomenable, reverseenable, stallenable, climbershift)
        self.coldaddr = [self.areasize - 1,self.areasize - 2]
    def attackp(self):
        rn = random.random()
        if rn > self.attackpp:
            return 0
        else:
            return 1
    def getindex(self):####round 0：hot：self.hot+2 cold : 0 other:1
        ans = self.index
        if self.flag == 0:
            if self.index >= self.attackarea - 2:
                self.round = 1
                self.index = 0
            elif self.round == 0:
                self.index = self.index + 1
            elif self.count < self.hot: #
                self.count = self.count + 1
                if self.initcycle == 1:
                    ans = self.coldaddr[self.flag]
            else:
                self.count = 0
                self.round = 0
        else:
            if self.index <= 1:
                self.round = 1
                self.index = self.attackarea - 1
            elif self.round == 0:
                self.index = self.index - 1
            elif self.count < self.hot:
                self.count = self.count + 1
                if self.initcycle == 1:
                    ans = self.coldaddr[self.flag]
            else:
                self.count = 0
                self.round = 0
        return ans
    def dowhenswap(self, isswap):
        if isswap[0] == 1:
            self.initcycle = 1
            self.round = 0
            self.count = 0
            if self.attackp() == 1:
                self.flag = self.flag ^ 1
if len(sys.argv) == 1:
    g1 = AcListGenerator(attacktype,maxpagenums,attackpp,0,0,0)
elif len(sys.argv) == 2:
    g1 = AcListGenerator(attacktype,maxpagenums,attackpp,int(sys.argv[1]),0,0)
elif len(sys.argv) == 3:
    g1 = AcListGenerator(attacktype,maxpagenums,attackpp,int(sys.argv[1]),int(sys.argv[2]),0)
elif len(sys.argv) == 4:
    g1 = AcListGenerator(attacktype,maxpagenums,attackpp,int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
with open(logpath,'w') as logfile:
    while isbreak == 0:
        addr = g1.getindex()
        attacknums = attacknums + 1
        if attacknums >= endnums:
            g1.d1.m1.printstat()
            isbreak = 1
            break
        memorystat = g1.d1.access(addr)
        g1.dowhenswap(memorystat)
        if memorystat[0] == -1:
            g1.d1.m1.printstat()
            isbreak = 1
print("end");