import serial
port=1
ser = serial.Serial('/dev/ttyACM'+str(port), 9600)
ser.write('3')
#while 1 :
#        ser.readline()
