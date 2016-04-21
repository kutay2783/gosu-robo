
####!!!!!derece kullandim encoderin olcusune gecilmesi icin scale edilmesi lazim !!!!


from collections import deque
import numpy as np
import argparse, cv2, time, serial
#from ardFunc import roundCW, startCom, roundCCW, goStraight, callHits
from camera_deneme import getCamera, findTarget
from collections import deque
from serial import Serial
import math

#ser = Serial('/dev/ttyUSB0',9600)
########Main Fuct of DECISION#######
##locationArray[0] --> angle between first robot and the initial location
##locationArray[1] --> angle between second robot and the initial location
##locationArray[2] --> angle between target and the initial location
##locationArray[3] --> distance of the target from the x pixels of the cylinder
##locationArray[4] --> current location of the robot 
def decision ():
    #global camera
    turnDegree =6
    global locationArray
    #script,filename = argv
    
    
    
    locationArray = [0]*5
    locationArray[0]=-1
    locationArray[2]=-1
    while True:
        print locationArray[0],locationArray[1],locationArray[2],locationArray[3],locationArray[4]
        if(locationArray[4]>=56):
            break;

        time.sleep(2)
        xRobot,xTarget,distanceTarget = getCamera()## cameraRobots()
        #print "xRobot:  " ,xRobot,"  xTarget:  " ,xTarget, "  distanceTarget: " ,distanceTarget 
        if xRobot !=-10 : ###duzelt burayi kutaya gore!!!
            updateArray((xRobot+locationArray[4])%51,1)          
        ##(degree,distance) = getCamera() ##cameraTarget()
        
        if xTarget !=-10 :
            updateArray((locationArray[4]+xTarget)%51,3)
            updateArray((distanceTarget),4)
        if( locationArray[1]!=0 and locationArray[2]!=-1 and locationArray[0]!=-1):
            break;
        #roundCW(turnDegree)
        locationArray[4]+= turnDegree
    if(locationArray[4]>51):
        locationArray[4]=locationArray[4]%51
    decision=decide2Go()
    print locationArray[0],locationArray[1],locationArray[2],locationArray[3],locationArray[4]
    if decision == -1:
        print "dont go !!"
        return -1;
    else:
        print "go go go gl hf!!"
        return 1;
#########Update Array#####
def updateArray(value,order):
    global locationArray
    if(order==1):       
            
        if(locationArray[0]==-1):
            if(value>46):
                locationArray[1]=value
                print "update 1"
            else:
                locationArray[0]=value
                print "update 0"            
        else:
            if(value-locationArray[0])>5:
                locationArray[1]=value                
    elif (order==3):
        if(locationArray[2]==-1):
            #print("target value:", value, "order",order )
            locationArray[2]=value
        else:
            print 'more than one target is detected ERROR!!'
    elif (order==4):
        if(locationArray[2]!=0):
            locationArray[3]=value
        else:
            print 'more than one target is detected ERROR!!'    
    return 0;    
    
########Decide and Turn The Direction######### 
def decide2Go():
    global locationArray
    if (locationArray[1]-locationArray[0]<14):
        if(locationArray[3]<45):
            print "target is inside triangle! ggwp"
            return -1;
        elif(locationArray[2]>=locationArray[0] and locationArray[2]<=locationArray[1]):
            turnDirection(1)
        elif ((locationArray[0]-locationArray[2])%51)<7: 
            if(locationArray[3]<60):
                return -1;
            else:
                criticalAngle=getCriticalAngle()
                if(((locationArray[0]-locationArray[2])%51)+(locationArray[1]-locationArray[0])/2)<criticalAngle:
                    turnDirection(1)
                else:
                    return -1;
        elif((locationArray[2]-locationArray[1])%51)<7 :
            if(locationArray[3]<60):
                return -1;
            else:
                criticalAngle=getCriticalAngle()
                if((locationArray[2]-locationArray[1])%51)+(locationArray[1]-locationArray[0])/2 <criticalAngle:
                    turnDirection(1)
                else:
                    return -1;
    else:
        if (locationArray[1]-locationArray[2])>7 and (locationArray[2]-locationArray[0])>7:
            return -1;
        
        elif (locationArray[2]<=locationArray[0]) and (locationArray[2]>=locationArray[1]):
            if(locationArray[3]<45):
                print "target is inside triangle! ggwp"
                return -1;
            else:
                turnDirection(2)
        elif (locationArray[2]-locationArray[0]<7):
            criticalAngle=getCriticalAngle()
            if(locationArray[2]-locationArray[0])+((locationArray[0]-locationArray[1])%51)/2<criticalAngle:
                turnDirection(2)
            else:
                return -1;
        elif(locationArray[1]-locationArray[2]<7):
            criticalAngle=getCriticalAngle()
            if(locationArray[1]-locationArray[2])+((locationArray[0]-locationArray[1])%51)/2 <criticalAngle:
                turnDirection(2)
            else:
                return -1;
#### turn Direction Algorith ####
def turnDirection (direction):
    global locationArray
    if (direction==1):  ##case#1 between 2 roobts angle is 60 
        if(locationArray[4]-(locationArray[1]+locationArray[0]))/2<26: 
            #roundCCW(int(locationArray[4]-(locationArray[1]+locationArray[0])/2)) 
            print ("case 1 between 2 rob " ,int (locationArray[4]-(locationArray[1]+locationArray[0])/2))
        else: 
            #roundCW(int( 51 - locationArray[4]+ ((locationArray[1]+locationArray[0])/2) ))
            print ("case 2 between 2 rob" ,int (51 - locationArray[4]+ ((locationArray[1]+locationArray[0])/2)))
    else:
        if((locationArray[0]+locationArray[1])%51)<10:
            #roundCW(int(((((locationArray[0]+locationArray[1])%51)/2)-locationArray[4])%51))
            print ("casse 3 mid point small",int(((((locationArray[0]+locationArray[1])%51)/2)-locationArray[4])%51))
        elif ((locationArray[0]+locationArray[1])%51)>42:
            if( locatoinArray[4]> locationArray[1] + ((locationArray[0]-locationArray[1])%51)/2 ):
               # roundCCW(int( locatoinArray[4]- locationArray[1] - ((locationArray[0]-locationArray[1])%51)/2 ))
                print ("casse 4 mid point large", int(locatoinArray[4]- locationArray[1] + ((locationArray[0]-locationArray[1])%51)/2))
            else:
                #roundCW(int(  locationArray[1]-locationArray[4] + ((locationArray[0]-locationArray[1])%51)/2 ))
                print ("case 5 mid point small " ,int(  locationArray[1]-locatoinArray[4] + ((locationArray[0]-locationArray[1])%51)/2 ))
    return 1;
         
    


    
def getCriticalAngle():
    global locationArray
    targetMeter=(locationArray[3])    
    criticalAngle=math.acos(43.3/targetMeter)
    criticalAngle=math.degrees(criticalAngle)
    print "arccos is used:))", criticalAngle
    return criticalAngle*51//360;

def pixel2MeterTarget (radius):
    result=(8.71591)*(10**-8)*((radius)**4)-(0.0000686939)*((radius)**3)+(0.0200612)*((radius)**2)-(2.72701)*radius+183.004
    return result;


decision()













    
        
