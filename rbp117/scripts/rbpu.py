#!/usr/bin/python
#coding: utf-8
import rospy
from movement import Movement
from detect import Detect
from memap import MemoryMap

CYCLEDURATION=0.1 #trocar por algo embasado depois


def cycle():

	try:

		while not rospy.is_shutdown():

			detect.update()
			movement.update()

			#dormir direito, calcular distancia gasto durante o ciclo basico e subtrair do tamanho do ciclo
			rospy.sleep(CYCLEDURATION)

	except rospy.ROSInterruptException:
		print("Ocorreu uma exceção com o rospy")
    

if __name__=="__main__":

	rospy.init_node("rbpu_main")
	memap= MemoryMap()
	movement= Movement(memap)
	detect= Detect(memap)

	cycle()
