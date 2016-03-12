# import the necessary packages ---- sis kapagi takip ediyo
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time

kapakLower = (10, 145, 140)
kapakUpper = (46, 255, 255)
ttt=0
time1=time.time()
camera = cv2.VideoCapture(1)
camera.set(3,320)
camera.set(4,240)
camera.set(5,10)
# keep looping
while True:
	(grabbed, frame) = camera.read()
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	
	mask = cv2.inRange(hsv, kapakLower, kapakUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	
	cnts = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
#	print(cnts)
	center = None

	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		center=(int(x), int(y))
		if radius > 10:
			cv2.circle(frame, center, int(radius),(0, 0, 0), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
		print('x: ',int (x)," y: ",int (y)," distance: ",radius)
	ttt=ttt+1
	time2=time.time()
	if (time2-time1)>1:
		print ttt
		print (time2-time1)
		ttt=0
		time1=0		
		time1=time.time()
	cv2.imshow("Frame", frame)
	cv2.imshow("mask", mask)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

camera.release()
cv2.destroyAllWindows()
