# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 15:31:52 2020

@author: 张瑞娟
"""

class Route():
    def __init__(self):
        self.cost = 0
        self.route = []

    def __str__(self):
        result = '---------Route--------- \ncost = %.2f\n'% self.cost + 'route = ['
        for customer in self.route:
            result += '%s\n'% customer
        return result + "]"

    def initial(self):
        self.cost = 0
        self.route = []


    def addNodeToRoute(self, node):
        self.route.append(node)

    def removeNode(self, node):
        self.route.remove(node)

    def insertNode(self, index, node):
        self.route.insert(index, node)



if __name__ == '__main__':
    print(Route())





