# -*- coding: utf-8 -*-

import instance.Route as Rou
import instance.Solution as Sol
import algorithm.MyALNS as My
import numpy as np
import copy

class InitialSolution():

    def __init__(self, ins):
        self.ins = ins
        self.distanceMatrix = ins.distaceMatrix
        ins.importVehicleData()
        self.vehicleCapacity = ins.vehicleCapacity
        self.vehicleNr = ins.vehicleNr
        self.customers = ins.nodes()
        self.fixCost = ins.fixCost
        self.perCost = ins.perCost


    def getInitialSolution(self):

        solution = Sol.Solution()  #实例化一个解
        customer = copy.deepcopy(self.customers)


        #创建一个路径
        route = Rou.Route()
        #load = 0  #负载
        self.vehicleNr = self.vehicleNr - 1
        route.cost = self.fixCost     #成本 目前只考虑固定成本和路径成本
        depot = customer.pop(0)  #删除并返回仓库节点
        route.addNodeToRoute(depot)  #添加仓库节点至路径



        while(True):
            #顾客全部遍历
            if(len(customer) == 0):
                break

            lastNode = route.route[-1]   #取当前路径的最后一个元素
            #找出距离当前解最近的点
            minIndex = np.argmin([self.distanceMatrix[lastNode.id][i.id] for i in customer])
            minNode = customer[minIndex]

            #若此点满足容量约束，更新路径、成本和负载,并从当前顾客集中移除该点
            route.addNodeToRoute(minNode)
            #print('初始化')
            nodeLoad = My.loadViolation(route, self.ins)
            if(nodeLoad):
                route.cost += self.perCost * self.distanceMatrix[lastNode.id][minNode.id]
                customer.remove(minNode)

            #若此点不满足容量约束，结束该路径并添加至解决方案中
            else:
                route.removeNode(minNode)
                route.addNodeToRoute(depot)
                route.cost += self.perCost * self.distanceMatrix[lastNode.id][depot.id]
                solution.addRouteToRoutes(route)
                if (self.vehicleNr == 0):
                    break
                else:
                    route = Rou.Route()
                    self.vehicleNr -= 1
                    route.cost = self.fixCost
                    route.addNodeToRoute(depot)

        # 添加最后一条路径至解决方案
        if(len(customer) == 0):
            route.addNodeToRoute(depot)
            route.cost += self.perCost * self.distanceMatrix[route.route[-1].id][depot.id]
            solution.addRouteToRoutes(route)

        #print('已生成初始解')
        return solution













                



































