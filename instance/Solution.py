# -*- coding: utf-8 -*-


import instance.Route

class Solution():

    def __init__(self):
        self.totalCost = 0
        self.routes = []

    def __str__(self):
        result = 'solution: total cost %.2f\n'%self.totalCost + 'routes: ['
        for route in self.routes:
            result += '%s'%route
        return result + ']'

    def addRouteToRoutes(self, route):
        self.routes.append(route)
        self.totalCost += route.cost

    def removeRoute(self, route):
        self.routes.remove(route)
        self.totalCost -= route.cost

    def replaceRoute(self, index, route):
        temp = self.routes[index]
        self.routes[index] = route
        self.totalCost += route.cost - temp.cost

if __name__ == '__main__':
    print(Solution())
