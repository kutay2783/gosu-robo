from serial import Serial
import serial
import time
ser = Serial('/dev/ttyUSB0',9600)
def startCom():
    ser.write(chr (1))
    while 1:
        time.sleep (1)
        ardMsg = ser.readline()
        ardMsg = int (ardMsg)
        #print(ardMsg)
        if (ardMsg==2):
            print('Comm started')
            break;
    return;
def roundCW(hitsNumber): 
    temp=0;
    ser.write(chr (5))
    while 1:
        #time.sleep (2)
        ardMsg = ser.readline()
        ardMsg = int (ardMsg)
        #print(ardMsg)
        if (ardMsg==20):
            #print('CW first HS')
            break;
    temp=hitsNumber//250
    #print(temp)
    ser.write(chr(temp))
    while 1:
        #time.sleep (2)
        ardMsg = ser.readline()
        ardMsg = int (ardMsg)
        print(ardMsg)
        if (ardMsg==21):
            #print('CW second HS')
            break;
    temp=hitsNumber%250
    #time.sleep (2)
    ser.write(chr(temp))
    #print(temp)
    while 1:
        #time.sleep (2)
        ardMsg = ser.readline()
        ardMsg = int (ardMsg)
        
        if (ardMsg==3):
            print('CW complete')
            break;            
    return;

    
def roundCCW(hitsNumber):
    temp=0;
    ser.write(chr (6))
    #print('i send ccw')
    while 1:
        #time.sleep (2)
        ardMsg = ser.readline()
        ardMsg = int (ardMsg)
        if (ardMsg==40):
            #print('CCW first HS')
            break;
    temp=hitsNumber//250
    ser.write(chr(temp))
    while 1:
        #time.sleep (2)
        ardMsg = ser.readline()
        ardMsg = int (ardMsg)
        if (ardMsg==41):
            #print('CCW second HS')
            break;
    temp=hitsNumber%250
    ser.write(chr(temp))
    while 1:
        #time.sleep (2)
        ardMsg = ser.readline()
        ardMsg = int (ardMsg)
        if (ardMsg==43):
            print('CCW complete',temp)
            break;            
    return;


def goStraight(hitsNumber):
    temp=0;
    ser.write(chr (7))
    while 1:
        #time.sleep (2)
        ardMsg = ser.readline()
        ardMsg = int (ardMsg)
        if (ardMsg==30):
            #print('GS first HS')
            break;
    temp=hitsNumber//250
    ser.write(chr(temp))
    while 1:
        #time.sleep (2)
        ardMsg = ser.readline()
        ardMsg = int (ardMsg)
        if (ardMsg==31):
            #print('GS second HS')
            break;
    temp=hitsNumber%250
    ser.write(chr(temp))
    while 1:
        #time.sleep (2)
        ardMsg = ser.readline()
        ardMsg = int (ardMsg)
        if (ardMsg==33):
            print('GS complete',temp)
            return 1;
        elif(ardMsg==4):
            return -1;
def incRight(hitsNumber):
    ser.write(chr (8))
    while 1:
        #time.sleep (2)
        ardMsg = ser.readline()
        ardMsg = int (ardMsg)
        if (ardMsg==2):
             break;
    ser.write(chr (hitsNumber))
    while 1:
        #time.sleep (2)
        ardMsg = ser.readline()
        ardMsg = int (ardMsg)
        if (ardMsg==3):
            break ;
    return;

def incLeft(hitsNumber):
    ser.write(chr (9))
    while 1:
        #time.sleep (2)
        ardMsg = ser.readline()
        ardMsg = int (ardMsg)
        if (ardMsg==2):
             break;
    ser.write(chr (hitsNumber))
    while 1:
        #time.sleep (2)
        ardMsg = ser.readline()
        ardMsg = int (ardMsg)
        if (ardMsg==3):
            break ;
    return;

def callHits():
    ser.write(chr (10))
    while 1:
        #time.sleep (2)
        ardMsg = ser.readline()
        ardMsg = int (ardMsg)
        if (ardMsg==2):
             break;
            
    #time.sleep (2)
    temp = ser.readline()
    temp = int (temp)
    #time.sleep (2)
    ardMsg = ser.readline()
    ardMsg = int (ardMsg)
    ardMsg=(temp*250) + ardMsg
    return (ardMsg); 
