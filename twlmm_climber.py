#coding:utf-8
import random
import numpy as np
import math


tracepath = 'whb_trace.dat'
##############################
##############################
pageshift = 12

interinterval = 128
swapthreshold = 32 ###visitcount小于swapthreshold的对不能进行交换
mu = 0.3 
sigma = mu*0.11 #

class memorymodel:
    def __init__(self, areasize, attacktype, no, areashift, randomenable, randomshift):
        ##areasize:最大页号，attacktype:攻击类型；no:序号；areashift：相对于页号的粒度移位4MB = 10

        self.maxpagenums = areasize
        self.attacktype = attacktype
        print('maxpagenums' + str(self.maxpagenums))
        np.random.seed(0)
        print("gen life distribution begin")
        areanums = self.maxpagenums >> 10
        p = np.random.normal(loc = mu, scale = sigma, size = 2*areanums)
        p.sort()
        
        x = [0 for i in range(self.maxpagenums)]
        for i in range(self.maxpagenums):
            x[i] = math.pow(p[areanums+(i>>10) - 1],-12)*90.345
        print("gen life distribution end")
        self.lifelist = [[0,x[0]] for y in range(len(x))]
        self.lifelist2 = [[0,x[0]] for y in range(len(x))]
        #self.ideallifelist = [0 for y in range(len(x))]
        self.interswapcount = [0 for y in range(len(x))]
        minlifetime = mu
        maxlifetime = 0
        for i in range(len(x)) :
            if(minlifetime > x[i]):
                minlifetime = x[i]
            if(maxlifetime < x[i]):
                maxlifetime = x[i]
            self.lifelist[i][0] = i
            self.lifelist[i][1] = x[i]###页面i寿命为x[i]
            self.lifelist2[i][0] = i
            self.lifelist2[i][1] = x[i]###页面i寿命为x[i]
            #ideallifelist[i] = x[i]###页面i寿命为x[i]
        print("minlifetime =%d,maxlifetime =%d"%(int(minlifetime),int(maxlifetime)))
        x = []
        self.pairlist = [0 for m in range(self.maxpagenums)]
        print("sort pages begin")
        self.sortedlist = sorted(self.lifelist2, key = lambda x:x[1])####按照寿命排序后，进行配对，配对公式：
        print("sort pages end")
        print("pair pages begin")
        for i in range(len(self.sortedlist)):
            self.pairlist[self.sortedlist[i][0]] = i
        print("pair pages end")
        self.intermaptable = [0 for m in range(int(self.maxpagenums))]###记录对间映射
        self.reversemaptable = [0 for m in range(int(self.maxpagenums))]###记录反向对间映射
        for i in range(len(self.intermaptable)):
            self.intermaptable[i] = i
            self.reversemaptable[i] = i
        self.isswap =  [0 for m in range(int(self.maxpagenums/2))] ##记录该对内部是否是处于交换状态
        self.swapvisitcount = [0 for m in range(int(self.maxpagenums))]###########记录每个页从上次交换起被访问的次数
        #self.hot_record = [0 for m in range(self.maxpagenums)]
        self.swaptimes = 0
        self.interswaptimes = 0
    
        self.no = no
        self.endlifepath = 'type' + str(self.attacktype)+'_twlmm_climber_60_endlife.dat'
    
        self.totalcount = 0
        self.remaptimes = 0
        self.totaltime = 0####循环内次数
    def getpairaddr(self, interswapcount,clifelist,areasize,addr_temp, intermaptable, reversemaptable,sourceaddr):
    #global interinterval
        raddr = 0
        sourceaddr2 = 0
        pairaddr = 0
        pairaddr0 = 0
        sourceaddr2 = 0
        sourceaddr0 = 0
        if sourceaddr == 1:
            addr = self.maxpagenums - 1 - addr_temp
        else:
            addr = addr_temp
        interswapcount[addr] = interswapcount[addr] + 1
        addr_next = 0
        if interswapcount[addr] >= interinterval:
            self.interswaptimes = self.interswaptimes + 1
            interswapcount[addr] = 0
            addr_next = random.randint(0,areasize-1)
            if intermaptable[addr] >=self.maxpagenums / 2:
                pairaddr0 = self.maxpagenums - 1 - intermaptable[addr]
                sourceaddr0 = 1
            else:
                pairaddr0 = intermaptable[addr]
                sourceaddr0 = 0
            while addr_next == intermaptable[addr]:
                addr_next = random.randint(0,areasize-1)           
                if addr_next >=self.maxpagenums / 2:
                    pairaddr = self.maxpagenums - 1 - addr_next
                    sourceaddr2 = 1
                else:
                    pairaddr = addr_next
                    sourceaddr2 = 0
                if sourceaddr0 ^ self.isswap[pairaddr0] != sourceaddr2 ^ self.isswap[pairaddr]:
                    continue

            if sourceaddr0 ^ self.isswap[pairaddr0] == 0:
                clifelist[self.sortedlist[intermaptable[addr]][0]][1] = clifelist[self.sortedlist[intermaptable[addr]][0]][1] - 1 
            else:
                clifelist[self.sortedlist[areasize - 1 - intermaptable[addr]][0]][1] = clifelist[self.sortedlist[areasize - 1 - intermaptable[addr]][0]][1] - 1    
            temp = intermaptable[addr]
            intermaptable[addr] = addr_next
            reverseaddr = reversemaptable[addr_next]
            interswapcount[reverseaddr] = 0
            intermaptable[reverseaddr] = temp
            reversemaptable[temp] = reversemaptable[addr_next]
            reversemaptable[addr_next] = addr
        raddr = intermaptable[addr]
        return raddr

    def swaparbiter (self, life1,life2):
        toss = random.random()
        if toss >= life1 / (life1 + life2):
            return 1
        else:
            return 0
    def access(self,addr_temp2):
        addr_temp =addr_temp2
        isdoswap = 0
        pairindex_temp = self.pairlist[addr_temp]
        pairindex = 0
        sourceaddr = 0 #要写的地址是块内块0还是块1的地址，用于判断是否交换 
        if pairindex_temp >=self.maxpagenums / 2:
            pairindex = self.maxpagenums - 1 - pairindex_temp
            sourceaddr = 1
        else:
            pairindex = pairindex_temp
            sourceaddr = 0
        newaddr = self.getpairaddr(self.interswapcount, self.lifelist, int(self.maxpagenums), pairindex, self.intermaptable, self.reversemaptable,sourceaddr)
        if newaddr >=self.maxpagenums / 2:
            pairaddr = self.maxpagenums - 1 - newaddr
            sourceaddr = 1
        else:
            pairaddr = newaddr
            sourceaddr = 0

        addr = self.sortedlist[pairaddr][0]
        nowaddr2 = self.sortedlist[self.maxpagenums - 1 - self.pairlist[addr]][0]
        if sourceaddr ^ self.isswap[pairaddr] == 0:
            self.swapvisitcount[addr] = self.swapvisitcount[addr] + 1
            if self.swapvisitcount[addr] >= swapthreshold:
                isdoswap = 1
        else:
            self.swapvisitcount[nowaddr2] = self.swapvisitcount[nowaddr2] + 1
            if self.swapvisitcount[nowaddr2] >= swapthreshold:
                isdoswap = 1
        if isdoswap == 1:
            self.swapvisitcount[addr] = 0
            self.swapvisitcount[nowaddr2] = 0
            isdoswap = 0
            swaptemp = 0
            if sourceaddr == 1:
                swaptemp = self.swaparbiter(self.lifelist[nowaddr2][1],self.lifelist[addr][1])#####在执行过程中根据当前寿命调整
            else:
                swaptemp = self.swaparbiter(self.lifelist[addr][1],self.lifelist[nowaddr2][1]) 
            if swaptemp ^ self.isswap[pairaddr] == 1:
                #block end
                #########################################
                ###进行交换，匹配对寿命降低
                self.swaptimes = self.swaptimes + 1
                self.lifelist[addr][1] = self.lifelist[addr][1] - 1
                if self.lifelist[addr][1] < 0:
                    return (-1,0)
                self.lifelist[self.sortedlist[self.maxpagenums - 1 - self.pairlist[addr]][0]][1] = self.lifelist[self.sortedlist[self.maxpagenums - 1 - self.pairlist[addr]][0]][1] -1
                if self.lifelist[self.sortedlist[self.maxpagenums - 1 - self.pairlist[addr]][0]][1] < 0:
                    return (-1,0)
                self.isswap[pairaddr] = self.isswap[pairaddr] ^ 1
            else:
                #self.noswaptimes[pairaddr] = self.noswaptimes[pairaddr] + 1 
                if sourceaddr ^ self.isswap[pairaddr] == 0:
                    self.lifelist[addr][1] = self.lifelist[addr][1] - 1####当前页寿命降低
                    if self.lifelist[addr][1] < 0:
                        return (-1,0)
                else:
                    self.lifelist[self.sortedlist[self.maxpagenums - 1 - self.pairlist[addr]][0]][1] = self.lifelist[self.sortedlist[self.maxpagenums - 1 - self.pairlist[addr]][0]][1] -1
                    if self.lifelist[self.sortedlist[self.maxpagenums - 1 - self.pairlist[addr]][0]][1] < 0:
                        return (-1,0)
        else:
            if sourceaddr ^ self.isswap[pairaddr] == 0:
                self.lifelist[addr][1] = self.lifelist[addr][1] - 1####当前页寿命降低
                if self.lifelist[addr][1] < 0:
                    return (-1,0)
            else:
                self.lifelist[self.sortedlist[self.maxpagenums - 1 - self.pairlist[addr]][0]][1] = self.lifelist[self.sortedlist[self.maxpagenums - 1 - self.pairlist[addr]][0]][1] -1
                if self.lifelist[self.sortedlist[self.maxpagenums - 1 - self.pairlist[addr]][0]][1] < 0:
                    return (-1,0)
        self.totalcount = self.totalcount + 1
        if (self.totalcount - (2000000)) % (20000000) == 0:
            lifenowlist = sorted(self.lifelist, key = lambda x:x[1])
            #for i in range(len(lifenowlist)):
                #self.sortednow[i] = lifenowlist[i][0]
            print('当前最弱页寿命：%d'%(int(lifenowlist[0][1])))
            maxwearrate = 0.0
            wearrate = 0.0
            maxlife = 0
            maxlife2 = 0
            maxi = 0
            mixi2 = 0
            for i in range(len(self.lifelist)):
                wearrate = 1.0- (self.lifelist[i][1]/self.lifelist2[i][1])
                if maxwearrate < wearrate:
                    maxwearrate = wearrate
                    maxlife = self.lifelist[i][1]
                    maxlife2 = self.lifelist2[i][1]
                    maxi = i
            print('当前最大磨损率：%f'%(maxwearrate))
            print('最大磨损页%d寿命：%f,%f'%(maxi,maxlife,maxlife2))
            mixi2 = self.sortedlist[self.maxpagenums - 1 - self.pairlist[maxi]][0]
            print('配对页%d寿命：%f,%f'%(mixi2,self.lifelist[mixi2][1],self.lifelist2[mixi2][1]))
        return (0,0)
    def printstat(self):
        print("write endstat start")
        print('swaptime:%d'%(self.swaptimes))
        print('interswaptime:%d'%(self.interswaptimes))
        with open(self.endlifepath,'w') as f2:
            for i in range(len(self.lifelist)):
                f2.write(U"%d,%d,%d\n"%(self.lifelist[i][0],int(self.lifelist[i][1]),int(self.lifelist2[i][1])))
        print("write endstat end")
        print('totaltime:%d'%(self.totaltime))    
        print("print end");