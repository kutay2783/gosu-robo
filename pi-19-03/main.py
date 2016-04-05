from ardFunc import roundCW
from ardFunc import startCom
from ardFunc import roundCCW
from ardFunc import goStraight
from ardFunc import callHits
#import ardFunc
from serial import Serial
import serial
import time

ser = Serial('/dev/ttyACM0',9600)
time.sleep (5)
startCom ()
time.sleep (2)
roundCW(100)
time.sleep (2)
roundCWW (10)
goStraight(20)
asd=callHits()
print(asd)


