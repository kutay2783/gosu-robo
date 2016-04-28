import sys
import time
import RPi.GPIO as GPIO
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time
global turns
turns=0
def stepTurn():
        global turns
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17,GPIO.OUT)
	GPIO.setup(27,GPIO.OUT)
        WaitTime = 10/float(1000)
	dir=0
	degrees=20
	GPIO.output(27,1)
	while True:
		GPIO.output(17, True)
		time.sleep(WaitTime)
		GPIO.output(17, False)
		time.sleep(WaitTime)
		degrees=degrees-1
		if degrees==0:
                        turns=turns+1
                        print "turns is:",turns
			break;

def detection():
        global turns
        robotLower = (10, 145, 140)
        robotUpper = (46, 255, 255)
        camera = cv2.VideoCapture(0)
        camera.set(3,320)
        camera.set(4,240)
        while True:
                (grabbed, frame)=camera.read()
                if frame!=None:
                        break
        for i in xrange(5):
        	(grabbed, frame) = camera.read()
        	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        	maskRobot = cv2.inRange(hsv, robotLower, robotUpper)
        	maskRobot = cv2.erode(maskRobot, None, iterations=2)
        	maskRobot = cv2.dilate(maskRobot, None, iterations=2)
                cntsRobot = cv2.findContours(maskRobot.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
                center = None
        	if len(cntsRobot)>0:
                        c = max(cntsRobot, key=cv2.contourArea)
                        ((xRobot, y), radius) = cv2.minEnclosingCircle(c)
                        center=(int(xRobot), int(y))
                        
                        if (radius > 10):
                                cv2.circle(frame, center, int(radius),(0, 0, 0), 2)
                                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                                dist_rad=(0.0000165909)*((radius)**4)-(0.00375541)*((radius)**3)+(0.318206)*((radius)**2)-(12.6395)*radius+236.597
                                tiks=((turns)*20)+(xRobot-150)//15
                                print('xRobot: ', xRobot," robotMeter: ",dist_rad,"step tiks:",tiks)
                        else:
                                Target=-10
		
GPIO.setmode(GPIO.BCM)		
GPIO.setup(22,GPIO.OUT)
GPIO.output(22,True)

stepTurn()
detection()
stepTurn()
detection()
stepTurn()
detection()
stepTurn()
detection()
stepTurn()
detection()
stepTurn()
detection()
stepTurn()
detection()
stepTurn()
detection()
stepTurn()
detection()
stepTurn()
detection()

#GPIO.output(22,False)
