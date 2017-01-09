import serial,os
import readchar
from time import sleep
port=os.popen('ls /dev/ttyACM*').read()[:-1]
ser = serial.Serial(port, 9600)
while True:
    inkey = readchar.readchar()
    if inkey == "w":
        ser.write('F')
    if inkey == "s":
        ser.write('B')
    if inkey == "a":
        ser.write('L')
    if inkey == "d":
        ser.write('R')
    if inkey == "j":
        ser.write('H')
    if inkey == "u":
        ser.write('U')
    if inkey == "n":
        ser.write('D')
    if inkey == "q":
        break
