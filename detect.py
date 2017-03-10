import rospy
from sensor_msgs.msg import Image

class Detect()

    def capture(image):
        self.image_buffer.append(image)
	    
	
	def update():
	    self.image_buffer.append(image)
	    
	    ##pensar com calma no conteúdo deste try catch
	    try:
		    antes = time.clock()
		    cv_image = bridge.imgmsg_to_cv2(imagem, "bgr8")
		    cv2.imshow("video", cv_image)
		    cv2.waitKey(1)
		    processa(cv_image)
		    depois = time.clock()
		    print ("TEMPO", depois-antes)
	    except CvBridgeError as e:
		    print(e)


    def __init__(self, memap):
    
        rospy.Subscriber("/camera/image_raw", Image, self.capture, queue_size=10, buff_size = 2**24)
        ## é possível que queue_size e buff_size possam ser alterados para valores melhores
        self.memap= memap
