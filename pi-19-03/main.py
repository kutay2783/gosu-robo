from collections import deque
import numpy as np
import argparse, cv2, time, serial
from ardFunc import roundCW, startCom, roundCCW, goStraight, callHits
from camera_deneme import getCamera,getCameraForRobots
from Movement import movement,straightenPID,step2Robot,initStep2Robot,getAngleStepper,radius2Meter,table4Angle
from collections import deque
from serial import Serial
from math import acos
import Decision
from serial import Serial
import serial
import time
import RPi.GPIO as GPIO




ser = Serial('/dev/ttyUSB0',9600)

time.sleep (1)
startCom ()
time.sleep (1)
result=-1
loopCount=0
result=Decision.decision(loopCount)
move=movement()
Decision.makeStepperZero()
        
#GPIO.output(22,False)



