import numpy as np
import argparse, cv2, time, serial
from ardFunc import roundCW, startCom, roundCCW, goStraight, callHits,incLeft,incRight, stopGoStraight
from collections import deque
from serial import Serial
import camera_deneme
import Decision  
import math

ser = Serial('/dev/ttyUSB0',9600)

def movement():
        global radiusFirst
        global radiusLast
	global hits
	hits=0
        radiusFirst=32		
        initialize=initStep2Robot()
        if initialize==-1:
                return -1
        constant=107
        goStraight(constant)        
        	
def initStep2Robot():
        global radiusFirst
        global xRobLast
        print "initStep locARR0", Decision.locationArray[0] , Decision.locationArray[1]
        if (Decision.locationArray[1]>Decision.locationArray[0]):
                focusRobotSmall=0
        else:
                focusRobotSmall=1
        if Decision.locationArray[4]<=(Decision.locationArray[focusRobotSmall]+camera_deneme.CAMERA_CONS/2):
                if Decision.locationArray[4]>Decision.locationArray[focusRobotSmall]:
                        rotate=(Decision.locationArray[4]-Decision.locationArray[focusRobotSmall])        
                        Decision.stepperCCW(rotate,1)
                        Decision.locationArray[4]-= rotate
                        if(Decision.locationArray[4]>camera_deneme.CAMERA_CONS):
                                Decision.locationArray[4]=locationArray[4]%camera_deneme.CAMERA_CONS
                else:
                        rotate = (Decision.locationArray[focusRobotSmall]-Decision.locationArray[4])
                        Decision.stepperCW(rotate,1)
                        Decision.locationArray[4]+= rotate
                        if(Decision.locationArray[4]>camera_deneme.CAMERA_CONS):
                                Decision.locationArray[4]=locationArray[4]%camera_deneme.CAMERA_CONS
        else:
                rotate=(Decision.locationArray[focusRobotSmall]-Decision.locationArray[4])%camera_deneme.CAMERA_CONS
                Decision.stepperCW(rotate,1)
                Decision.locationArray[4]+= rotate
                if(Decision.locationArray[4]>camera_deneme.CAMERA_CONS):
                        Decision.locationArray[4]=Decision.locationArray[4]%camera_deneme.CAMERA_CONS                       
	
        print"rotate :",rotate
	while 1:
                (xrbt4Init,radius4Init) = camera_deneme.getCameraForRobots()
                print"xrobot: init step",xrbt4Init
                if xrbt4Init==-80:
                        print "init step hatasi"
                        return -1
                elif xrbt4Init>-4 and xrbt4Init<4:
                        print "robot detected ez initStep",xrbt4Init
                        radiusFirst=radius4Init
                        xRobLast=xrbt4Init
                        break
                else:
                        kp=0.5
                        rotate=kp*xrbt4Init
                        if rotate>0:
                                rotate=int(abs(rotate)*camera_deneme.DC2CAMERA_RATIO)
				if rotate<2:
					rotate=1
                                #Decision.stepperCW(rotate,1)
                                roundCW(rotate)
                                Decision.locationArray[0]=(Decision.locationArray[0]-rotate)%camera_deneme.CAMERA_CONS        
                                Decision.locationArray[1]=(Decision.locationArray[1]-rotate)%camera_deneme.CAMERA_CONS
                                Decision.locationArray[2]=(Decision.locationArray[2]-rotate)%camera_deneme.CAMERA_CONS
                                #Decision.locationArray[4]+= rotate
                                if(Decision.locationArray[4]>camera_deneme.CAMERA_CONS):
                                        Decision.locationArray[4]=Decision.locationArray[4]%camera_deneme.CAMERA_CONS
                                print "case5 cw initstep2",rotate
                        elif rotate<0:
				
                                rotate=int(abs(rotate)*camera_deneme.DC2CAMERA_RATIO)
				if rotate<2:
					rotate=1
				
                                roundCCW(rotate)
                                Decision.locationArray[0]=(Decision.locationArray[0]-rotate)%camera_deneme.CAMERA_CONS        
                                Decision.locationArray[1]=(Decision.locationArray[1]-rotate)%camera_deneme.CAMERA_CONS
                                Decision.locationArray[2]=(Decision.locationArray[2]-rotate)%camera_deneme.CAMERA_CONS
                                #Decision.stepperCCW (rotate,1)
                                #Decision.locationArray[4]-= rotate
                                if(Decision.locationArray[4]>camera_deneme.CAMERA_CONS):
                                        Decision.locationArray[4]=Decision.locationArray[4]%camera_deneme.CAMERA_CONS
                                print "case6 ccw initstep2",rotate
                
                
	return 1       
             
def getAngleStepper(xRobot):## orta nokta hatasi var!!!!!!
        
	return xRobot+Decision.locationArray[4];

def radius2Meter(radius): ## bura dolcak !!!!!!!!!!!!
	distMet= radiusdist_guess=(0.0000165909)*((radius)**4)-(0.00375541)*((radius)**3)+(0.318206)*((radius)**2)-(12.6395)*radius+236.597              
	return distMet
	

def table4Angle(angle):
        if angle>(camera_deneme.CAMERA_CONS/4):
                angle =(camera_deneme.CAMERA_CONS/2)-angle 
#	radius=((4.39107)*(10**-6)*(angle**4))-(0.0013749)*((angle)**3)+(0.151729)*((angle)**2)-(6.27768)*angle+116.197
	#polulu radius
	angle=(angle*200)/512
	radius= (0.00013055)*((angle)**4)-(0.0162049)*((angle)**3)+(0.706096)*((angle)**2)-(11.0045)*angle+84.6914                   
        print "angle,radius from table",angle,radius
        return int (radius)
	
	


def getCameraForRobots ():
        global xRobot
        global radius
        global radiusFirst
        global hits
	count=0
        camera = cv2.VideoCapture(0)
#        camera.set(3,320)
#        camera.set(4,240)
        radi=-80
        xRob=-80
	robotLower=camera_deneme.robotLower
	robotUpper=camera_deneme.robotUpper	
	#time.sleep(1)        
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
                cntsRobot = cv2.findContours(maskRobot.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]        
                if len(cntsRobot) > 0:
                        c = max(cntsRobot, key=cv2.contourArea)
                        ((xRob, y), radi) = cv2.minEnclosingCircle(c)
                        #dist_guess=(0.000530837)*((radius)**4)-(0.0646349)*((radius)**3)+(2.97707)*((radius)**2)-(63.2866)*radius+586.071
                        if radi < 10:		    
                                xRob=-80    
                else:
                        xRob=-80
                cameraAngle=360/camera_deneme.CAMERA_CONS
                pixel4Slot =int(640//(40/cameraAngle))
                if xRob !=-80:
	                xRob= int((xRob-(320-pixel4Slot//2))//pixel4Slot)
	                print "camera4robots xRob",xRob
                if xRob==-80:
                        print"xrobot ERROR get camera"
                lock.acquire()
                xRobot=xRob
                radius=radi
                lock.release()
                print"semapreleaase"
#		synevent.set()
 #               semapMove.release()
		count+=1
                if (radius<radiusFirst and hits>30) :#or count>50 :
                        camera.release()
                        cv2.destroyAllWindows()
                        break
        
        
	
	
	
	
	
	
	
	
	
	
	
	
	

