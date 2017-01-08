from gpiozero import Motor
from gpiozero import LED
led = LED(2)
motor = Motor(20, 21)
while True:
    led.on()
    motor.forward()
