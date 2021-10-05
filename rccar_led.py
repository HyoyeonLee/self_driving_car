import RPi.GPIO as GPIO
import time
"""
LED1 = 26
LED2 = 16
LED3 = 20
LED4 = 21
"""
LEDs = [26,16,20,21]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) 
    #board com mode (instead of pin numbers, use GPIO numbering)
for led in LEDs:
    GPIO.setup(led,GPIO.out)

try:
    while True:
        for led in LEDs:
            GPIO.output(led,GPIO.HIGH)
            time.sleep(1.0)
            GPIO.output(led,GPIO.LOW)
            time.sleep(1.0)
except KeyboardInterrupt:
    pass

GPIO.cleanup()

