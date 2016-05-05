from serial import Serial
import serial
import time
import RPi.GPIO as GPIO
from ardFunc import startCom



ser = Serial('/dev/ttyUSB0',9600)

time.sleep (1)
startCom ()
