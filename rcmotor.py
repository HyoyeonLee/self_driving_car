"""
  MOTOR_A_pwm = 18
  MOTOR_A_IN1 = 22
  MOTOR_A_IN2 = 27
 
  MOTOR_B_pwm = 23
  MOTOR_B_IN1 = 25
  MOTOR_B_IN2 = 24
"""
import RPi.GPIO as GPIO
import time

MOTOR_pwms = [18,23]
MOTOR_dirs = [22,27,25,24]
GPIO.setwarnings(False)
GPIO.setmode(BCM)
for i in (0,1):
    GPIO.setup(MOTOR_pwms[i],GPIO.out)
    GPIO.setup(MOTOR_dirs[i],GPIO.out)
    GPIO.setup(MOTOR_dirs[i+2],GPIO.out)
pwmA = MOTOR_pwmsGPIO.


