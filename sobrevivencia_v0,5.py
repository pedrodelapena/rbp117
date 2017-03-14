#! /usr/bin/env python
# -*- coding:utf-8 -*-


import rospy

from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan

class Laser:
	def __init__(self):
		self.ranges=[0.1]*360
		
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

	def back(self):
		print(self.getClosest())



if __name__=="__main__":


	rospy.init_node("aula7")
	laser= Laser()
	velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
	rospy.Subscriber("/scan", LaserScan, laser.bufferize, queue_size = 1)



	while not rospy.is_shutdown():
		temp= laser.getClosest()
		print(temp)
		if temp[1] > 0.4:




		
			velocidade = Twist(Vector3(1, 0, 0), Vector3(0, 0, 0))
			velocidade_saida.publish(velocidade)
		rospy.sleep(2)



# distancia minima 0.7