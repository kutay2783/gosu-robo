
####!!!!!derece kullandim encoderin olcusune gecilmesi icin scale edilmesi lazim !!!!


from collections import deque
import numpy as np
import argparse, cv2, time, serial
from ardFunc import roundCW, startCom, roundCCW, goStraight, callHits
from camera_deneme import getCamera, findTarget
from collections import deque
from serial import Serial
from math import acos

ser = Serial('/dev/ttyUSB0',9600)
########Main Fuct of DECISION#######
##locationArray[0] --> angle between first robot and the initial location
##locationArray[1] --> angle between second robot and the initial location
##locationArray[2] --> angle between target and the initial location
##locationArray[3] --> distance of the target from the x pixels of the cylinder
##locationArray[4] --> current location of the robot 
def decision ():
    #global camera
    turnDegree =7
    global locationArray
    #script,filename = argv
    
    
    target=open("foo.txt" ,"w")
    locationArray = [0]*5    
    while True:
        if(locationArray[0]and locationArray[1] and locationArray[2])!=0:
            break;
        if(locationArray[4]>=52):
            break;
        degree,dummy = getCamera()## cameraRobots()
        target.write("basladi")
        target.write("  ")
        line=locationArray [4]
        target.write("nsd")
        target.write("\n")
        time.sleep (2)
        if degree !=-1 : ###duzelt burayi kutaya gore!!!
            updateArray(degree+locationArray[4],1)          
        (degree,distance) = getCamera() ##cameraTarget()
        
        if degree !=-1 :
            updateArray(locationArray[4]+degree,3)
            updateArray(distance,4)
        roundCW(turnDegree)
        locationArray[4]+= turnDegree
    decision=decide2Go()
    target.close()
    if decision == -1:
        return -1;
    else:
        return 1;
#########Update Array#####
def updateArray(value,order):
    global locationArray
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
    global locationArray
    if (locationArray[1]-locationArray[0]<14):
        if(locationArray[2]>=locationArray[0] and locationArray[2]<=locationArray[1]):
            turnDirection(1)
        elif ((locationArray[0]-locationArray[2])%52)<7: 
            criticalAngle=getCriticalAngle()
            if(((locationArray[0]-locationArray[2])%52)+(locationArray[1]-locationArray[0])/2)<criticalAngle:
                turnDirection(1)
            else:
                return -1;
        elif((locationArray[2]-locationArray[1])%52)<7 :
            criticalAngle=getCriticalAngle()
            if((locationArray[2]-locationArray[1])%52)+(locationArray[1]-locationArray[0])/2 <criticalAngle:
                turnDirection(1)
            else:
                return -1;
    else:
        if(locationArray[2]-locationArray[0])>7 and (locationArray[1]-locationArray[0]>7):
            return -1;
        elif (locationArray[2]<=locationArray[0]) or (locationArray[2]>=locationArray[1]):
            turnDirection(2)
        elif (locationArray[2]-locationArray[0]<7):
            criticalAngle=getCriticalAngle()
            if(locationArray[2]-locationArray[0])+((locationArray[0]-locationArray[1])%52)/2<criticalAngle:
                turnDirection(2)
            else:
                return -1;
        elif(locationArray[1]-locationArray[2]<7):
            criticalAngle=getCriticalAngle()
            if(locationArray[1]-locationArray[2])+((locationArray[0]-locationArray[1])%52)/2 <criticalAngle:
                turnDirection(2)
            else:
                return -1;
#### turn Direction Algorith ####
def turnDirection (direction):
    global locationArray
    if (direction==1):  ##case#1 between 2 roobts angle is 60 
        if(locationArray[4]-(locationArray[1]+locationArray[0]))/2<26: 
            roundCCW(int(locationArray[4]-(locationArray[1]+locationArray[0])/2))
            print (locationArray[4]-(locationArray[1]+locationArray[0])/2)
        else:
            roundCW(int( 52 - locationArray[4]+ ((locationArray[1]+locationArray[0])/2) ))
            print 52 - locationArray[4]+ ((locationArray[1]+locationArray[0])/2)
    else:
        if((locationArray[0]+locationArray[1])%52)<10:
            roundCW(((((locationArray[0]+locationArray[1])%52)/2)-locationArray[4])%52)
        elif ((locationArray[0]+locationArray[1])%52)>42:
            if( locatoinArray[4]> locationArray[1] + ((locationArray[0]-locationArray[1])%52)/2 ):
                roundCCW(int( locatoinArray[4]- locationArray[1] + ((locationArray[0]-locationArray[1])%52)/2 ))
                print locatoinArray[4]- locationArray[1] + ((locationArray[0]-locationArray[1])%52)/2
            else:
                roundCW(int( locatoinArray[4]- locationArray[1] + ((locationArray[0]-locationArray[1])%52)/2 ))
                print locatoinArray[4]- locationArray[1] + ((locationArray[0]-locationArray[1])%52)/2 
    return 1;
         
    


    
def getCriticalAngle():
    global locationArray
    targetMeter=pixel2MeterTarget(locationArray[3])    
    criticalAngle=acos(43.3/targetMeter)
    return criticalAngle;

def pixel2MeterTarget (radius):
    result=(0.000530837)*((radius)**4)-(0.0646349)*((radius)**3)+(2.97707)*((radius)**2)-(63.2866)*radius+586.071
    return result;
















    
        
