
from collections import deque
import numpy as np
import argparse, cv2, time
from ardFunc import roundCW, startCom, roundCCW, goStraight, callHits

def getCamera():
        time1=time.time()
        #global camera
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
        #camera.set(3,320)
        #camera.set(4,240)
        #camera.set(5,10)
        dist_guess=0
        xRobot_list=range(10)
        xTarget_list=range(10)
        # keep looping
        while True:
                (grabbed, frame)=camera.read()
                if frame!=None:
                        break
        for i in xrange(5):
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
        #	print(cntsRobot)
        	center = None
        	if len(cntsRobot) > 0:
                        c = max(cntsRobot, key=cv2.contourArea)
                        ((xRobot, y), radius) = cv2.minEnclosingCircle(c)
                        center=(int(xRobot), int(y))
                        #dist_guess=(0.000530837)*((radius)**4)-(0.0646349)*((radius)**3)+(2.97707)*((radius)**2)-(63.2866)*radius+586.071
                        if radius > 10:
        			found=found+1
                                xRobot_list[i]=xRobot
                                print('xRobot: ', xRobot," observation:",i)
                        else:
                                xRobot=-10
                else:
                        xRobot=-10
##################################################################################################
                cntsTarget = cv2.findContours(maskTarget.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
        #	print(cntsTarget)
        	center = None
        	if len(cntsTarget) > 0:
                        c = max(cntsTarget, key=cv2.contourArea)
                        xTarget,yTarget,wTarget,hTarget= cv2.boundingRect(c)
                        xTarget=xTarget+(wTarget/2)
                        center=(int(xTarget), int(yTarget))
                        dist_guess=int((8.71591)*(10**-8)*((wTarget)**4)-(0.0000686939)*((wTarget)**3)+(0.0200612)*((wTarget)**2)-(2.72701)*wTarget+183.004)
                        if wTarget > 10:
                                xTarget=xTarget+(wTarget/2)
        			found=found+1
                                xTarget_list[i]=xTarget
                                print("xTarget: ",int (xTarget)," targetMeter: ",dist_guess," observation:",i)
                        else:
                                xTarget=-10
                else:
                        xTarget=-10
        
                
                              
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
        time2=time.time()
        #print time2-time1
        time1=0
        time2=0
        return(xRobot,xTarget,dist_guess)

def findTarget():
        camera_x_diff=100 #dummy value
        while(abs(camera_x_diff)>5):
            camera_x=int(camera())
            camera_x_diff=camera_x-160
            print "Target position: ",camera_x
            print "Target distance from center in x axis: ",camera_x_diff
            if camera_x==(-1):
                roundCW(50)
            if camera_x!=(-1) and camera_x_diff>0:
                roundCW(camera_x_diff/2)
            if camera_x!=(-1) and camera_x_diff<0:
                roundCCW(camera_x_diff*(-1)/2)


