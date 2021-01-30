# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 15:07:24 2021

@author: 张瑞娟
"""

'''
定义参数的类
'''

class Parameter():
    def __init__(self):

        #算子更新频率250
        self.fre = 1

        #新解优于最优解时得分
        self.theta1 = 20

        #新解优于当前解时得分
        self.theta2 = 12

        #新解不优于当前解但接受
        self.theta3 = 6

        #新解不优于当前解且没接受
        self.theta4 = 2

        #冷却系数
        self.c = 0.95

        #反应系数
        self.r = 0.5

        #终止系数
        self.t = 0.01

        #破坏率
        self.drate= 0.2

