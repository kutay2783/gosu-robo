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
	global locArr
	locArr = [0]*2
	hits=0
        radiusFirst=32		
        initialize=initStep2Robot()
        if initialize==-1:
                return -1
        locArr[0]=Decision.locationArray[4]
        constant=70
        goStraight(constant)        
        while True:
                hitsLeft,hitsRight=callHits()
                hits=(hitsLeft+hitsRight)/2
                if (hits>constant-2):
                        equilibrium=equalizer()
			break
                print "waiting for condition",hits
                time.sleep(1)
        
        constant=20
        goStraight(constant)
        if (equilibrium>0):
                incLeft(equilibrium)
        elif (equilibrium<0):
                incRight(abs(equilibrium))
        while True:
                hitsLeft,hitsRight=callHits()
                hits=(hitsLeft+hitsRight)/2
                if (hits>constant-2):
                        equilibrium=equalizer()
			break
		print "waiting for condition",hits                        
                time.sleep(1)
        constant=10
        goStraight(constant)
        if (equilibrium>0):
                incLeft(equilibrium)
        elif (equilibrium<0):
                incRight(abs(equilibrium))
        while True:
                hitsLeft,hitsRight=callHits()
                hits=(hitsLeft+hitsRight)/2
                if (hits>constant-2):
                        equilibrium=equalizer()
			
                        break
		print "awaiting for condition",hits
                time.sleep(1)
        constant=5
        goStraight(constant)
        if (equilibrium>0):
                incLeft(equilibrium)
        elif (equilibrium<0):
                incRight(abs(equilibrium))
        
        	
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
                elif xrbt4Init>-7 and xrbt4Init<7:
                        print "robot detected ez initStep",xrbt4Init
                        radiusFirst=radius4Init
                        xRobLast=xrbt4Init
                        break
                else:
                        kp=0.5
                        rotate=kp*xrbt4Init
                        if rotate>0:
                                rotate=int(round(abs(rotate)*camera_deneme.DC2CAMERA_RATIO))
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
	
def equalizer ():
        global locArr
	if (Decision.locationArray[4]>camera_deneme.CAMERA_CONS/2):
        	flag=-1
	else:
		flag=1
        kp=0.5
        turnDegree=camera_deneme.CAMERA_CONS//15
        
        while True:
		xRob,radius=camera_deneme.getCameraForRobots()
                if xRob>-23 and xRob<23:
                        locArr[0]=Decision.locationArray[4]
                        print "found1"
                        break

                if flag==-1:
                        Decision.stepperCCW(turnDegree,1)
                        Decision.locationArray[4]-= turnDegree
                else:
                        Decision.stepperCW(turnDegree,1)
                        Decision.locationArray[4]+= turnDegree
               
                
        while True:
		if (flag==-1):
                        Decision.stepperCCW(turnDegree,1)
                        Decision.locationArray[4]-= turnDegree

                else:
                        Decision.stepperCW(turnDegree,1)
                        Decision.locationArray[4]+= turnDegree

                xRob2,radius2=camera_deneme.getCameraForRobots()
                if xRob2>-23 and xRob2<23 :
                        print "found2"
                        locArr[1]=Decision.locationArray[4]
                        if abs(locArr[1]-locArr[0])>camera_deneme.CAMERA_CONS/8:
                                print "found2"
                                break

                
        result = int(round(flag*kp*(radius-radius2)))
	print "result:",result
        if result>3:
                return 3
        elif result<-3:
                return -3
        else:
                return result	
                
	
	
	
	
	
	
	
	
	
	
	

