
from collections import deque
import numpy as np
import argparse, cv2, time
def getCamera():  
	global CAMERA_CONS
	global WHEEL_CONS 
	global DC2CAMERA_RATIO
        time.sleep(1)
	CAMERA_CONS= 512.0      ## for unipolar stepper motor
	#CAMERA_CONS= 200.0     ## for POLOLU stepper motor
	WHEEL_CONS = 51.0
	DC2CAMERA_RATIO = WHEEL_CONS/CAMERA_CONS
	
	global robotLower 
	global robotUpper
        robotLower = (10, 145, 140)
        robotUpper = (46, 255, 255)
        targetLower = (70, 46, 56)
        targetUpper = (85, 255, 245)
        distRobot=0
        radius=0
	dist_guess=0
        camera = cv2.VideoCapture(0)
        #camera.set(3,320)
        #camera.set(4,240)
               
        while True:
            (grabbed, frame)=camera.read()
            if frame!=None:
                break
        
        (grabbed, frame) = camera.read()
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        maskTarget = cv2.inRange(hsv, targetLower, targetUpper)
        maskTarget = cv2.erode(maskTarget, None, iterations=2)
        maskTarget = cv2.dilate(maskTarget, None, iterations=2)
        	
        maskRobot = cv2.inRange(hsv, robotLower, robotUpper)
        maskRobot = cv2.erode(maskRobot, None, iterations=2)
        maskRobot = cv2.dilate(maskRobot, None, iterations=2)
        	
        cntsRobot = cv2.findContours(maskRobot.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]        
        if len(cntsRobot) > 0:
            c = max(cntsRobot, key=cv2.contourArea)
            ((xRobot, y), radius) = cv2.minEnclosingCircle(c)
            distRobot=round((0.000530837)*((radius)**4)-(0.0646349)*((radius)**3)+(2.97707)*((radius)**2)-(63.2866)*radius+586.071)
            if radius < 10:     
		xRobot=-80
        else:
            xRobot=-80
##################################################################################################
        cntsTarget = cv2.findContours(maskTarget.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
        #   print(cntsTarget)
        if len(cntsTarget) > 0:
            c = max(cntsTarget, key=cv2.contourArea)
            xTarget,yTarget,wTarget,hTarget= cv2.boundingRect(c)
            xTarget=xTarget+(wTarget/2)
            dist_guess=round((8.71591)*(10**-8)*((wTarget)**4)-(0.0000686939)*((wTarget)**3)+(0.0200612)*((wTarget)**2)-(2.72701)*wTarget+183.004)
            if wTarget > 10:
                xTarget=xTarget+(wTarget/2)				
            else:
                xTarget=-80
        else:
            xTarget=-80                
                              
        camera.release()
        cv2.destroyAllWindows()
	cameraAngle=360/CAMERA_CONS
	pixel4Slot =(640/(40/cameraAngle))
        if xTarget!=-80:
            xTarget= round((xTarget-(320-pixel4Slot//2))//pixel4Slot)	                        
        if xRobot!=-80:
            xRobot= round((xRobot-(320-pixel4Slot//2))//pixel4Slot)           
        print ("xRobot:", xRobot,"radiusrobot:",int (radius), "xTarget:" , xTarget, " targetMeter: ", dist_guess, )
        return(xRobot,xTarget,dist_guess,distRobot)

def getCameraForRobots ():
        camera = cv2.VideoCapture(0)
        #camera.set(3,320)
        #camera.set(4,240)
        radius=-80
        xRobot=-80
	global robotLower
	global robotUpper	
	time.sleep(1)
        while True:
                (grabbed, frame)=camera.read()
                if frame!=None:
                        break
        
        (grabbed, frame) = camera.read()
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)								
        maskRobot = cv2.inRange(hsv, robotLower, robotUpper)
        maskRobot = cv2.erode(maskRobot, None, iterations=2)
        maskRobot = cv2.dilate(maskRobot, None, iterations=2)					
        cntsRobot = cv2.findContours(maskRobot.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]        
        if len(cntsRobot) > 0:
                c = max(cntsRobot, key=cv2.contourArea)
                ((xRobot, y), radius) = cv2.minEnclosingCircle(c)
                #dist_guess=round((0.000530837)*((radius)**4)-(0.0646349)*((radius)**3)+(2.97707)*((radius)**2)-(63.2866)*radius+586.071)
                if radius < 10:		    
                        xRobot=-80    
        else:
                xRobot=-80

        if xRobot !=-80:
                cameraAngle=360/CAMERA_CONS
                pixel4Slot =(640/(40/cameraAngle))
                xRobot= round((xRobot-(320-pixel4Slot/2))/pixel4Slot)
        if xRobot==-80:
                print"xrobot ERROR get camera"
	camera.release()
        cv2.destroyAllWindows()        
	return xRobot,int(radius)
							


								
								
								
								
								
								
								
								
								
								
								
								
								


