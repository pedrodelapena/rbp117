import rospy
from movement import Movement
from detect import Detect
from memap import MemoryMap

CYCLEDURATION=0.1 #trocar por algo embasado depois


def cycle():

    try:

		while not rospy.is_shutdown():
		

			movement.update()
			detect.update()
			rospy.sleep(CYCLEDURATION)

    except rospy.ROSInterruptException:
	        print("Ocorreu uma exceção com o rospy")
	        
def init():

	rospy.init_node("rbpu_main")
	memap= MemoryMap() 
	#movement= Movement(memap)
	detect= Detect(memap)
	
	recebedor= rospy.Subscriber("/camera/image_raw", Image, recebe, queue_size=10, buff_size = 2**24)

	#cv2.namedWindow("hope")
	#cv2.namedWindow("dreams")

	cycle()
    

if __name__=="__main__":

    init()
