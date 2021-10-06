import params
import RPi.GPIO as GPIO
import time
import serial
import threading

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
#find serial port of bluetooth
#by      :  ls -l /dev/serial0
#returns :  >ttyS0
bt_serial = serial.Serial("/dev/ttyS0",baudrate = 9600, timeout = 1.0)

"""
********************************************************
       Global variabile & Functions 
********************************************************
"""
grx_data = ""
def bt_serial_thread():
    global grx_data 
    while True:
        rx_data = bt_serial.readline()
        rx_data = rx_data.decode()
        grx_data = rx_data

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
def main():
    global grx_data
    cmd = ["go","back","left","right","stop"]
    go_where = [go_forward,go_backward,go_left,go_right,go_stop]
    speed = 50
    try:
        while True:
            for i in range(0,5):
                if grx_data.find(cmd[i])>=0:
                    grx_data = ""
                    print("OK! %s",cmd[i])
                    if(cmd[i]=="stop"):
                        speed = 0
                    go_where[i](speed)
            for i in range(0,4):
                if(GPIO.input(SWs[i]==1):
                        print("Emergency Stop!!")
                        go_where[-1](0)
    except: KeyboardInterrupt:
        pass

"""
********************************************************
       Jobs 
********************************************************
"""
if __name__=="__main__":
    task1 = threading.Thread(target = bt_serial_thread)
    task1.start()
    main()
    bt_serial.close()
    GPIO.cleanup()







