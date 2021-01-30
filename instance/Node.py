# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 23:05:01 2020

@author: 张瑞娟
"""


import copy

class Node():
    id = 0
    coordinate = [0, 0]
    demand = [0, 0]

    def __str__(self):
        result = ('id:{0},condition:{1},demand:{2}'.format(self.id, self.coordinate, self.demand))
        return result









