#coding:utf-8
import random
import numpy as np
import twlmm_climber as mm
enable = 0
normalp = 0
attackp = 0
gapp = [normalp, attackp]
###############stall par begin
stalllimits = 5
stallenable = 0
par1threshold = 0
par2threshold = 0
#################### end
#######################random begin
randomshift = 10
randomenable = 0
######################random end
class DefenseLayer:
    def __init__(self, areasize, attacktype,climberenable, randomenable, stallenable):
        self.areashift = 10#
        self.maxpagenums = areasize
        self.attacktype = attacktype
        self.stallnums = 0
        self.attacknums = 0
        self.stat = 0 ##
        self.start = 0
        no = 0
        self.m1 = mm.memorymodel(self.maxpagenums, self.attacktype,no, self.areashift, randomenable, randomshift)
        #self.life2sorted = self.m1.getlife2sorted()
        self.life2sorted = [0 for i in range(self.maxpagenums)]####climber
        self.logpath = "type"+str(self.attacktype)+"_defense_idealmm.dat"
        #self.life2sorted = self.m1.getlife2sorted()
        self.logfile = open(self.logpath, "w")
    def __del__(self):
        self.logfile.close()
    def hotdistribute(self, sortedcountlist):
        areasize = 1000
        total = 0
        for i in range(len(sortedcountlist)):
            total = total + sortedcountlist[i][1]
        average = float(total) / float(areasize)
        maxcount = sortedcountlist[len(sortedcountlist) - 1][1]
        print(maxcount)
        level = int(float(maxcount) / average)
        self.logfile.write(U"level:%d\n"%level)
        return level
    def hotmonitor(self, sortedcountlist):
        dismatch = 0
        areasize = 1000
        addrsource = 0
        maxdismatch = 0
        dis = 0
        if self.start == 0:
            return (0,0)
        for i in range(areasize):
            addrsource = sortedcountlist[i][0]
            if i >= self.life2sorted[addrsource]:
                dis = i - self.life2sorted[addrsource]
            else:
                dis = self.life2sorted[addrsource] - i
            self.life2sorted[addrsource] = i
            dismatch = dismatch + dis
            if maxdismatch < dis:
                maxdismatch = dis
        self.logfile.write(U"dismatch:%d\n"%dismatch)
        self.logfile.write(U"max:%d\n"%maxdismatch)
        return (dismatch, maxdismatch)
    def attdetector(self, addr_temp, sortedlist):
        isswap = 1
        par1 = self.hotdistribute(sortedlist)
        par2 = self.hotmonitor(sortedlist)
        if stallenable == 1:
            if par1 >= par1threshold or par2[1] >= par2threshold:
                self.stallnums = self.stallnums + 1
                if self.stallnums >= stalllimits:
                    return -1 
        return isswap
    def access(self, addr_temp):
        memorystat1 = self.m1.access(addr_temp)
        if memorystat1[0] == 1:
            if enable == 0:
                self.start = 1
                memorystat2 = self.m1.doswap(addr_temp, 1)
                if memorystat2[0] == -1:
                    return (memorystat2[0], memorystat1[1])
            #return (isswap, memorystat1[1])
                return (memorystat1[0],memorystat1[1])
            isswap = self.attdetector(addr_temp,memorystat1[2])
            if isswap == -1:
                return (-1, memorystat1[1])
            self.start = 1
            memorystat2 = self.m1.doswap(addr_temp, isswap)
            if memorystat2[0] == -1:
                return (memorystat2[0], memorystat1[1])
            #return (isswap, memorystat1[1])
            return (memorystat1[0], memorystat1[1])
        return (memorystat1[0],memorystat1[1])
