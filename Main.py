# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 17:45:54 2021

@author: 张瑞娟
"""

import instance.Instance as Ins
import algorithm.InitialSolution as Init
import algorithm.MyALNSProcess as Process

'''
    
'''
def main():
    insType = 'solomon'
    size = 25
    name = 'C101'

    instance = Ins.ImportData(insType, size, name)
    initialSol = Init.InitialSolution(instance)
    #initialSolution = initialSol.getInitialSolution()

    operation = Process.Process(instance, initialSol)
    globalSol = operation.iteration()
    #bestVal = operation.bestVal
    print('globalSol:', globalSol)

    # print('最优值：')
    # for i in bestVal:
    #     print(i)

    # print('最优解' + globalSol)

if __name__ == '__main__':
    main()









