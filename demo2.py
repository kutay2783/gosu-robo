import numpy as np
import cv2
import Adafruit_BBIO.PWM as PWM

#mavikapakLower = (86, 120, 73)
#kapakUpper = (106, 255, 255)
kapakLower = (6, 3, 83)
kapakUpper = (48, 255, 255)
### GPIO ###
#PWM.start(channel, duty, freq=2000, polarity=0)
pwmA1="P9_21"
pwmA2="P9_22"
pwmB1="P9_14"
pwmB2="P9_16"
pwmC="P8_13"
pwmS=13
PWM.start(pwmA1,50)
PWM.start(pwmA2,0)
PWM.start(pwmB1,0)
PWM.start(pwmB2,50)
PWM.start(pwmC,13,50,0)
xexloc=160
xloc=160
yloc=120
n=1
x=1

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
		
		if radius > 10:
			if xloc <130:
				pwmS=pwmS*(1.0-(155-xloc)/2000)
        		elif xloc<155:
            			pwmS=pwmS*(1.0-(155-xloc)/4000)
        		elif xloc>165:
            			pwmS=pwmS*(1.0-(xloc-165)/4000)#465)
			elif xloc>190
				pwmS=pwmS*(1.0-(xloc-165)/2000) 
		elif xexloc<155:
			pwmS=pwmS*(1.0-(xloc-165)/4000)
		elif xexloc>165:
			pwmS=pwmS*(1.0-(155-xloc)/4000) 
			
	if pwmS<4:
		PWM.set_duty_cycle(pwmA2,50)
		PWM.set_duty_cycle(pwmB1,50)
		break
		#print(pwmL)
        	#print(pwmR)
       	PWM.set_duty_cycle(pwmC, pwmS)
	xexloc=xloc
	if n==20:
		print(x)
		x=x+1
		n=1
	elif:
		n=n+1	

	#else:
		#if xloc>280:
            	#	PWM.set_duty_cycle(pwmA,100.0)
		#elif xloc<40:
           	# 	PWM.set_duty_cycle(pwmB,100.0)
