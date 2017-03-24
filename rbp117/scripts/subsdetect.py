import rospy
from sensor_msgs.msg import Image
import cv2

from triangle import Triangle

import itertools

class Detect()

    def capture(self, image):
        try:
            image= bridge.imgmsg_to_cv2(image, "bgr8")
            self.image_buffer.append(image)
		    
		except CvBridgeError as e:
		    print("Erro em Detect.capture: "+ e)
		    
	def recon(self):
	
	    #começar analisando da imagem mais recente, abortar se eu conseguir confirmação visual do que eu procuro
	    #TODO opcional: analisar a idade das imagens e começar meu triângulo com uma certa idade proporcional em vez de zero
	    
	    still_work_to_do= True
	    
	    while(still_work_to_do or len(self.image_buffer) != 0)
	        def scope():
	        
	            src=self.image_buffer[-1]
	            cv2.resize(src, None,fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
	            src = cv2.GaussianBlur(src, (5, 5), 0)
	            
                reds= Detect.recon_target(src, "red")
                if (len(reds) == 0):
                    return 1
                greens= Detect.recon_target(src, "green")
                if (len(greens) == 0):
                    return 2
                blues= Detect.recon_target(src, "blue")
                if (len(blues) == 0):
                    return 3
                    
                triangles= find_right_angled_triangles(reds, greens, blues)
                if (len(triangles) == 0):
                    return 4
                
                #posso checar por persistência no mapa mental para me certificar que
                #estou com o triângulo certo caso de alguma forma detect mais de um
                
                triangles= double_values(triangles)
                #dobro os valores porque a imagem de entrada tinha sido minimizada em 2
                self.triangle= Triangle(triangles[0])
	            
                still_work_to_do= False
                return 0
	        exit_code= scope()
	        
	        if (exit_code==0):
	            recon_debug(self.image_buffer[-1], self.Triangle)
            else():
                print("Nenhum triângulo encontrado, código "+str(exit_code))
	        self.image_buffer.pop(-1)
	        
        image_buffer=[]
        
    def double_values(lst):
        for i in range(len(lst)):
            lst[i]*=2
            
        return lst
        
    def find_right_angled_triangles(alpha, beta, gamma):
        
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
                        
    def filter_right_angled(triangle)
        #De mathworld.wolfram: For an isosceles right triangle with side lengths a, the hypotenuse has length sqrt(2)a
        tolerance= 0.1
        
        
    def recon_target(src, color):
        
        color2int={
            "red": 2,
            "green": 1,
            "blue": 0
        }
	    img= src[:,:,color2int[color]]

	    ret, img = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
	    #depois setar valor mínimo embasado
	    
	    kernel= cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
	    #posso alterar o kernel se achar que isso melhore minha detecção
	    img= cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
	    
	    contours= cv2.findContours(img.copy(), CV_RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)	
        contours= contours[0]
        #Tomar cuidado com essa linha, fiz ela seguindo o pyimagesearch mas n'ao estou certo dela
        
        centers=[]
        for c in contours:
            mm= cv2.moments(c)
            x= int(mm["m10"]/mm["m00"])
            y= int(mm["m01"]/mm["m00"])
            
            centers.append((x, y))

	    return centers
	    
    def recon_debug(img, target, center, distance, code):
        
        cv2.circle(img, triangle.red, distance/2, **RED**)
        cv2.circle(img, triangle.green, distance/2, **Green**)
        cv2.circle(img, triangle.blue, distance/2, **RED**)
        cv2.circle(img, triangle.center, (1.0 + 2.0**(1/2))*distance/2, **WHITE**)
        #TODO: fazer as distancias em func do triangulo
        
        
        cv2.imshow("Debug: Detect.recon", img)
        cv2.waitKey(0)
        #para me mostrar um feed constante, waitkey deve ser zero?
        #lembrar de comentar ambas essas linhas para o release final
    
	        
	def update(self):
	    
	    #checar as imagens só se meu triângulo for velho?
	    if (not (self.triangle is None)):
	        self.triangle.update()
	        if (self.triangle.age%RENEW_AGE == 0):
	            # Confere só a cada RENEW ciclos, se não reencontrar o triângulo
	            #mantém na memória o triângulo velho
	            
	            self.recon()
	    else:
	        self.recon()
	        


    def __init__(self, memap):
    
        rospy.Subscriber("/camera/image_raw", Image, self.capture, queue_size=10, buff_size = 2**24)
        ## é possível que queue_size e buff_size possam ser alterados para valores melhores
        self.memap= memap
        self.triangle= None