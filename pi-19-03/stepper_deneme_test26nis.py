import sys
import time
import RPi.GPIO as GPIO
def stepTurn():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17,GPIO.OUT)
	GPIO.setup(27,GPIO.OUT)
        print "argv2 is:", sys.argv[2]
	if len(sys.argv)>1:
		WaitTime=int(sys.argv[1])/float(1000)
	else:
		WaitTime = 10/float(1000)
	dir=int(sys.argv[3])
	if dir==0:
		GPIO.output(27,True)
		print "cw"
	if (dir==1):
		GPIO.output(27,False)
		print "ccw"
	degrees=int(sys.argv[2])
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
stepTurn()
#stepTurn(0,10)
timey=time.time()
print timey-timex
#GPIO.output(22,False)
