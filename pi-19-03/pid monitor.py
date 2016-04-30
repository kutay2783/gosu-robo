from ardFunc import roundCW, startCom, roundCCW, goStraight, callHits,incLeft,incRight, stopGoStraight

from ardFunc import roundCW, startCom, roundCCW, goStraight, callHits
from serial import Serial
import time
ser = Serial('/dev/ttyUSB0',9600)
time.sleep(1)
startCom()
time.sleep(1)
goStraight(250)
while True:    
    ardMsg1 = ser.readline()
    ardMsg1 = int (ardMsg1)
    ardMsg2 = ser.readline()
    ardMsg2 = int (ardMsg2)
    ardMsg3 = ser.readline()
    ardMsg3 = int (ardMsg3)
    ardMsg4 = ser.readline()
    ardMsg4 = int (ardMsg4)
    #time.sleep(3)
    incRight(3) 
    print"left" ,ardMsg1,"  right",ardMsg2,"  output",ardMsg3,"  input",ardMsg4 
