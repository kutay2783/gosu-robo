from collections import deque
import numpy as np
import argparse, cv2, time, serial
from ardFunc import roundCW, startCom, roundCCW, goStraight, callHits
from camera_deneme import camera, findTarget
from collections import deque
from serial import Serial

#ser = Serial('/dev/ttyACM1',9600)
time.sleep (1)
#startCom ()
time.sleep (1)
findTarget()

#roundCW(50)
#time.sleep (1)
#roundCCW (25)
goStraight(100)
#asd=callHits()
#print(asd)


