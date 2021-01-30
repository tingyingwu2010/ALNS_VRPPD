# -*- coding: utf-8 -*-

import copy
import instance.Instance
from random import choice



class RandomDestroy():

    @staticmethod
    def destroy(s, destroyNum, ins):     # 传入当前解决方案和destroy的点数
        removeCustomers = []
        solution = copy.deepcopy(s)
        distanceMatrix = ins.distaceMatrix


        while (len(removeCustomers) < destroyNum):

            route = choice(solution.routes) #随机选择一个路径
            solution.removeRoute(route)

            nodeIndex = choice(range(1,len(route.route)-1))
            node = route.route.pop(nodeIndex)
            removeCustomers.append(node)

            if(len(route.route) > 2):
                node0 = route.route[nodeIndex-1]
                node1 = route.route[nodeIndex]
                fitness = distanceMatrix[node0.id][node1.id] - distanceMatrix[node0.id][node.id]
                - distanceMatrix[node.id][node1.id]

                route.cost += ins.perCost * fitness
                solution.addRouteToRoutes(route)

        return removeCustomers, solution









