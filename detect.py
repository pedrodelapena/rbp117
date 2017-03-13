import rospy
from sensor_msgs.msg import Image

class Detect()

    def capture(image):
        self.image_buffer.append(image)
	    
	def recon():
	
	    #começar analisando da imagem mais recente, abortar se eu conseguir confirmação visual do que eu procuro
	    
	    still_work_to_do= True
	    
	    while(still_work_to_do or len(image_buffer) != 0)
	        #aqui vai o código de reconhecimento de imagem
	        def scope():
	            #inicialmente tratar a imagem para que seja mais rápido/simples de trabalhar
	        
	            #a cada check de consistência dar um return se falhar
	            
	            #check1- Procurar por Vermelhos significativos
	                reds= []
	                
	                if (len(reds) == 0):
	                    return
	            #check2- Procurar por Verdes significativos
	                greens= []
	                
	                if (len(greens) == 0):
	                    return
	            #check3- Procurar por Azuis significativos
	                blues= []
	                
	                if (len(blues) == 0):
	                    return
	            #check4- Procurar por triângulos significativos
	            
	            #check5- Refinar para garantir que estamos certos de que esse é o alvo
	            
	            #por fim, anotar as coordenadas desse reconhecimento em alguma memória
                still_work_to_do= False
	        scope()
	        
	        image_buffer.pop(-1)
	        #if step
	        
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
