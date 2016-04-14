from ardFunc import roundCW
from ardFunc import startCom
from ardFunc import roundCCW
from ardFunc import goStraight
from ardFunc import callHits
#import ardFunc
from serial import Serial
import serial
import time

ser = Serial('/dev/ttyACM1',9600)
time.sleep (1)
startCom ()
time.sleep (1)
#roundCW(50)
#time.sleep (1)
roundCCW (25)
goStraight(15)
asd=callHits()
print(asd)


