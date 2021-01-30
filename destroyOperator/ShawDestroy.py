# -*- coding: utf-8 -*-

import instance.Instance
from random import choice
import copy

#删除相关度最高的
class ShawDestroy():

    @staticmethod
    def destroy(s, destroyNum, ins):     # 传入当前解决方案和destroy的点数
        removeCustomers = []
        solution = copy.deepcopy(s)
        distanceMatrix = ins.distaceMatrix

        route = choice(solution.routes) #随机选择一个路径
        node = choice(route.route[1:-1])

        while (len(removeCustomers) < destroyNum):
            solution.removeRoute(route)
            nodeIndex = route.route.index(node)
            #print('nodeIndex:', nodeIndex)
            #print(len(route.route))

            route.removeNode(node)
            #print(len(route.route))
            removeCustomers.append(node)
            if(len(route.route) > 2):
                node0 = route.route[nodeIndex-1]
                node1 = route.route[nodeIndex]
                fitness = distanceMatrix[node0.id][node1.id] - distanceMatrix[node0.id][node.id]
                - distanceMatrix[node.id][node1.id]

                route.cost += ins.perCost * fitness
                solution.addRouteToRoutes(route)

            #此处相关度只考虑了距离和需求，没有考虑是否在同一辆车上
            minRelate = float("inf")
            for r in solution.routes:
                for n in r.route[1:-1]:
                    nextNode = n

                    fitness = 3 * distanceMatrix[node.id][nextNode.id]
                    + 2 * abs((node.demand[1] - node.demand[0]) - (nextNode.demand[1] - nextNode.demand[0]))

                    if(fitness < minRelate):
                        minRelate = fitness
                        route = r
                        node = n

        return removeCustomers, solution


































