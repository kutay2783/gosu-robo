
from collections import deque
import numpy as np
import argparse, cv2, time
from ardFunc import roundCW, startCom, roundCCW, goStraight, callHits

def camera():
        kapakLower = (10, 145, 140)
        kapakUpper = (46, 255, 255)
        found=0
        not_found=0
        temp=0
        temp2=0
        camera = cv2.VideoCapture(0)
        camera.set(3,320)
        camera.set(4,240)
        camera.set(5,10)
        x_list=range(10)
        # keep looping
        for i in xrange(10):
        	(grabbed, frame) = camera.read()
        	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        	
        	mask = cv2.inRange(hsv, kapakLower, kapakUpper)
        	mask = cv2.erode(mask, None, iterations=2)
        	mask = cv2.dilate(mask, None, iterations=2)
        	
        	cnts = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
        #	print(cnts)
        	center = None
        	if len(cnts) > 0:
                        c = max(cnts, key=cv2.contourArea)
                        ((x, y), radius) = cv2.minEnclosingCircle(c)
                        center=(int(x), int(y))
                        dist_guess=(0.000530837)*((radius)**4)-(0.0646349)*((radius)**3)+(2.97707)*((radius)**2)-(63.2866)*radius+586.071
                        if radius > 10:
        			found=found+1
                                x_list[i]=x
                                print('x: ',int (x)," y: ",int (y)," distance: ",dist_guess)
                        else:
                                x=-1
                else:
                        x=-1
                              
        camera.release()
        cv2.destroyAllWindows()
        return(x)

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
