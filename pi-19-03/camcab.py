import sys
import RPi.GPIO as GPIO
import time

def stepperCW(degrees): ##check the over turn !!
	
	WaitTime=3.0/1000
	GPIO.setmode(GPIO.BCM)
	
	GPIO.setwarnings(False)
	GPIO.setup(17,GPIO.OUT)
	GPIO.setup(22,GPIO.OUT)	
	GPIO.setup(23,GPIO.OUT)
	GPIO.setup(27,GPIO.OUT)		
	while (degrees>0):
		GPIO.output(17, True)		
		GPIO.output(27, False)
		GPIO.output(22, False)		
		GPIO.output(23, False)		
		time.sleep(WaitTime)

		GPIO.output(17, False)		
		GPIO.output(27, True)
		GPIO.output(22, False)		
		GPIO.output(23, False)		
		time.sleep(WaitTime)

		GPIO.output(17, False)		
		GPIO.output(27, False)
		GPIO.output(22, True)		
		GPIO.output(23, False)		
		time.sleep(WaitTime)

		GPIO.output(17, False)		
		GPIO.output(27, False)
		GPIO.output(22, False)		
		GPIO.output(23, True)		
		time.sleep(WaitTime)		
		degrees-=1
		
		

def stepperCCW(degrees): ##check the over turn !!
	
	WaitTime=3.0/1000
	GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
	GPIO.setup(17,GPIO.OUT)
	GPIO.setup(22,GPIO.OUT)	
	GPIO.setup(23,GPIO.OUT)
	GPIO.setup(27,GPIO.OUT)	
	while (degrees>0):
		GPIO.output(17, False)		
		GPIO.output(27, False)
		GPIO.output(22, False)		
		GPIO.output(23, True)		
		time.sleep(WaitTime)
            
		GPIO.output(17, False)		
		GPIO.output(27, False)
		GPIO.output(22, True)		
		GPIO.output(23, False)		
		time.sleep(WaitTime)

		GPIO.output(17, False)		
		GPIO.output(27, True)
		GPIO.output(22, False)		
		GPIO.output(23, False)		
		time.sleep(WaitTime)

		GPIO.output(17, True)		
		GPIO.output(27, False)
		GPIO.output(22, False)		
		GPIO.output(23, False)		
		time.sleep(WaitTime)
		
		degrees -=1


degrees=int (sys.argv[2])
mode = int (sys.argv[1])
if mode ==1:
    stepperCW(degrees)
else:
    stepperCCW(degrees)
