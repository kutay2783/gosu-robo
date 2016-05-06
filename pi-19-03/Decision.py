
####!!!!!derece kullandim encoderin olcusune gecilmesi icin scale edilmesi lazim !!!!


from collections import deque
import numpy as np
import argparse, cv2, time, serial
from ardFunc import roundCW, startCom, roundCCW, goStraight, callHits
import camera_deneme
import RPi.GPIO as GPIO
from collections import deque
from serial import Serial
import math

ser = Serial('/dev/ttyUSB0',9600)
########Main Fuct of DECISION#######
##locationArray[0] --> angle between first robot and the initial location or step count
##locationArray[1] --> angle between second robot and the initial location or step count
##locationArray[2] --> angle between target and the initial location or step count
##locationArray[3] --> distance of the target from the x pixels of the cylinder
##locationArray[4] --> stepper motor direction
##locationArray[5] --> current location of the robot
##locationArray[6] --> distance of the robot 0
##lcoationArray[7] --> distance of the robot 1
def decision (time2Call):  
        global locationArray
        global stepCount
        if time2Call==0:
                stepCount = 0
        locationArray =  [0]*8
        locationArray[0]=-1
        locationArray[1]=-1
        locationArray[2]=-1
        while True:                       
                xRobot,xTarget,distanceTarget,distanceRobot = camera_deneme.getCamera()
                turnDegree=camera_deneme.CAMERA_CONS//15
                if(locationArray[4]>=camera_deneme.CAMERA_CONS+10):
                        break;
                if xRobot !=-80 : 
                        updateArray((xRobot+locationArray[4])%camera_deneme.CAMERA_CONS,1,distanceRobot)
                if xTarget !=-80 :
                        updateArray((distanceTarget),4,0)
                        updateArray((locationArray[4]+xTarget)%camera_deneme.CAMERA_CONS,3,0)
                print locationArray[0],locationArray[1],locationArray[2],locationArray[3],locationArray[4],locationArray[5]
                if( locationArray[1]!=-1 and locationArray[2]!=-1 and locationArray[0]!=-1):
                        break;
                print locationArray[0],locationArray[1],locationArray[2],locationArray[3],locationArray[4],locationArray[5]   
                stepperCW(turnDegree,1)
                locationArray[4]+= turnDegree
                if(locationArray[4]>camera_deneme.CAMERA_CONS):
                        locationArray[4]=locationArray[4]%camera_deneme.CAMERA_CONS
        decide=decide2Go()
        print locationArray[0],locationArray[1],locationArray[2],locationArray[3],locationArray[4]
        if decide == -1:
                print "dont go !!"
                return -1;
        else:
                print "go go go gl hf!!"
                return 1;
