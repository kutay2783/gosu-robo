import numpy as np
import argparse, cv2, time, serial
from ardFunc import roundCW, startCom, roundCCW, goStraight, callHits,incLeft,incRight, stopGoStraight
from collections import deque
from serial import Serial
import camera_deneme
import Decision  
import math
import threading
ser = Serial('/dev/ttyUSB0',9600)
maxconnections=1
semapMove=threading.Semaphore (value=1)
event =threading.Event()
synevent=threading.Event()
lock=threading.Lock()
lock4RadiusFirst=threading.Lock()
def movement():
        global radiusFirst
        global radiusLast
	global hits
	hits=0
        event.clear()
        radiusFirst=32
		
        initialize=initStep2Robot()
        if initialize==-1:
                return -1
        constant=115
	hits=0
	(hitsLeft,hitsRight) = callHits()
        hits = callHits()
        print "call hits",hitsLeft,"right",hitsRight

	radiusLast=radiusFirst
        goStraight(constant)        
         
        
        gCFR= threading.Thread(target=getCameraForRobots)
        gCFR.start()
        time.sleep(1)
        roM=threading.Thread(target=restOfMovement)
        roM.start()
        event.wait()
def restOfMovement():
        global radiusFirst
        global xRobot
        global radius
        global hits
        global xRobLast
        while True:
                synevent.wait()
                time.sleep(0.5)
                lock.acquire()
                xRob=xRobot
                radi=radius
                lock.release()
                if (radi<radiusFirst and hits>30):
			print radi
			stopGoStraight()
			event.set()
			break;
                print "movament camera enable"
                (hitsLeft,hitsRight) = callHits()
                hits = callHits()
                print "call hits",hitsLeft,"right",hitsRight
                angleStepper=getAngleStepper(xRob)
                print "angle stepper",angleStepper
                hits = (hitsLeft+hitsRight)/2
                straightenPID(radius,angleStepper,hits)		
                step2Robot(xRob,angleStepper)
                print"semap acquire"
                semapMove.acquire()
	

def straightenPID(radius,angle,distanceInitial):	
	global radiusLast
	setLimit=5
	Kp=0.04
	Kd=0.005
	
	radiusTable=table4Angle(angle)
	correctionValue =int(Kp*(radius-radiusTable)+Kd*(radius-radiusLast))
	if correctionValue>setLimit:
                correctionValue=setLimit
        elif correctionValue<(-setLimit):
                correctionValue=-setLimit
	print "angle radius PID",angle,radius
	print "correction value",correctionValue
	if(correctionValue > 0):
                print "inc Right",correctionValue
                incRight(abs(correctionValue))
	elif (correctionValue < 0):
                print "inc Left",correctionValue
		incLeft(abs(correctionValue))
	radiusLast=radius	
	synevent.clear()
	
def step2Robot(xRob,angle):
        global xRobLast
	kp=1.0
	kd=0.01
	eConst=1
	print"step2Robot xRobot",xRob
	if xRobot==-80:
                print "step2Robot error"
        
	rotate=int(round(2.5+kp*xRob+kd*(xRob-xRobLast)))
	if rotate>10:
                rotate=10
        elif rotate<-10:
                rotate=-10
	if rotate>0:
                Decision.stepperCW(rotate,1)
                Decision.locationArray[4]-= rotate
                print"step2Robot CCW",rotate
                if(Decision.locationArray[4]>camera_deneme.CAMERA_CONS):
                        Decision.locationArray[4]=locationArray[4]%camera_deneme.CAMERA_CONS
	elif rotate<0:
                rotate=abs(rotate)
		Decision.stepperCCW (rotate,1)
		Decision.locationArray[4]+= rotate
		print"step2Robot CW",rotate
                if(Decision.locationArray[4]>camera_deneme.CAMERA_CONS):
                        Decision.locationArray[4]=locationArray[4]%camera_deneme.CAMERA_CONS
	
	
	
def initStep2Robot():
        global radiusFirst
        global xRobLast
        print "initStep locARR0,1,4:", Decision.locationArray[0] , Decision.locationArray[1],Decision.locationArray[4]
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
                        print "robot detected ez initStep"
                        radiusFirst=radius4Init
                        xRobLast=xrbt4Init
                        break
                else:
                        kp=0.5
                        rotate=kp*xrbt4Init
                        if rotate>0:
                                rotate=int(round(abs(rotate)*camera_deneme.DC2CAMERA_RATIO))
				if rotate<2:
					rotate=2
                                #Decision.stepperCW(rotate,1)
                                roundCW(rotate)
                                Decision.locationArray[0]=(Decision.locationArray[0]-rotate)%camera_deneme.CAMERA_CONS        
                                Decision.locationArray[1]=(Decision.locationArray[1]-rotate)%camera_deneme.CAMERA_CONS
                                Decision.locationArray[2]=(Decision.locationArray[2]-rotate)%camera_deneme.CAMERA_CONS
                                #Decision.locationArray[4]+= rotate
                                if(Decision.locationArray[4]>camera_deneme.CAMERA_CONS):
                                        Decision.locationArray[4]=Decision.locationArray[4]%camera_deneme.CAMERA_CONS
                                print "case5 cw initstep2"
                        elif rotate<0:
				
                                rotate=int(round(abs(rotate)*camera_deneme.DC2CAMERA_RATIO))
				if rotate<2:
					rotate=2
				
                                roundCCW(rotate)
                                Decision.locationArray[0]=(Decision.locationArray[0]-rotate)%camera_deneme.CAMERA_CONS        
                                Decision.locationArray[1]=(Decision.locationArray[1]-rotate)%camera_deneme.CAMERA_CONS
                                Decision.locationArray[2]=(Decision.locationArray[2]-rotate)%camera_deneme.CAMERA_CONS
                                #Decision.stepperCCW (rotate,1)
                                #Decision.locationArray[4]-= rotate
                                if(Decision.locationArray[4]>camera_deneme.CAMERA_CONS):
                                        Decision.locationArray[4]=Decision.locationArray[4]%camera_deneme.CAMERA_CONS
                                print "case6 ccw initstep2",rotate
                
                #elif xRobot>2 :
                #        Decision.stepperCW(1,1)
                #elif xRobot<-2:
                #        Decision.stepperCCW(1,1)
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
		synevent.set()
                semapMove.release()
		count+=1
                if (radius<radiusFirst and hits>30) :#or count>50 :
                        camera.release()
                        cv2.destroyAllWindows()
                        break
        
        
	
	
	
	
	
	
	
	
	
	
	
	
	

