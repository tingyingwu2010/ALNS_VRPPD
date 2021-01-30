# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 20:36:29 2020

@author: 张瑞娟
"""
import instance.Instance as ins
import instance.Node

import numpy as np


def loadViolation(route, ins):

    vehicleCapacity = ins.vehicleCapacity
    load = np.zeros(len(route.route))  #和路径中点对应,但离开最后一个点（车场）时无实际意义
    #计算离开车场时的负载
    for n in route.route:
        #print(type(n))
        load[0] += n.demand[0]

    #离开i点时车辆的负载
    for i in range(1, len(route.route)):

        load[i] = load[i-1] - route.route[i].demand[0] + route.route[i].demand[1]
    # print('vehicleCapacity:', vehicleCapacity)
    # print('load', load)
    # print(type(vehicleCapacity))
    # print(type(load))

    nodeLoad = (np.array(load) < vehicleCapacity).all()
    return nodeLoad








