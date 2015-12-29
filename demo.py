import numpy as np
import cv2
import Adafruit_BBIO.PWM as PWM

kapakLower = (86, 120, 73)
kapakUpper = (106, 255, 255)
### GPIO ###
#PWM.start(channel, duty, freq=2000, polarity=0)
pwmA="P9_22"
pwmB="P9_21"
PWM.start(pwmA, 50)
PWM.start(pwmB, 50)

camera = cv2.VideoCapture(0)
camera.set(3,320)
camera.set(4,240)
kernel = np.ones((5,5),np.uint8)

while(1):
	_, frame = camera.read()
#	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, kapakLower, kapakUpper)
	mask = cv2.erode(mask, kernel, iterations=1)
	mask = cv2.dilate(mask, kernel, iterations=1)
	
	xloc=160
    	yloc=120
    	mmnt = cv2.moments(mask)
    	if mmnt['m00']!=0:
        	xloc = mmnt['m10']/mmnt['m00']
        	yloc = mmnt['m01']/mmnt['m00']
        	#print(xloc,yloc)
		print(mmnt['m00'])
        	if yloc<120:
           		pwmL=(120.0-yloc)*(5.0/6.0)
            		pwmR=pwmL
        	else: 
           		pwmL=0
            		pwmR=0
		
        	if xloc<155:
            		pwmL=pwmL*(1.0-(155-xloc)/465)
        	if xloc>165:
            		pwmR=pwmR*(1.0-(xloc-165)/465)#465)
		
		#print(pwmL)
        	#print(pwmR)
       	 	PWM.set_duty_cycle(pwmA, int(pwmL))
        	PWM.set_duty_cycle(pwmB, int(pwmR))

	else:
		if xloc>280:
            		PWM.set_duty_cycle(pwmA,100.0)
		elif xloc<40:
           	 	PWM.set_duty_cycle(pwmB,100.0)
