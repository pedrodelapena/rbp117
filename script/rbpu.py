#! /usr/bin/env python
# -*- coding:utf-8 -*-


import rospy
from movement import Movement
from detect import Detect
from memap import MemoryMap

CYCLEDURATION=0.2 #trocar por algo embasado depois


def cycle():

	try:

		while not rospy.is_shutdown():

			detect.update()
			movement.update()
			rospy.sleep(CYCLEDURATION)
			movement.stop()
			

	except rospy.ROSInterruptException:
		print("Ocorreu uma exceção com o rospy")
    

if __name__=="__main__":

	rospy.init_node("rbpu_main")
	memap= MemoryMap()
	movement= Movement(memap)
	detect= Detect(memap)

	cycle()
