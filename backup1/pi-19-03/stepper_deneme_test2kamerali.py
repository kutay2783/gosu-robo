import sys
from collections import deque
import numpy as np
import argparse, cv2, time
import RPi.GPIO as GPIO
def stepTurn(dir,degrees):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17,GPIO.OUT)
	GPIO.setup(27,GPIO.OUT)

	if len(sys.argv[1])>1:
		WaitTime=int(sys.argv[1])/float(1000)
	else:
		WaitTime = 10/float(1000)
	if dir==0:
		GPIO.output(27,True)
	else:
		GPIO.output(27,False)
	while True:
		GPIO.output(17, True)
		time.sleep(WaitTime)
		GPIO.output(17, False)
		time.sleep(WaitTime)
		print degrees
		degrees=degrees-1
		if degrees==0:
			break;
		
GPIO.setmode(GPIO.BCM)		
GPIO.setup(22,GPIO.OUT)
GPIO.output(22,True)
timex=time.time()
stepTurn(1,10)
time.sleep(1)
stepTurn(0,10)
timey=time.time()
print timey-timex
#GPIO.output(22,False)
