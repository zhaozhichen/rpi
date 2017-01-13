import serial,os
import readchar
import keypress

port=os.popen('ls /dev/ttyACM*').read()[:-1]
ser = serial.Serial(port, 9600)
kp=keypress.KeyPress()

fnHalt      = lambda:ser.write('H')
fnForward   = lambda:ser.write('F')
fnBackward  = lambda:ser.write('B')
fnTurnLeft      = lambda:ser.write('L')
fnTurnRight     = lambda:ser.write('R')
fnServoUp   = lambda:ser.write('U')
fnServoDown = lambda:ser.write('D')
kp.registerDefaultHandler(fnHalt)
kp.registerHandlers({\
    'w':fnForward,\
    's':fnBackward,\
    'a':fnTurnLeft,\
    'd':fnTurnRight,\
    'q':fnServoUp,\
    'e':fnServoDown}
kp.registerQuitKey('q')
kp.start()
