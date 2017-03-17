import rospy
from geometry_msgs.msg import Twist, Vector3, Pose
from laser import Laser

class Movement():
    
    def __init__(self, memap):
    
        self.move= rospy.Publisher("/cmd_vel", Twist, queue_size = 1) #entender bem esta linha
        self.speed= Twist(Vector3(0,0,0), Vector3(0,0,0))
        self.memap= memap
        self.laser= Laser()
        self.abort_and_survive
    
    def update():
    
        self.laser.getClosest()
        
        	readings= self.laser.getClosest()
	        #velocidade = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))
	        #velocidade_saida.publish(velocidade)
	        minimum_distance = 0.35

	        if readings[1] < minimum_distance and (readings[0] < 45 or temp[0]> 315) :

		        angular = Twist(Vector3(0, 0, 0), Vector3(0, 0, 1))
		        self.move.publish(angular)

	        elif temp[1] < Dm:
		        go_forward= Twist(Vector3(0.5, 0, 0), Vector3(0, 0, 0))
		        self.move.publish(go_forward)
               
        
    def codedump():
    
        if len(media) != 0 and len(centro) != 0:
				dif_x = media[0]-centro[0]
				dif_y = media[1]-centro[1]
				if math.fabs(dif_x)<30: #and math.fabs(dif_y)<50:
					vel = Twist(Vector3(0.5,0,0), Vector3(0,0,0))
				else:
					if dif_x > 0:
						# Vira a direita
						vel = Twist(Vector3(0,0,0), Vector3(0,0,-0.2))
					else:
						# Vira a esquerda
						vel = Twist(Vector3(0,0,0), Vector3(0,0,0.2))
