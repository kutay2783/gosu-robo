
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
        degree = cameraRobots()  
        if inputCamera !=-1 : ###duzelt burayi kutaya gore!!!
            updateArray(degree+locationArray[4],1)          
        (degree,distance) = cameraTarget()
        if inputCamera !=-1 :
            updateArray(locationArray[4]+degree,3)
            updateArray(distance,4)
        roundCW(turnDegree)
        locationArray[4]+=turnDegree
    turnFinalDirection()
    return 0;
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
def turnFinalDirection():
    if (abs((locationArray[0]-locationArray[2])%360)<50) or (abs(locationArray[2]-locationArray[1])<50):  ##target close to robots
        if ((locationArray[2]-locationArray[0])%360<50) or ((locationArray[1]-locationArray[2])%360<50) : ##target between 2 robots
            if locationArray[1]>locationArray[0]:                     ##if 2.robot last seen  
                roundCCW (locationArray[4]-locationArray[1]+(locationArray[1]-locationArray[0])/2) ##ccw is shortest way
            else :
                if(locationArray[4]-locationArray[0])< (locationArray[1]-locationArray[0])/2)
                    roundCW (locationArray[4]+ ((locationArray[1]-locationArray[0])%360)/2)
        else :
            CriticalAngle=getCriticalAngle()
            
            
    else:
        return -1;




def turnFinalDirection():
    
    


    
def getCriticalAngle():
    targetMeter=pixel2MeterTarget(locationArray[3])    
    criticalAngle=math.acos(43.3/targetMeter)
    return criticalAngle;


















    
        
