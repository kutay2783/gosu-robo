from collections import deque
import numpy as np
import argparse, cv2, time, serial
from ardFunc import roundCW, startCom, roundCCW, goStraight, callHits
from camera_deneme import getCamera, findTarget
from collections import deque
from serial import Serial
import math

ser = Serial('/dev/ttyUSB0',9600)
def movement():
    stepMotor()
    constant=25
    goStraight(constant)
        while (calhits()<constant):
            
