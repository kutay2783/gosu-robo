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

ser = Serial('/dev/ttyUSB0',9600)
time.sleep(1)
timex=time.time()
startCom()
timey=time.time()

print timey-timex


