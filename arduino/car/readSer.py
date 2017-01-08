import serial,os
from time import sleep
port=os.popen('ls /dev/ttyACM*').read()[:-1]
ser = serial.Serial(port, 9600)
while True:
    inkey = raw_input()
    if inkey == "w":
        print '----- Forward -----'
        ser.write('F')
    if inkey == "s":
        print '----- Backward -----'
        ser.write('B')
    if inkey == "a":
        print '----- Turn Left -----'
        ser.write('L')
    if inkey == "d":
        print '----- Turn Right -----'
        ser.write('R')
    if inkey == "j":
        print '----- Halt -----'
        ser.write('H')
    if inkey == "u":
        print '----- Servo Up -----'
        ser.write('U')
    if inkey == "n":
        print '----- Servo Down -----'
        ser.write('D')
