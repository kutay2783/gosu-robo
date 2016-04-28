
from collections import deque
import numpy as np
import argparse, cv2, time
#from ardFunc import roundCW, startCom, roundCCW, goStraight, callHits
import RPi.GPIO as GPIO
import threading
global degrees

def stepTurn(dir,degrees):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17,GPIO.OUT)
	GPIO.setup(27,GPIO.OUT)
        WaitTime = 10/float(1000)
	if dir==0:
		GPIO.output(27,True)
	else:
		GPIO.output(27,False)
	while True:
		GPIO.output(17, True)
		time.sleep(WaitTime)
		GPIO.output(17, False)
		time.sleep(WaitTime)
		degrees=degrees-1
		if degrees==0:
			break;

def turnCamera():

        global degrees
        GPIO.setmode(GPIO.BCM)
	GPIO.setup(17,GPIO.OUT)
	GPIO.setup(27,GPIO.OUT)
	GPIO.setup(22,GPIO.OUT)
	GPIO.output(22, True)
        WaitTime = 15/float(1000)
	GPIO.output(27,True)
	degrees=0
	
	while True:
                GPIO.output(17, True)
                time.sleep(WaitTime)
                GPIO.output(17, False)
                time.sleep(WaitTime)
                degrees=degrees+1
                if degrees==100:
                        GPIO.output(27,False)
                        break;
        while True:
                GPIO.output(17, True)
                time.sleep(WaitTime)
                GPIO.output(17, False)
                time.sleep(WaitTime)
                degrees=degrees-1
                if degrees==0:
                        break;
        GPIO.output(22, False)

def getCamera():      
        global degrees
	
        robotLower = (10, 145, 140)
        robotUpper = (46, 255, 255)
        targetLower = (60, 95, 65)
        targetUpper = (91, 212, 255)
        found=0
        not_found=0
        temp=0
        temp2=0
        radius=0

        camera = cv2.VideoCapture(0)
        camera.set(3,320)
        camera.set(4,240)
        time1=time.time()
        #camera.set(5,60)
        dist_guess=0
##################################################
 
        while True:
                (grabbed, frame)=camera.read()
                if frame!=None:
                        break
        while True:
        	(grabbed, frame) = camera.read()
        	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        	maskRobot = cv2.inRange(hsv, robotLower, robotUpper)
        	maskRobot = cv2.erode(maskRobot, None, iterations=2)
        	maskRobot = cv2.dilate(maskRobot, None, iterations=2)
        	maskTarget = cv2.inRange(hsv, targetLower, targetUpper)
        	maskTarget = cv2.erode(maskTarget, None, iterations=2)
        	maskTarget = cv2.dilate(maskTarget, None, iterations=2)
        	
        	cntsRobot = cv2.findContours(maskRobot.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
        #	print(cntsRobot)
        	center = None
        	if len(cntsRobot)>0:
                        c = max(cntsRobot, key=cv2.contourArea)
                        ((xRobot, y), radius) = cv2.minEnclosingCircle(c)
                        center=(int(xRobot), int(y))
                        dist_rad=(0.0000165909)*((radius)**4)-(0.00375541)*((radius)**3)+(0.318206)*((radius)**2)-(12.6395)*radius+236.597
                        if (radius > 10):
                                cv2.circle(frame, center, int(radius),(0, 0, 0), 2)
                                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                                print('xRobot: ', xRobot," robotMeter: ",dist_rad, degrees)
                                print degrees
                        else:
                                xRobot=-10
                else:
                        xRobot=-10


                
                
                
#################################################################################################
                cntsTarget = cv2.findContours(maskTarget.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
        	center = None
        	if len(cntsTarget) > 0:
                        c = max(cntsTarget, key=cv2.contourArea)
                        xTarget,yTarget,wTarget,hTarget= cv2.boundingRect(c)
                        xTarget=xTarget+(wTarget/2)
                        center=(int(xTarget), int(yTarget))
                        xTarget=xTarget+(wTarget/2)
                        dist_guess=int((8.71591)*(10**-8)*((wTarget)**4)-(0.0000686939)*((wTarget)**3)+(0.0200612)*((wTarget)**2)-(2.72701)*wTarget+183.004)
                        if (wTarget > 10 and xTarget>150 and xTarget<170):
                                cv2.rectangle(maskTarget,(xTarget,yTarget),(xTarget+wTarget,yTarget+hTarget),(166,166,166),2)
        			found=found+1
                                print("xTarget: ",int (xTarget)," targetMeter: ",dist_guess, degrees)
                                print degrees
                        else:
                                xTarget=-10
                else:
                        xTarget=-10

                cv2.imshow("Frame", frame)
                cv2.imshow("mask", maskRobot)
                cv2.imshow("mask", maskTarget)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                        break
  
        camera.release()
        cv2.destroyAllWindows()
        if xTarget!=-10:
                xTarget=(xTarget-320)//80
                if xTarget<0:
                        xTarget=xTarget-1
                        
        if xRobot!=-10:
                xRobot=(xRobot-320)//80
                if xRobot<0:
                        xRobot=xRobot-1
        print ("xRobot:", xRobot,"radiusrobot:",int (radius), "xTarget:" , xTarget, " targetMeter: ", dist_guess, )
        GPIO.output(22, False)
        return(xRobot,xTarget,dist_guess)

getCamera=threading.Thread(target=getCamera)
getCamera.start()
time.sleep(0.5)
turnCamera=threading.Thread(target=turnCamera)
turnCamera.start()

