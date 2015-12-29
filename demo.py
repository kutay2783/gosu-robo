import numpy as np
import cv2
import Adafruit_BBIO.PWM as PWM

kapakLower = (86, 120, 73)
kapakUpper = (106, 255, 255)
### GPIO ###
#PWM.start(channel, duty, freq=2000, polarity=0)
pwmA1="P9_21"
pwmA2="P9_22"
pwmB1="P9_14"
pwmB2="P9_16"
pwmC="P9_42"
PWM.start(pwmA1, 50)
PWM.start(pwmA2, 50)
PWM.start(pwmB1, 50)
PWM.start(pwmB2, 50)
PWM.start(pwmC,50,50,0)

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
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	xloc=160
    	yloc=120
    	#mmnt = cv2.moments(mask)
    	if len(cnts) > 0:
    		c= max(cnts, key=cv2.contourArea)
		((xloc, yloc), radius) = cv2.minEnclosingCircle(c)
		print('Enclosing circle:',xloc,yloc,radius)
		M = cv2.moments(c)
    	#if mmnt['m00']!=0:
        	xloc = M['m10']/M['m00']
        	yloc = M['m01']/M['m00']
        	
		##print('Moment:',M['m00'])
		print('Moment:',xloc,yloc)
        	#if yloc<120:
           	#	pwmL=(120.0-yloc)*(5.0/6.0)
            	#	pwmR=pwmL
        	#else: 
           	#	pwmL=0
            	#	pwmR=0
		
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
