
####!!!!!derece kullandim encoderin olcusune gecilmesi icin scale edilmesi lazim !!!!


from collections import deque
import numpy as np
import argparse, cv2, time, serial
from ardFunc import roundCW, startCom, roundCCW, goStraight, callHits
from camera_deneme import camera, findTarget
from collections import deque
from serial import Serial
from math import acos
turnDegree is 15
#ser = Serial('/dev/ttyACM1',9600)
########Main Fuct of DECISION#######
##locationArray[0] --> angle between first robot and the initial location
##locationArray[1] --> angle between second robot and the initial location
##locationArray[2] --> angle between target and the initial location
##locationArray[3] --> distance of the target from the x pixels of the cylinder
##locationArray[4] --> current location of the robot 
def Decision ():
    global locationArray=[0]*5    
    while TRUE:
        if(locationArray[0]and locationArray[1] and locationArray[2])!=0:
            break;
        if(locationArray[4]>=360):
            break;
        degree = cameraRobots()  
        if inputCamera !=-1 : ###duzelt burayi kutaya gore!!!
            updateArray(degree+locationArray[4],1)          
        (degree,distance) = cameraTarget()
        if inputCamera !=-1 :
            updateArray(locationArray[4]+degree,3)
            updateArray(distance,4)
        roundCW(turnDegree)
        locationArray[4]+=turnDegree
    decision=decide2Go()
    if decision == -1:
        return -1;
    else:
        return 1;
#########Update Array#####
def updateArray(value,order):
    if(order==1):
        if(locationArray[0]==0):
            locationArray[0]=value
        else:
            if(locationArray[0]-value)>5:
                locationArray[1]=value                
    elif (order==3):
        if(locationArray[2]!=0):
            locationArray=value
        else:
            print 'more than one target is detected ERROR!!'
    elif (order==4):
        if(locationArray[3]!=0):
            locationArray=value
        else:
            print 'more than one target is detected ERROR!!'    
    return 0;    
    
########Decide and Turn The Direction######### 
def decide2Go():
    if (locationArray[1]-locationArray[0]<100):
        if(locationArray[2]>=locationArray[0] and locationArray[2]<=locationArrauy[1]):
            turnDirection(1)
        elif ((locationArray[0]-locationArray[2])%360)<50: 
            criticalAngle=getCriticalAngle()
            if((locationArray[0]-locationArray[2])%360)+(locationArray[1]-locationArray[0])/2)<criticalAngle:
                turnDirection(1)
            else:
                return -1;
        elif((locationArray[2]-locationArray[1])%360)<50 :
            criticalAngle=getCriticalAngle()
            if((locationArray[2]-locationArray[1])%360)+(locationArray[1]-locationArray[0])/2 <criticalAngle:
                turnDirection(1)
            else:
                return -1;
    else:
        if(locationArray[2]-locationArray[0])>50 and (locationArray[1]-locationArray[0]>50):
            return -1;
        elif (locationArray[2]<=locationArray[0]) or (locationArray[2]>=locationArray[1]):
            turnDirection(2)
        elif (locationArray[2]-locationArray[0]<50):
            criticalAngle=getCriticalAngle()
            if(locationArray[2]-locationArray[0])+((locationArray[0]-locationArray[1])%360)/2<criticalAngle:
                turnDirection(2)
            else:
                return -1;
        elif(locationArray[1]-locationArray[2]<50):
            criticalAngle=getCriticalAngle()
            if(locationArray[1]-locationArray[2])+((locationArray[0]-locationArray[1])%360)/2 <criticalAngle:
                turnDirection(2)
            else:
                return -1;
#### turn Direction Algorith ####
def turnDirection (direction):
    if (direction==1):  ##case#1 between 2 roobts angle is 60 
        if(locationArray[4]-(locationArray[1]+locationArray[0]))/2<180: 
            roundCCW(locationArray[4]-(locationArray[1]+locationArray[0])/2)
        else:
            roundCW( 360 - locationArray[4]+ ((locationArray[1]+locationArray[0])/2) )
    else:
        if((locationArray[0]+locationArray[1])%360)<70:
            roundCW(((((locationArray[0]+locationArray[1])%360)/2)-locationArray[4])%360)
        elif ((locationArray[0]+locationArray[1])%360)>290:
            if( locatoinArray[4]> locationArray[1] + ((locationArray[0]-locationArray[1])%360)/2 ):
                roundCCW( locatoinArray[4]- locationArray[1] + ((locationArray[0]-locationArray[1])%360)/2 )
            else:
                roundCW( locatoinArray[4]- locationArray[1] + ((locationArray[0]-locationArray[1])%360)/2 )
    return 1;
         
    


    
def getCriticalAngle():
    targetMeter=pixel2MeterTarget(locationArray[3])    
    criticalAngle=math.acos(43.3/targetMeter)
    return criticalAngle;


















    
        
