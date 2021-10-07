import params
import RPi.GPIO as GPIO
import time
import serial
import threading
import cv2
import os

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
       [HW : driving] Functions 
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



def buzzer_in_action(honk1_park2):
    if honk1_park2==1:
        melody = melody_Honking.copy()
        duration = duration_Honking.copy()
    else :
        melody = melody_Parking.copy()
        duration = duration_Parking.copy()
    for i in range(0,len(melody):
        pwm_buzzer.start(50)
        pwm_buzzer.ChangeFrequency(melody[i])
        time.sleep(duration[i])
        pwm_buzzer.stop()
        time_sleep(0.1)
    pwm_buzzer.stop()

"""
********************************************************
       [CAMERA]   
********************************************************
"""

"""
********************************************************
       MAIN() 
********************************************************
"""
def main():
    cam = cv2.VideoCapture(-1)
    cam.set(3,640)
    cam.set(4,480)
    folder = "/home/pi/selfdrive/video/frames"
    STATE = "stop"
    ref_angle = [90,0,45,135,0,0,0]
    global grx_data
    cmd = ["go","back","left","right","stop","honk","park"]
    go_where = [go_forward,go_backward,go_left,go_right,go_stop]
    speed = 50
    is1st = 1
    count = 0
    while (cam.isOpened()):        
        for i in range(0,len(cmd)):
            if grx_data.find(cmd[i])>=0:
                print("[COMMAND] %s",cmd[i])
                if i<=4:
                    STATE = cmd[i]
                    grx_data = ""
                    if i==4:
                        speed = 0
                    go_where[i](speed)
                else:
                    honk1_park2 = i-4
                    buzzer_in_action(honk1_park2)
        for i in range(0,4):
            if(GPIO.input(SWs[i]==1):
                print("Emergency Stop!!")
                go_where[4](0)
        #------------------------------------[1] capture a frame and flip
        _,src = cap.read()
        src = cv2.flip(src,-1)
        cv2.imshow('src',src)
        #------------------------------------[2] crop, color, blur, resize
        height,_,_  = src.shape
        out = src[int(height/2): , : , : ]
        out = cv2.cvtColor(out,cv2.BGR2YUV)
        out = cv2.GaussianBlur(out,(3,3),0)
        out = cv2.resize(out,dsize = (200,66))
        cv2.imshow("out",out)
        #------------------------------------[3] save
        
        if STATE == "go" or STATE=="left" or STATE=="right":
            fname = folder + "%05d_%03d.png"%(count,ref_angle[cmd.index(STATE)])
            cv2.imwrite(fname,out)
        count += 1
        key = cv2.waitKey(10)
        if key==ord('q'):
            break;


    

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







