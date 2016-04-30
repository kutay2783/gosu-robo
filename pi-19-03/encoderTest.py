
import numpy as np
import argparse, cv2, time, serial
from camera_deneme import getCamera
from ardFunc import roundCW, startCom, roundCCW, goStraight, callHits,incLeft,incRight, stopGoStraight

from serial import Serial
import sys
import time
import RPi.GPIO as GPIO

ser = Serial('/dev/ttyUSB0',9600)
degrees=int (sys.argv[2])
mode = int (sys.argv[1])
time.sleep (1)
startCom ()

if mode ==1:
    roundCW(degrees)
else:
    roundCCW(degrees)

