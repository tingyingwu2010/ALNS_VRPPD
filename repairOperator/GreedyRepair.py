# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 20:43:52 2020

@author: 张瑞娟
"""
import instance.Instance
import instance.Route as Rou
import instance.Node as Nod
import algorithm.MyALNS as My

import copy

class GreedyRepair():

    @staticmethod
    def repair(removedSolution, removeCustomers, ins):
        solution = copy.deepcopy(removedSolution)
        distanceMatrix = ins.distaceMatrix
        customers = ins.nodes()

        while(removeCustomers != []):
            insertNode = removeCustomers.pop(0)
            #选择最佳插入位置
            bestFitness = float("inf") #这个保证只要有一个位置满足容量约束，minCost一定会改变
            for i in range(0, len(solution.routes)):
                for j in range(1, len(solution.routes[i].route)):
                    tempRoute = copy.deepcopy(solution.routes[i])
                    tempRoute.insertNode(j, insertNode)
                    #print('GreedyRepair')
                    nodeLoad = My.loadViolation(tempRoute, ins)
                    if(nodeLoad):
                        node0 = tempRoute.route[j - 1]
                        node1 = tempRoute.route[j + 1]
                        fitness = distanceMatrix[node0.id][insertNode.id]
                        + distanceMatrix[insertNode.id][node1.id] - distanceMatrix[node0.id][node1.id]
                        if (fitness < bestFitness):
                            bestFitness = fitness
                            bestRouteIndex = i
                            bestNodeIndex = j
            if bestFitness < float("inf"):
                route = solution.routes[bestRouteIndex]
                route.insertNode(bestNodeIndex, insertNode)
                addCost = ins.perCost * bestFitness
                route.cost += addCost
                solution.totalCost += addCost
            else:
                newroute = Rou.Route()
                insertList = [customers[0], insertNode, customers[0]]
                [newroute.route.append(i) for i in insertList]
                newroute.cost = ins.fixCost + distanceMatrix[customers[0].id][insertNode.id]
                + distanceMatrix[insertNode.id][customers[0].id]
                solution.addRouteToRoutes(newroute)


        return solution








