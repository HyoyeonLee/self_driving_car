import params
import RPi.GPIO as GPIO
import time




"""
********************************************************
        SetUp raspberry pi GPIOs
********************************************************
"""
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for pin in leds_buzzer_motors:
    GPIO.setup(pin,GPIO.OUT)
for pin in sws:
    GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
pwm_motor_left = GPIO.PWM(MOTOR_A_L_PWM,500)
pwm_motor_right = GPIO.PWM(MOTOR_B_R_PWM,500)
pwm_motor_left.start(0)
pwm_motor_right.start(0)

pwm_buzzer = GPIO.PWM(BUZZER,nDo)
pwm_buzzer.stop()


"""
********************************************************
       Functions 
********************************************************
"""
def go_forward(speed):
    for i in range(0,4):
        GPIO.output(MOTOR_INs[i],STATE_FORWARD[0][i])
        GPIO.output(LEDs[i],STATE_FORWARD[1][i])
    pwm_motor_left.changeDutyCycle(speed)
    pwm_motor_right.changeDutyCycle(speed)
    
def go_backward(speed):
    for i in range(0,4):
        GPIO.output(MOTOR_INs[i],STATE_BACKWARD[0][i])
        GPIO.output(LEDs[i],STATE_BACKWARD[1][i])
    pwm_motor_left.changeDutyCycle(speed)
    pwm_motor_right.changeDutyCycle(speed)


def go_left(speed):
    for i in range(0,4):
        GPIO.output(MOTOR_INs[i],STATE_LEFT[0][i])
        GPIO.output(LEDs[i],STATE_LEFT[1][i])
    pwm_motor_left.changeDutyCycle(speed)
    pwm_motor_right.changeDutyCycle(speed)

def go_right(speed):
    for i in range(0,4):
        GPIO.output(MOTOR_INs[i],STATE_RIGHT[0][i])
        GPIO.output(LEDs[i],STATE_RIGHT[1][i])
    pwm_motor_left.changeDutyCycle(speed)
    pwm_motor_right.changeDutyCycle(speed)

def go_stop(speed):
    for i in range(0,4):
        GPIO.output(MOTOR_INs[i],STATE_STOP[0][i])
        GPIO.output(LEDs[i],STATE_STOP[1][i])
    pwm_motor_left.changeDutyCycle(0)
    pwm_motor_right.changeDutyCycle(0)

"""
********************************************************
       MAIN() 
********************************************************
"""
go_where = [go_forward,go_backward,go_left,go_right,go_stop]
speed = 50
try:
    while True:
        for i in range(0,4):
            if GPIO.input(i)==1:
                go_where[i](speed)
except: KeyboardInterrupt:
    pass
go_where[4](0)
GPIO.cleanup()






