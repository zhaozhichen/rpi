import serial,os

port=os.popen('ls /dev/ttyACM*').read()[:-1]
ser = serial.Serial(port, 115200)

while True:
    line = ser.readline()#.decode('utf-8')
    print line
