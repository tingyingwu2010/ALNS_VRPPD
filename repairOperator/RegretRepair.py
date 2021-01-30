# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 21:16:54 2020

@author: 张瑞娟
"""
import instance.Route as Rou
import algorithm.MyALNS as My
import numpy as np
import instance.Node
import copy

class RegretRepair():

    @staticmethod
    def repair(removedSolution, removeCustomers, ins):
        solution = copy.deepcopy(removedSolution)
        distanceMatrix = ins.distaceMatrix
        customers = ins.nodes()
        bestPoses = []

        while(removeCustomers != []):
            insertNod = removeCustomers.pop(0)
            first = second = float('inf')
            bestNodeIndex = 0
            bestRouteIndex = 0

            for i in range(0, len(solution.routes)):
                for j in range(1, len(solution.routes[i].route)):
                    tempRoute = copy.deepcopy(solution.routes[i])
                    tempRoute.insertNode(j, insertNod)
                    nodeLoad = My.loadViolation(tempRoute, ins)
                    if(nodeLoad):
                        node0 = tempRoute.route[j - 1]
                        node1 = tempRoute.route[j + 1]
                        fitness = distanceMatrix[node0.id][insertNod.id]
                        + distanceMatrix[insertNod.id][node1.id] - distanceMatrix[node0.id][node1.id]
                        if (fitness < first):
                            bestRouteIndex = i
                            bestNodeIndex = j
                            second = first
                            first = fitness
                        elif(fitness < second and fitness != first):
                            second = fitness
            val = float('%.2f' % (second - first))
            bestPoses.append([insertNod.id, bestRouteIndex, bestNodeIndex, val])
        bestPoses = np.array(bestPoses)
        bestPoses = bestPoses[np.lexsort(-bestPoses.T)]  #按最后一列做降序排序
        #前面bestPose为不考虑插入先后顺序和最佳位置的重复性得到的，再依次插入时，要重新计算负载和成本增加
        for i in bestPoses:
            tempRoute = copy.deepcopy(solution.routes[int(i[1])])
            for j in range(0, len(customers)):
                if customers[j].id == int(i[0]):
                    #print('inserNode:', insertNod)
                    insertNod = customers[j]
            #insertNode = [customers[j] for j in range(0, len(customers)) if customers[j].id == int(i[0])
            #print(type(insertNode))
            tempRoute.insertNode(int(i[2]), insertNod)
            #print('RegertRepair')
            nodeLoad = My.loadViolation(tempRoute, ins)
            if(nodeLoad):
                node0 = tempRoute.route[int(i[2]) - 1]
                node1 = tempRoute.route[int(i[2]) + 1]
                tempRoute.cost += distanceMatrix[node0.id][insertNod.id]
                + distanceMatrix[insertNod.id][node1.id] - distanceMatrix[node0.id][node1.id]
                solution.replaceRoute(int(i[1]), tempRoute)


            else:
                newroute = Rou.Route()
                insertList = [customers[0], insertNod, customers[0]]
                [newroute.route.append(i) for i in insertList]
                newroute.cost = ins.fixCost + distanceMatrix[customers[0].id][insertNod.id]
                + distanceMatrix[insertNod.id][customers[0].id]
                solution.addRouteToRoutes(newroute)

        return solution









