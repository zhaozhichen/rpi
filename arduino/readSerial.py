import serial,os

port = os.popen('ls /dev/ttyACM*').read()[:-1]
baud = 115200
ser = serial.Serial(port, baud)

while True:
    print ser.readline()