#########Update Array#####
def updateArray(value,order,distance):
        global locationArray
        if(order==1):           
                if(locationArray[0]==-1):
                    if(value>int(6*camera_deneme.CAMERA_CONS//7)):
                        locationArray[1]=value
                        locationArray[7]=distance        ##distance of the robot 1
                        print "update 1"
                    else:
                        locationArray[0]=value
                        locationArray[6]=distance        ##distance of the robot 0
                        print "update 0"            
                else:
                        if(value-locationArray[0])>int(camera_deneme.CAMERA_CONS//9)and locationArray[1]==-1:
                                locationArray[1]=value
                                locationArray[7]=distance       ##distance of the robot 1
			else:
				print "same robot seen again updateArray"   
				
        elif (order==3):
                if(locationArray[2]==-1):
                        #print("target value:", value, "order",order )
                        locationArray[2]=value
                elif (value-locationArray[2]>2): ## burdaki 2 degismeli mi her iki case de de cameradan gelen yanlis olcum onemli
                        print 'more than one target is detected ERROR!!'
        elif (order==4):
                if(locationArray[2]==-1): ##locationArray[5] is a temp variable to use here
                        locationArray[3]=value	       
        return 0;    
    
########Decide and Turn The Direction######### 
def decide2Go():
        
        global locationArray
	global CAMERA_CONS
	global WHEEL_CONS	
	angleCri=int(50*camera_deneme.CAMERA_CONS/360)
        if (locationArray[1]-locationArray[0]<camera_deneme.CAMERA_CONS//2):        
                if(locationArray[2]>=locationArray[0] and locationArray[2]<=locationArray[1]):
                        if(locationArray[3]<60): ## pisagoru dusun 
                                print "target is inside triangle! ggwp"
                                return -1;
                        else:
                                turnDirection(1)
                elif ((locationArray[0]-locationArray[2])%camera_deneme.CAMERA_CONS)<angleCri:  ## critical Angle case
                        if(locationArray[3]<60):###########aciya gore 60 duzeltilmesi lazim!!!!!!!!!!!!!!!!!!#################################
                                print"case1, critical angle called, target too close no need to go"
                                return -1;
                                
                        else:
                                criticalAngle=getCriticalAngle()
                                if(((locationArray[0]-locationArray[2])%camera_deneme.CAMERA_CONS)+(locationArray[1]-locationArray[0])/2)<criticalAngle:
                                        turnDirection(1)
                                        print"case2, critical angle called, decided to go"
                                else:
                                        print"case4"
                                        return -1;
                        
                elif((locationArray[2]-locationArray[1])%camera_deneme.CAMERA_CONS)<angleCri :	## critical Angle case
                        if(locationArray[3]<60):
                                print"case5"
                                return -1;
                                
                        else:
                                criticalAngle=getCriticalAngle()
                                if((locationArray[2]-locationArray[1])%camera_deneme.CAMERA_CONS)+(locationArray[1]-locationArray[0])/2 <criticalAngle:
                                        turnDirection(1)
                                        print"case6"
                                else:                                        
                                        print"case7"
                                        return -1;
                else:
                        return -1
        else:
                if ((locationArray[1]-locationArray[2])>angleCri )and ((locationArray[2]-locationArray[0])>angleCri):                              
                        print"case8"
                        return -1;
        
                elif (locationArray[2]<=locationArray[0]) or (locationArray[2]>=locationArray[1]):
                        if(locationArray[3]<60):
                                print "target is inside triangle! ggwp"                                
                                print"case9"
                                return -1;
                        else:
                                turnDirection(2)
                                print"case10"
                elif (locationArray[2]-locationArray[0])<= angleCri :
                        if(locationArray[3]<60):
                                
                                print"case11"
                                return -1;
                        else:
                                criticalAngle=getCriticalAngle()
                                if(locationArray[2]-locationArray[0])+((locationArray[0]-locationArray[1])%camera_deneme.CAMERA_CONS)/2<criticalAngle:
                                        turnDirection(2)
                                        print"case12"
                                else:
                                        print"case13"
                                        return -1;
                                                
                elif(locationArray[1]-locationArray[2]<=angleCri):
                        if(locationArray[3]<60):
                                print"case14"
                                return -1;
                                
                        else:
                                criticalAngle=getCriticalAngle()
                                if(locationArray[1]-locationArray[2])+((locationArray[0]-locationArray[1])%camera_deneme.CAMERA_CONS)/2 <criticalAngle:
                                        turnDirection(2)
                                        print"case15"
                                else:
                                        print"case16"
                                        return -1;
                                        
#### turn Direction Algorith ####
def turnDirection (direction):	
        global locationArray
        if locationArray[1]-locationArray[0]>camera_deneme.CAMERA_CONS/2:
            finalDest=(locationArray[1]+((locationArray[0]-locationArray[1])%camera_deneme.CAMERA_CONS)/2)%camera_deneme.CAMERA_CONS
        else:
            finalDest=(locationArray[0]+locationArray[1])/2
        if finalDest< camera_deneme.CAMERA_CONS/2:
            hitsReq=int(round(finalDest*camera_deneme.DC2CAMERA_RATIO))
            roundCW(hitsReq)
            print "roundCW req, step ", hitsReq, finalDest
	    locationArray[0]=(locationArray[0]-round(finalDest))%camera_deneme.CAMERA_CONS
	    locationArray[1]=(locationArray[1]-round(finalDest))%camera_deneme.CAMERA_CONS
	    locationArray[2]=(locationArray[2]-round(finalDest))%camera_deneme.CAMERA_CONS
        else:
            hitsReq=int(round((camera_deneme.CAMERA_CONS-finalDest)*camera_deneme.DC2CAMERA_RATIO))
            roundCCW(hitsReq)
            print "roundCCW req, step ", hitsReq, finalDest
	    locationArray[0]=(locationArray[0]-round(finalDest))%camera_deneme.CAMERA_CONS
	    locationArray[1]=(locationArray[1]-round(finalDest))%camera_deneme.CAMERA_CONS
	    locationArray[2]=(locationArray[2]-round(finalDest))%camera_deneme.CAMERA_CONS
    
def getCriticalAngle():
	global CAMERA_CONS
	global WHEEL_CONS 	
        global locationArray
        targetMeter=(locationArray[3])    
        criticalAngle=math.acos(51.96/targetMeter)
        criticalAngle=math.degrees(criticalAngle)
        print "arccos is used:))", criticalAngle
        return criticalAngle*camera_deneme.CAMERA_CONS//360;

def pixel2MeterTarget (radius): ## bura guncelle yeni target a agore 
        result=(8.111591)*(10**-8)*((radius)**4)-(0.0000686939)*((radius)**3)+(0.0200612)*((radius)**2)-(2.72701)*radius+183.004
        return result;

def stepperCW(degrees,zero): ##check the over turn !!
	global stepCount
	finalLoc=(stepCount+degrees)%camera_deneme.CAMERA_CONS
	if finalLoc<stepCount:
                stepperCCWManuel(stepCount-finalLoc)                
        elif finalLoc>stepCount:                
                stepperCWManuel(finalLoc-stepCount)
       
        return 0
def stepperCWManuel (degrees):
        global stepCount
	WaitTime=3.0/1000
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(17,GPIO.OUT)
	GPIO.setup(22,GPIO.OUT)	
	GPIO.setup(23,GPIO.OUT)
	GPIO.setup(27,GPIO.OUT)		
	while (degrees>0):
		GPIO.output(17, True)		
		GPIO.output(27, False)
		GPIO.output(22, False)		
		GPIO.output(23, False)		
		time.sleep(WaitTime)

		GPIO.output(17, False)		
		GPIO.output(27, True)
		GPIO.output(22, False)		
		GPIO.output(23, False)		
		time.sleep(WaitTime)

		GPIO.output(17, False)		
		GPIO.output(27, False)
		GPIO.output(22, True)		
		GPIO.output(23, False)		
		time.sleep(WaitTime)

		GPIO.output(17, False)		
		GPIO.output(27, False)
		GPIO.output(22, False)		
		GPIO.output(23, True)		
		time.sleep(WaitTime)
		
		stepCount+=1
		degrees-=1

		

def stepperCCW(degrees,zero): ##check the over turn !!
	global stepCount
	finalLoc=(stepCount-degrees)%camera_deneme.CAMERA_CONS
	if finalLoc>stepCount:
                stepperCWManuel(finalLoc-stepCount)                
        elif finalLoc<stepCount:
                stepperCCWManuel(stepCount-finalLoc)        
        return 0
def stepperCCWManuel (degrees):
        global stepCount
	WaitTime=3.0/1000
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17,GPIO.OUT)
	GPIO.setup(22,GPIO.OUT)	
	GPIO.setup(23,GPIO.OUT)
	GPIO.setup(27,GPIO.OUT)	
	while (degrees>0):
		GPIO.output(17, False)		
		GPIO.output(27, False)
		GPIO.output(22, False)		
		GPIO.output(23, True)		
		time.sleep(WaitTime)
            
		GPIO.output(17, False)		
		GPIO.output(27, False)
		GPIO.output(22, True)		
		GPIO.output(23, False)		
		time.sleep(WaitTime)

		GPIO.output(17, False)		
		GPIO.output(27, True)
		GPIO.output(22, False)		
		GPIO.output(23, False)		
		time.sleep(WaitTime)

		GPIO.output(17, True)		
		GPIO.output(27, False)
		GPIO.output(22, False)		
		GPIO.output(23, False)		
		time.sleep(WaitTime)
		stepCount -=1
		degrees -=1


def makeStepperZero():
	global stepCount
	stepperCCW(stepCount,0)
	

