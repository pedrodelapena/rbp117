#! /usr/bin/env python
# -*- coding:utf-8 -*-


import rospy

from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan

class Laser:
	def __init__(self):
		self.ranges=[0.1]*360
		rospy.Subscriber("/scan", LaserScan, self.bufferize, queue_size= 1)
		
	def bufferize(self, data):
		self.ranges= list(data.ranges)

	def getClosest(self):
		copy=list(self.ranges)
		try:
			while(True):
				copy.remove(0.0)
		except:
			pass

		return [self.ranges.index(min(copy)), min(copy)]
