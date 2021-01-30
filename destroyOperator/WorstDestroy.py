# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 22:00:33 2020

@author: 张瑞娟
"""
import instance.Instance
import instance.Route
import copy


class WorstDestroy():

    @staticmethod
    def destroy(s, destroyNum, ins):     # 传入当前解决方案和destroy的点数
        removeCustomers = []
        solution = copy.deepcopy(s)
        distanceMatrix = ins.distaceMatrix

        while(len(removeCustomers) < destroyNum):
            bestFitness = float("inf")
            for r in solution.routes:
                for n in r.route[1:-1]:

                    #路径中只有一个顾客时，fitness为路径所有成本，否则fitnes为路径成本变化量
                    if(len(r.route) <= 3):
                        fitness = r.cost
                    else:
                        nodeIndex = r.route.index(n)
                        node0 = r.route[nodeIndex - 1]
                        #print('路径长度：', len(r.route))
                        #print('node:', nodeIndex)
                        node1 = r.route[nodeIndex + 1]
                        fitness = distanceMatrix[node0.id][node1.id] - distanceMatrix[node0.id][n.id]
                        - distanceMatrix[n.id][node1.id]

                    if fitness < bestFitness:
                        bestFitness = fitness
                        route = r
                        node = n

            removeCustomers.append(node)
            solution.removeRoute(route)
            route.removeNode(node)
            if(len(route.route) > 2):
                route.cost += ins.perCost * fitness
                solution.addRouteToRoutes(route)

        return removeCustomers, solution








