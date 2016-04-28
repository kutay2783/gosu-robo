import sys
import time
import RPi.GPIO as GPIO
def stepTurn(dir,degrees):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17,GPIO.OUT)
	GPIO.setup(27,GPIO.OUT)
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
		degrees=degrees-1
		if degrees==0:
			break;
