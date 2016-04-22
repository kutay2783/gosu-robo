from collections import deque
import numpy as np
import argparse, cv2, time, serial
from ardFunc import roundCW, startCom, roundCCW, goStraight, callHits
from camera_deneme import getCamera, findTarget
from collections import deque
from serial import Serial
from math import acos
from Decision import *
from serial import Serial
import serial
import time

##global camera
#camera = cv2.VideoCapture(0)


#global camera
ser = Serial('/dev/ttyUSB0',9600)

time.sleep (1)
startCom ()
time.sleep (1)
while True:
    result=decision()
    if(result==1):
        goStraight(50)
    time.sleep(15)
asd=callHits()
print "asd"
#camera.release()
#cv2.destroyAllWindows()

