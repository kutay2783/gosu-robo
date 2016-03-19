from serial import Serial
import serial
import time
ser = Serial('/dev/ttyACM2',9600)
time.sleep(2)

ser.write(chr (20))
while 1:
    time.sleep (2)
    ardMsg = ser.readline()
    ardMsg = int (ardMsg)
    if (ardMsg==8):
        print 'fa'
    if(ardMsg ==5):
        print (ardMsg)
        print 'kt'
        break

ser.write (chr(49))
ser.write (chr(255))

