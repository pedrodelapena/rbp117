import rospy
from sensor_msgs.msg import Image
import cv2

class Detect()

    def capture(image):
        try:
            image= bridge.imgmsg_to_cv2(image, "bgr8")
            self.image_buffer.append(image)
            
	        cv2.imshow("visual", cv_image)
		    cv2.waitKey(0)
		    #para me mostrar um feed constante, waitkey deve ser zero?
		    #lembrar de comentar ambas essas linhas para o release final
		    
		except CvBridgeError as e:
		    print("Erro em Detect: "+ e)
		    
	def recon():
	
	    #começar analisando da imagem mais recente, abortar se eu conseguir confirmação visual do que eu procuro
	    
	    still_work_to_do= True
	    
	    while(still_work_to_do or len(self.image_buffer) != 0)
	        def scope():
	        
	            src=self.image_buffer[-1]
	            self.image_buffer.pop(-1)
	            #resizear a imagem aqui
	            src = cv2.GaussianBlur(src, (5, 5), 0)
	            
                reds= Detect.recon_shape(src, "red")
                if (len(reds) == 0):
                    return
                greens= Detect.recon_shape(src, "green")
                if (len(greens) == 0):
                    return
                blues= Detect.recon_shape(src, "blue")
                if (len(blues) == 0):
                    return
                    
	            #check4- Procurar por triângulos significativos
	            
	            #check5- Refinar para garantir que estamos certos de que esse é o alvo
	            
	            #por fim, anotar as coordenadas desse reconhecimento em alguma memória
                still_work_to_do= False
	        scope()
	        
        image_buffer=[]
        
    def recon_red(src, color):
        
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
    
	        
	def update(self):
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
