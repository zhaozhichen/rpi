import serial
ser = serial.Serial('/dev/ttyACM2', 9600)
ser.write('3')
#while 1 :
#        ser.readline()
