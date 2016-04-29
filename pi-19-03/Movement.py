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
        global radiusLast
	radiusLast = 32
	
        initialize=initStep2Robot()
        if initialize==-1:
                return -1
        constant=300
	hits=0
        goStraight(constant)
        while hits<constant:		
                (xRobot,radius) = camera_deneme.getCameraForRobots()
		if radius<32 and hits>30:
			stopGoStraight()
			break;
                print "movament camera enable"
		(hitsLeft,hitsRight) = callHits()
                #hits = callHits()
		print "call hits",hitsLeft,"right",hitsRight
		angleStepper=getAngleStepper(xRobot)
		print "angle stepper",angleStepper
		hits = (hitsLeft+hitsRight)/2
		straightenPID(radius,angleStepper,hits)		
		step2Robot(xRobot)
		
	return 1	

def straightenPID(radius,angle,distanceInitial):	
	global radiusLast
	Kp=1
	Kd=0
	radiusTable=table4Angle(angle)
	correctionValue =int(Kp*(radius-radiusTable)+Kd*(radius-radiusLast))
	print "radius angle PID",radius,angle
	print "correction value",correctionValue
	if(correctionValue < 0):
                print "inc Right",correctionValue
                incRight(correctionValue)
	elif (correctionValue > 0):
                print "inc Left",correctionValue
		incLeft(abs(correctionValue))
	radiusLast=radius	
	
	
def step2Robot(xRobot):
	kp=2
	print"step2Robot xRobot",xRobot
	if xRobot==-80:
                print "step2Robot error"
	rotate=4-kp*xRobot
	if rotate>0:
                Decision.stepperCCW(rotate,1)
                Decision.locationArray[4]-= rotate
                print"step2Robot CCW",rotate
                if(Decision.locationArray[4]>camera_deneme.CAMERA_CONS):
                        Decision.locationArray[4]=locationArray[4]%camera_deneme.CAMERA_CONS
	elif rotate<0:
                rotate=abs(rotate)
		Decision.stepperCW (rotate,1)
		Decision.locationArray[4]+= rotate
		print"step2Robot CW",rotate
                if(Decision.locationArray[4]>camera_deneme.CAMERA_CONS):
                        Decision.locationArray[4]=locationArray[4]%camera_deneme.CAMERA_CONS
	
	
	
def initStep2Robot():
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
                (xRobot,radius) = camera_deneme.getCameraForRobots()
                print"xrobot: init step",xRobot
                if xRobot==-80:
                        print "init step hatasi"
                        return -1
                elif xRobot>-2 and xRobot<2:
                        print "robot detected ez initStep"
                        break
                else:
                        kp=1
                        rotate=int(kp*xRobot)
                        if rotate>0:
                                Decision.stepperCW(rotate,1)
                                Decision.locationArray[4]+= rotate
                                if(Decision.locationArray[4]>camera_deneme.CAMERA_CONS):
                                        Decision.locationArray[4]=locationArray[4]%camera_deneme.CAMERA_CONS
                                print "case5 cw initstep2"
                        elif rotate<0:
                                rotate=abs(rotate)
                                Decision.stepperCCW (rotate,1)
                                Decision.locationArray[4]-= rotate
                                if(Decision.locationArray[4]>camera_deneme.CAMERA_CONS):
                                        Decision.locationArray[4]=locationArray[4]%camera_deneme.CAMERA_CONS
                                print "case6 ccw initstep2"
                
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
	radius=((4.39107)*(10**-6)*(angle**4))-(0.0013749)*((angle)**3)+(0.151729)*((angle)**2)-(6.27768)*angle+116.197
	#polulu radius#radius= (0.00013055)*((angle)**4)-(0.0162049)*((angle)**3)+(0.706096)*((angle)**2)-(11.0045)*angle+84.6914                   
        print "angle,radius from table",angle,radius
        return int (radius)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

