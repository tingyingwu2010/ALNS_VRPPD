# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 20:56:22 2021

@author: 张瑞娟
"""

from instance.Instance import ImportData as Imp
from algorithm.InitialSolution import InitialSolution as Init
from destroyOperator.WorstDestroy import WorstDestroy
from destroyOperator.RandomDestroy import RandomDestroy
from repairOperator.GreedyRepair import GreedyRepair as GreedyRepair
from repairOperator.RandomRepair import RandomRepair as RandomRepair
from repairOperator.RegretRepair import RegretRepair as RegretRepair
from destroyOperator.ShawDestroy import ShawDestroy


import ControlParameter as Par

import numpy as np
import random
import time
import copy
import math



class Process():

    temStart = 100 #起始温度
    destroyList = [RandomDestroy, ShawDestroy, WorstDestroy] #destroy算子列表
    repairList = [GreedyRepair, RandomRepair, RegretRepair]


    def __init__(self, ins, initialSol):
        self.alns = Par.Parameter()
        self.temTermin = self.temStart * self.alns.t
        self.timeOperator = copy.deepcopy(self.creatDict()) #记录每个算子选中次数
        self.scoreOperator = copy.deepcopy(self.creatDict()) #记录每个算子的得分
        self.ins = ins
        self.numberOfNode = len(self.ins.customerID)
        self.destroyNr = int(self.alns.drate * self.numberOfNode)  #destroy的点的数量
        self.time = 0
        #self.bestVal = []
        #self.currentVal = []
        self.initialSol = initialSol.getInitialSolution()
        self.destroyList = [RandomDestroy, ShawDestroy, WorstDestroy] #destroy算子列表
        self.repairList = [GreedyRepair, RandomRepair, RegretRepair]
        self.weightDestroy = np.array([1,1,1],dtype = float)  #每个destroy算子的权重
        self.weightRepair = np.array([1,1,1], dtype = float)   #每个repair算子的权重


    def iteration(self):

        globalSol = copy.deepcopy(self.initialSol)
        currentSol = copy.deepcopy(self.initialSol)
        bestVal = []
        currentVal = []


        bestVal.append(globalSol.totalCost)
        currentVal.append(currentSol.totalCost)
        noImprove = 0

        start = time.time()
        T = self.temStart
        ite = 0
        time_1 = 0
        time_2 = 0
        time_3 = 0
        while T >= self.temTermin:
            #print(ite)

            p_destroy = self.weightDestroy / sum(self.weightDestroy)
            # print(p_destroy)
            p_repair = self.weightRepair / sum(self.weightRepair)
            # print(p_repair)

            # 内层循环，循环完成后更新一次算子权重
            for i in range(self.alns.fre):

                start_1 = time.time()
                destroy = np.random.choice(self.destroyList, p = p_destroy)
                removeCus, removedSol = destroy.destroy(currentSol, self.destroyNr, self.ins)
                repair = np.random.choice(self.repairList, p = p_repair)
                tempSol = repair.repair(removedSol, removeCus, self.ins)
                end_1 = time.time()
                #print(end_1-start_1)
                time_1 += end_1 -start_1
                self.timeOperator = self.upDict(self.timeOperator, destroy, repair, 1)

                start_2 = time.time()
                tempVal = tempSol.totalCost
                p = math.exp((currentSol.totalCost - tempVal)/T)


                if tempVal < globalSol.totalCost:
                    globalSol = copy.deepcopy(tempSol)
                    bestVal.append(tempVal)
                    print('优化一次')
                    self.scoreOperator = self.upDict(self.scoreOperator, destroy, repair, self.alns.theta1)
                    noImprove = 0

                elif tempVal < currentSol.totalCost:
                    currentSol = copy.deepcopy(tempSol)
                    currentVal.append(tempVal)
                    self.scoreOperator = self.upDict(self.scoreOperator, destroy, repair, self.alns.theta2)

                elif p > random.random():
                    currentSol = copy.deepcopy(tempSol)
                    currentVal.append(tempVal)
                    self.scoreOperator = self.upDict(self.scoreOperator, destroy, repair, self.alns.theta3)
                    noImprove += 1

                else:
                    self.scoreOperator = self.upDict(self.scoreOperator, destroy, repair, self.alns.theta4)
                    noImprove += 1

                end_2 = time.time()
                time_2 += end_2 - start_2
                #print('判断时间：', end_2-start_2)

                if noImprove >= 10:
                    p_destroy, p_repair = self.initialWeight()
                    currentSol = copy.deepcopy(globalSol)
                    noImprove = 0

            #每完成一次内层循环，更新一次算子权重
            start_3 = time.time()
            for operator in self.timeOperator:
                # print('self.destroyList:', type(self.destroyList))
                # print(type(self.destroyList[1]))
                # print('operator类型：' , type(operator))
                # print(operator)
                if self.timeOperator[operator] == 0:
                    self.upWeight1(operator)
                else:
                    self.upWeight2(operator)
            end_3 = time.time()
            time_3 += end_3 - start_3

            T = T * self.alns.c
            ite += 1

        end = time.time()
        self.time = end - start
        print('算子操作：', time_1)
        print('判断操作：', time_2)
        print('更新权重：', time_3)

        #输出运行时间和各算子使用次数
        print('总运行时间为%.2f\n' % self.time)
        #print('最优值：', globalSol.totalCost)
        print('bestVal:', bestVal)
        print('currentVal:', currentVal)
        #print('最优解：', globalSol)
        for key, value in self.timeOperator.items():
            print('{}:{}'.format(key.__name__,value))

        return globalSol


    #创建包含所有算子的字典
    def creatDict(self):
        key = [RandomDestroy, ShawDestroy, WorstDestroy, GreedyRepair, RandomRepair, RegretRepair]
        value = np.zeros(6, int)
        dictionary = dict(zip(key, value))
        return dictionary

    #更新字典(更新算子使用次数和分数)
    def upDict(self, dictionary, destroy, repair, val):
        dictionary[destroy] += val
        dictionary[repair] += val
        return dictionary

    #初始化算子权重
    def initialWeight(self):
        self.weightDestroy = np.array([1,1,1], dtype = float)
        self.weightRepair = np.array([1,1,1], dtype = float)
        p_destroy = self.weightDestroy / sum(self.weightDestroy)
        p_repair = self.weightRepair / sum(self.weightRepair)
        return  p_destroy, p_repair

    #更新权重
    #算子使用次数为0
    def upWeight1(self, operator):
        if operator in self.destroyList:
            index1 = self.destroyList.index(operator)
            # print(self.weightDestroy[index1])
            # print(self.alns.r)
            self.weightDestroy[index1] = self.weightDestroy[index1] * (1 - self.alns.r)
            # print(self.weightDestroy[index1])
            # print('0weightDestroy:', self.weightDestroy)
        else:
            index2 = self.repairList.index(operator)
            self.weightRepair[index2] = self.weightRepair[index2] * (1 - self.alns.r)
            # print('0weightRepair:', self.weightRepair)

    #算子使用次数不为0
    def upWeight2(self, operator):
        if operator in self.destroyList:
            index1 = self.destroyList.index(operator)
            self.weightDestroy[index1] = self.weightDestroy[index1] * (1 - self.alns.r)
            + self.alns.r * self.scoreOperator[operator] / self.timeOperator[operator]
            # print('1weightDestroy:', self.weightDestroy)
        else:
            #print(operator)
            index2 = self.repairList.index(operator)
            self.weightRepair[index2] = self.weightRepair[index2] * (1 - self.alns.r)
            + self.alns.r * self.scoreOperator[operator] / self.timeOperator[operator]
            # print('1weightRepair:', self.weightRepair)












































