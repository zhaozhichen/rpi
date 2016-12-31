from gpiozero import LED
from time import sleep

led = LED(17)

while True:
    print "start cycle"
    led.on()
    sleep(1)
    led.off()
    sleep(1)
