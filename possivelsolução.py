#!/usr/bin/env python
# -*- coding:utf-8 -*- 
import roslib;
import rospy
import cv2
import sys, select, termios, tty
from geometry_msgs.msg import Twist, Vector3, Pose
from sensor_msgs.msg import LaserScan
from neato_node.msg import Bump


maxSize = ?
resol = (640,480)
obj_global = None
mid = 20;
Ylimit = 50;
velang= None
speed = 1;
turnSpeed = 2.2;
aborted = False
laserScan = [];

def sigaobj(size, pos): #pos é uma tupla (x,y)
    print("sigaobj")
    velrodas = [0,0]
    global velang

    if(size > maxSize or pos[1] <= Ylimit):
        NewSpeed(velrodas)
        return
    
    velrodas = [speed,0]
    distobj = pos[0] - (resol[0] / 2) #recebe x do objeto e vê se está a direita ou esquerda da tela


    if(distobj >= mid):
    velang = -turnSpeed * (float(distobj / (resol[0] / 2)))
    velrodas = [speed, velang]

    print("Distancia eixo X",distobj)
    print(velrodas)
    NewSpeed(velrodas)
    print(velang)
    
    
def NewSpeed(velrodas):   
    vel = Twist(Vector3(velrodas[0],0,0),Vector3(0,0,velrodas[1]))    
    velfinal = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)   
    velfinal.publish(vel)
    
def scanned(laser):
    global laserScan
    laserScan = laser.ranges

def Search(right):        
    if(right):
        NewSpeed([0,-0.3])
    else:
        NewSpeed([0,0.3])
