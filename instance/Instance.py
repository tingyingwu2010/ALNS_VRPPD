# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 14:42:14 2020

@author: 张瑞娟
"""
import numpy as np
import instance.Node as Node
import copy

'''
待修正：
1）需求点：本文实际算例中只有ID,没有坐标
2）需求：实际算例中包括 pickup 和 delivery 两项，目前pickpu 全取0
2）距离矩阵：本文实际算例为直接导入距离数据，不用计算


'''
class ImportData():

    def __init__(self, type, size, name):
        self.file = r'data/{0}_{1}/{2}.TXT'.format(type,size,name)
        self.vehicleNr = 0
        self.vehicleCapacity = 0
        self.fixCost = 100
        self.perCost = 1.5
        self.customerID = []
        self.customercoordinate = []  #list
        self.customerDemand = []
        self.importCustomerData()
        self.distaceMatrix = self.createDistanceMatrix()





    #导入车辆信息：车辆数量，车辆容量（按照标准算例的书写形式）
    def importVehicleData(self):
        with open(self.file) as f:
            for eachline in f:
                info = eachline.split() #默认按空格分
                if info !=[]:
                    if info[0].isdigit():
                        self.vehicleNr = int(info[0])
                        self.vehicleCapacity = int(info[1])
                        break
        print('vehicle information import sucess!')


    #导入需求点信息：id、坐标、需求量(demandD,demandP)
    def importCustomerData(self):
        row = -1000
        with open(self.file) as f:
            for eachline in f:
                info = eachline.split()
                if info != []:
                    if info[0] == 'CUSTOMER':
                        row = 0
                if row >= 3 and len(info) >= 1:
                    self.customerID.append(int(info[0]))
                    self.customercoordinate.append([int(info[1]), int(info[2])])
                    self.customerDemand.append([int(info[3]), 0])
                row += 1
            self.customerCondition = np.array(self.customercoordinate)
            print('顾客点数：', len(self.customerID))
            print('customer information import sucess!')



    def nodes(self):
        node = Node.Node()
        numberOfNode = len(self.customerID)
        Nodes = []
        for i in range(0, numberOfNode):
            node.id = self.customerID[i]
            node.coordinate = self.customercoordinate[i]
            node.demand = self.customerDemand[i]
            new_node = copy.deepcopy(node)
            Nodes.append(new_node)
        return Nodes

    #计算距离矩阵，后续替换为导入距离矩阵
    def createDistanceMatrix(self):
        numberOfNode = len(self.customerID)
        distance = np.zeros([numberOfNode, numberOfNode])
        for i in range(0, numberOfNode):
            for j in range(0, numberOfNode):
                distance[i][j] = distance[j][i] = np.linalg.norm(self.customerCondition[i]-self.customerCondition[j])
        print('distance matrix create sucess!')
        return distance




# def main():
#     importData = ImportData('solomon', 25, 'C101')
#     importData.importVehicleData()
#     importData.importCustomerData()
#     importData.createDistanceMatrix()


# if __name__ == '__main__':
#     # main()
