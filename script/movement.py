# -*- coding:utf-8 -*-
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
        #self.abort_and_survive
    
    def update(self):
        print("BATATA")
    
        self.laser.getClosest()
        
        readings= self.laser.getClosest()
            #velocidade = Twist(Vector3(0, 0, 0), Vector3(0, 0, 0))
            #velocidade_saida.publish(velocidade)
        minimum_distance = 0.35
        if (readings[1] < minimum_distance) and ( (readings[0] <= 40) or (readings[0]>= 320) ):
            #Emergência! Algo entrou no caminho!
            print("Algo esta proximo demais! :o")
            print("/t detectado ruindade em: "+str(readings))


            if readings[0] <= 40: # 45 graus fica a esquerda dele? então roda para a direita
                print("objeto a esquerda manobras evasivas para a direita!")
                mov = (Twist(Vector3(-0.5,0,0), Vector3(0,0,1)))


            elif readings[0]>= 320: # 315 graus fica a direita dele? então ele roda para a esquerda
                print("objeto a direita manobras evasivas para a esquerda!")
                mov = (Twist(Vector3(-0.5,0,0), Vector3(0,0,-1)))

            print(mov)
            self.move.publish(mov)



            # else:
            #     self.move.publish(Twist(Vector3(0.1,0,0), Vector3(0,0,2))) # não é mais necessario,espero

        elif (self.memap.triangle is None or self.memap.triangle.age >= 30 ):
            #Temos que procurar o triângulo!
            print("cadê triângulo? :c")
            self.move.publish(self.angular)

        else:
            #Achamos o triângulo!
            print("Triângulo achado! ATACAR! >:3")
            pos= self.memap.triangle.center
            resolution= self.memap.resolution
            turnSpeed= 1.0
            mov= Twist(Vector3(0.5,0,0), Vector3(0,0,turnSpeed))

            distance = pos[0] - (resolution[0] / 2) #recebe x do objeto e vê se está a direita ou esquerda da tela
            angular= -turnSpeed * (float(distance / (resolution[0] / 2)))
            mov= Twist(Vector3(0.5,0,0), Vector3(0,0,angular))

            #self.move.publish(mov)
            self.move.publish(Twist(Vector3(1.0,0.0,0.0), Vector3(0.0,0.0,0.0)))