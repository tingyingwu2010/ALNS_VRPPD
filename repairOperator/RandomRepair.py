# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 16:17:11 2020

@author: 张瑞娟
"""
import instance.Instance
import instance.Route as Rou
import instance.Node as Nod
import algorithm.MyALNS as My
import copy
import random

class RandomRepair():

    @staticmethod
    def repair(removedSolution, removeCustomers, ins):
        solution = copy.deepcopy(removedSolution)
        distanceMatrix = ins.distaceMatrix
        customers = ins.nodes()

        while(removeCustomers != []):
            insertNode = removeCustomers.pop(0)
            bestFitness = float("inf")
            #随机产生可能插入的路径索引
            routeNr = random.randint(1, len(solution.routes))
            routeList = random.sample(range(len(solution.routes)), routeNr)

            for i in routeList:
                tempRoute = copy.deepcopy(solution.routes[i])
                #随机产生可能插入的位置的个数和索引
                nodeNr = random.randint(1, len(tempRoute.route) - 1) #可插入位置为1个--总个数-1个
                nodeList = random.sample(range(1, len(tempRoute.route)), nodeNr)
                for j in nodeList:
                     tempRoute.insertNode(j, insertNode)
                     #print('RandomRepair')
                     nodeLoad1 = My.loadViolation(tempRoute, ins)
                     if(nodeLoad1):
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





