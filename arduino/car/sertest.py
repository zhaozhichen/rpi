import serial,os
from time import sleep
port=os.popen('ls /dev/ttyACM*').read()[:-1]
ser = serial.Serial(port, 9600)
while 1:
    inkey = raw_input()
    if inkey == "w":
        print '----- Forward -----'
        ser.write('F')
    if inkey == "x":
        print '----- Backward -----'
        ser.write('B')
    if inkey == "a":
        print '----- Turn Left -----'
        ser.write('L')
    if inkey == "d":
        print '----- Turn Right -----'
        ser.write('R')
    if inkey == "s":
        print '----- Halt -----'
        ser.write('H')
