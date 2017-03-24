# -*- coding:utf-8 -*-

import rospy
import tf
import math
import cv2
import time
from geometry_msgs.msg import Twist, Vector3, Pose
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

from triangle import Triangle

import itertools

class Detect:

    def capture(self, image):
        if self.channel_open:
            image= self.bridge.imgmsg_to_cv2(image, "bgr8")
            self.image_buffer.append(image)
            
    def recon(self):
        print("LARANJA")
        if (len(self.image_buffer)==0):
            return
        #começar analisando da imagem mais recente, abortar se eu conseguir confirmação visual do que eu procuro
        #TODO opcional: analisar a idade das imagens e começar meu triângulo com uma certa idade proporcional em vez de zero
        
        still_work_to_do= True
        
        while(still_work_to_do and (len(self.image_buffer) != 0)):
            print(len(self.image_buffer))
            self.image_buffer=self.image_buffer[-1:]
            def scope():
        
                src=self.image_buffer[-1]
                cv2.resize(src, None,fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
                src = cv2.GaussianBlur(src, (5, 5), 0)
                self.image_buffer.pop(-1)
                self.channel_open=False
            
                reds= self.recon_target(src, "red")
                if (len(reds) < 3): #versão do if para quando só uso vermelhos
                    return 1
                #if (len(reds) == 0):
                #    return 1
                #greens= self.recon_target(src, "green")
                #if (len(greens) == 0):
                #    return 2
                #blues= self.recon_target(src, "blue")
                #if (len(blues) == 0):
                #    return 3
                
                #triangles= self.find_right_angled_triangles(reds, greens, blues)
                triangles= self.find_right_angled_triangles_monocolor(reds)
                if (len(triangles) == 0):
                    return 4
            
                #posso checar por persistência no mapa mental para me certificar que
                #estou com o triângulo certo caso de alguma forma detect mais de um
            
                triangles= self.double_values(triangles)
                #dobro os valores porque a imagem de entrada tinha sido minimizada em 2
                self.triangle= Triangle(triangles[0])
            
                still_work_to_do= False
                return 0
            exit_code= scope()
            
            if (exit_code==0):
                True
                print("Triângulo encontrado!")
                #recon_debug(self.image_buffer[-1], self.Triangle)
            else:
                print("Nenhum triângulo encontrado, código "+str(exit_code))

            #self.recon_debug(self.image_buffer[-1], self.triangle)
            
        self.channel_open=True          
        self.image_buffer=[]
        
    def double_values(self, lst):
        for i in range(len(lst)):
            lst[i]*=2
            
        return lst
        
    def find_right_angled_triangles(self, alpha, beta, gamma):
         
        tolerance= 0.1
        
        triangles=[]
        for a in range(len(alpha)):
            ax, ay= alpha[a]
            for b in range(len(beta)):
                bx, by= beta[b]
                for g in range(len(gamma)):
                    gx, gy= gamma[g]
                    
                    distance1= (ax-bx)**2 + (ay-by)**2 #quadrado da distância
                    distance2= (bx-gx)**2 + (by-gy)**2
                    distance3= (ax-gx)**2 + (ay-gy)**2
                    
                    #d1+d2 deve ser d3
                    if(abs(distance1+distance2 - distance3) < tolerance*distance3):
                        triangles.append( (alpha[a], beta[b], gamma[g]) )
        return triangles
    
    def find_right_angled_triangles_monocolor(self, alpha):

        tolerance= 0.1

        triangles=[]

        combinations= itertools.combinations(alpha, 3);
        distance=[0]*3
        for combination in combinations:
                    
            distance[0]= (combination[0][0]-combination[1][0])**2 + (combination[0][1]-combination[1][1])**2 #quadrado da distância
            distance[1]= (combination[1][0]-combination[2][0])**2 + (combination[1][1]-combination[2][1])**2
            distance[2]= (combination[0][0]-combination[2][0])**2 + (combination[0][1]-combination[2][1])**2
            
            distance.sort()
            #d1+d2 deve ser d3
            if(abs(distance[0]+distance[1] - distance[2]) < tolerance*distance[2]):
                triangles.append( list(combination) )

        return triangles
        
    def recon_target(self, src, color):
        
        color2int={ "red": 2, "green": 1,"blue": 0}
        img= src[:,:,color2int[color]]
        rmv1= src[:,:,(color2int[color]+1)%3]
        rmv2= src[:,:,(color2int[color]+2)%3]

        #for i in range(len(img)):
        #    for j in range(len(img[i])):
        #        if ( ((src[i][j][color2int[color]]-20) <= src[i][j][(color2int[color]+1)%3]) or ((src[i][j][color2int[color]]-20) <= src[i][j][(color2int[color]+2)%3])):
        #            src[i][j][color2int[color]]= 0

        ret, test= cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
        ret, img= cv2.threshold(img, 150, 255, cv2.THRESH_BINARY) 

        #limpa rmv1
        ret, rmv1= cv2.threshold(rmv1, 100, 255, cv2.THRESH_BINARY_INV)
        ret, rmv1= cv2.threshold(rmv1, 1, 255, cv2.THRESH_TRUNC)

        #limpa rmv2
        ret, rmv2= cv2.threshold(rmv2, 100, 255, cv2.THRESH_BINARY_INV)
        ret, rmv2= cv2.threshold(rmv2, 1, 255, cv2.THRESH_TRUNC)

        for i in range(len(img)):
            for j in range(len(img[i])):
                img[i][j]*=rmv1[i][j]*rmv2[i][j]
        #depois setar valor mínimo embasado

        kernel= cv2.getStructuringElement(cv2.MORPH_RECT,(15,15))
        #posso alterar o kernel se achar que isso melhore minha detecção
        img= cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

        contours, hier= cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)   
        #contours= contours[0]
        #Tomar cuidado com essa linha, fiz ela seguindo o pyimagesearch mas n'ao estou certo dela

        centers=[]
        #for c in contours:
        #    mm= cv2.moments(c)
        #    x= int(mm["m10"]/mm["m00"])
        #    y= int(mm["m01"]/mm["m00"])
        
        #    centers.append((x, y))
        for shape in contours:
            x=0
            y=0
            for dot in shape:
                x+=dot[0][0]
                y+=dot[0][1]
            x/=len(shape)
            y/=len(shape)
            centers.append((x, y))


        return centers

    def recon_debug(self, img, triangle):
        if (not(triangle is None)):
            cv2.circle(img, triangle.red, 10, [255,0,0])
            cv2.circle(img, triangle.green, 10, [0,255,0])
            cv2.circle(img, triangle.blue, 10, [0,0,255])
            cv2.circle(img, triangle.center, 10, [255,255,255])
            #TODO: fazer os raios em func do triangulo


        cv2.imshow("Debug: Detect.recon", img)
        #para me mostrar um feed constante, waitkey deve ser zero?
        #lembrar de comentar ambas essas linhas para o release final


    def update(self):
        print("BANANA")
        RENEW_AGE= 30
        #checar as imagens só se meu triângulo for velho?
        if (not (self.triangle is None)):
            self.triangle.update()

            if (self.triangle.age%RENEW_AGE == 0):
                # Confere só a cada RENEW ciclos, se não reencontrar o triângulo
                #mantém na memória o triângulo velho
        
                self.recon()
        else:
            self.recon()

        self.memap.loadtriangle(self.triangle)



    def __init__(self, memap):

        rospy.Subscriber("/camera/image_raw", Image, self.capture, queue_size=10, buff_size = 2**24)
        ## é possível que queue_size e buff_size possam ser alterados para valores melhores

        self.channel_open=True
        self.memap= memap
        self.triangle= None
        self.bridge = CvBridge()
        self.image_buffer= []
