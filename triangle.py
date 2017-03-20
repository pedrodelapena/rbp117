# -*- coding:utf-8 -*-

class Triangle()

    def __init__(self, coord):
        self.red= coord[0]
        self.green= coord[1]
        self.blue= coord[2]
        self.center=( (coord[0][0]+coord[2][0])/2, (coord[0][1]+coord[2][1])/2 )
        #self.rotation
        #self.angle
        #self.distance
        self.age= 0
    
    def update(self):
        self.age+=1
