#!/usr/bin/env python
# -*- coding:utf-8 -*- 
import roslib;
import rospy
import cv2

from geometry_msgs.msg import Twist, Vector3, Pose
from sensor_msgs.msg import LaserScan
from neato_node.msg import Bump

import sys, select, termios, tty

msg = """

"""
maxSize = ?
res = (640,480)
obj_global = None
middleZone = 20;
Ylimit = 50;
delta= None
speed = 1;
turnSpeed = 2.2;

#--
aborted = False
laserScan = [];
batidas = [];

def main(size, pos):
    print("main")
    wheel = [0,0]
    global delta
    if(aborted):
        print("bebe chutado")
        return;
        
       
    if(size > maxSize or pos[1] <= Ylimit):
        SendSpeed(wheel)
        return
    
    wheel = [speed,0]
    distobj = pos[0] - (res[0] / 2)


    #if(distobj >= middleZone):
    delta = -turnSpeed * (float(distobj / (res[0] / 2)))
    wheel = [speed, delta]

    print("odist",distobj)


    print(wheel)
    SendSpeed(wheel);
    print(delta)
    
    
def SendSpeed(wheel):
    
    vel = Twist(Vector3(wheel[0],0,0),Vector3(0,0,wheel[1]))    
    velocidadeFinal = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
    
    velocidadeFinal.publish(vel)
    
    #função que manda pro robo as velocidades de cada roda
    
def scanned(laser):
    global laserScan
    laserScan = laser.ranges

# def onhit(bump_obj):
#     global obj_global
#     obj_global = bump_obj
    
# def Survival():
#     if(not aborted):
#         global laserScan
#         rospy.Subscriber("/scan", LaserScan, scanned)
#         #print(laserScan)
#         rospy.Subscriber("/bump",Bump,bateu)
#         if obj_global != None:
#             if  obj_global.rightFront==1:
#                 print("Bateu frente direita")
#                 SendSpeed([-1,-3])
#                 Abort(1.5)
#             elif  obj_global.leftFront==1 :
#                 print("Bateu frente esquerda")
#                 SendSpeed([-1,3])    
#                 Abort(1.5)  

    

def Abort(time):
    global aborted
    global obj_global
    aborted = True
    print("estou abortando")
    cv2.waitKey(1000)
    aborted = False
    print("Desabortei")
    #dar ré por um tempo e virar um pouco
    #aborted = False

def Search(right):
    if(aborted):
        print("bebe chutado")
        return;
        
    if(right):
        SendSpeed([0,-0.3])
    else:
        SendSpeed([0,0.3])
