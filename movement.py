import rospy
from geometry_msgs.msg import Twist, Vector3, Pose
from laser import Laser

class Movement:
    
    def __init__(self, memap):
    
        self.move= rospy.Publisher("/cmd_vel", Twist, queue_size = 1) #entender bem esta linha
        self.speed= Twist(Vector3(0.5,0,0), Vector3(0,0,0))
        self.angular= Twist(Vector3(0,0,0), Vector3(0,0,1))
        self.memap= memap
        self.laser= Laser()
        self.abort_and_survive
    
    def update(self):
    
        self.laser.getClosest()
        
        readings= self.laser.getClosest()
	        #velocidade = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))
	        #velocidade_saida.publish(velocidade)
        minimum_distance = 0.35


        if readings[1] < minimum_distance:
            #Emergência! Algo entrou no caminho!


            if (readings[0] < 45 or readings[0]> 315) :
                self.move.publish(self.angular)

            else:
                self.move.publish(self.speed)
        elif (memap.triangle is None or memap.triangle.age >= 30 ):
            #Temos que procurar o triângulo!
            self.move.publish(self.angular)

        else:
            #Achamos o triângulo!
            pos= self.memap.triangle.center
            resolution= self.memap.resolution
            turnSpeed= 2.2
            mov= Twist(Vector3(0.5,0,0), Vector3(0,0,2.2))

            distance = pos[0] - (resolution[0] / 2) #recebe x do objeto e vê se está a direita ou esquerda da tela
            angular= -turnSpeed * (float(distance / (resolution[0] / 2)))
            mov= Twist(Vector3(0.5,0,0), Vector3(0,0,angular))

            self.move.publish(mov)





