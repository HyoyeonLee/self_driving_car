from params import *
import RPi.GPIO as GPIO
import time
import serial
import threading
import cv2
mat src,out
VideoCapture cap
label = 0
count = 0
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
pwm_buzzer = GPIO.PWM(BUZZER,notes[0])
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
def imageProcessing_thread():
    global src,out
    global cap
    global label
    global count
    ret,src = cap.read(cv2.GRAYSCALE)
    src = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
    #src = cv2.flip(src,-1)
    cv2.imshow("org",src)
    #height = src.shape[0]
    out = src[int(height/2):,:]
    out = cv2.GaussianBlur(out,(3,3),0)
    out = cv2.resize(out,dsize=(66,200),interpolation = cv2.INTER_LINEAR)
    cv2.imshow("out",out)
    if isSave==1:
        fname  = "data/out%05d%_%03d.png" %(count,label)
        imwrite(fname,out)
        count+=1
        isSave=0

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
    pwm_motor_left.ChangeDutyCycle(speed)
    pwm_motor_right.ChangeDutyCycle(speed)
    
def go_backward(speed):
    for i in range(0,4):
        GPIO.output(MOTOR_INs[i],STATE_BACKWARD[0][i])
        GPIO.output(LEDs[i],STATE_BACKWARD[1][i])
    pwm_motor_left.ChangeDutyCycle(speed)
    pwm_motor_right.ChangeDutyCycle(speed)

def go_left(speed):
    for i in range(0,4):
        GPIO.output(MOTOR_INs[i],STATE_LEFT[0][i])
        GPIO.output(LEDs[i],STATE_LEFT[1][i])
    pwm_motor_left.ChangeDutyCycle(speed)
    pwm_motor_right.ChangeDutyCycle(speed)

def go_right(speed):
    for i in range(0,4):
        GPIO.output(MOTOR_INs[i],STATE_RIGHT[0][i])
        GPIO.output(LEDs[i],STATE_RIGHT[1][i])
    pwm_motor_left.ChangeDutyCycle(speed)
    pwm_motor_right.ChangeDutyCycle(speed)

def go_stop(speed):
    for i in range(0,4):
        GPIO.output(MOTOR_INs[i],STATE_STOP[0][i])
        GPIO.output(LEDs[i],0)
    pwm_motor_left.ChangeDutyCycle(0)
    pwm_motor_right.ChangeDutyCycle(0)



def buzzer_in_action(honk1_park2):
    pwm_buzzer.ChangeDutyCycle(50)
    if honk1_park2==1:
        melody = melody_Honking
        duration = duration_Honking
    else :
        melody = melody_Parking
        duration = duration_Parking
    for i in range(0,len(melody)):
        pwm_buzzer.start(50)
        pwm_buzzer.ChangeFrequency(melody[i])
        time.sleep(duration[i])
        pwm_buzzer.stop()
        time_sleep(0.1)
    pwm_buzzer.ChangeDutyCycle(0)
    pwm_buzzer.stop()


"""
********************************************************
       MAIN() 
********************************************************
"""
def main():
    cap = cv2.VideoCapture(-1)
    cap.set(3,640)
    camera.set(4,480)
    folder = "/captures"
    count=0;
    global grx_data
    global label
    isSave = 0
    grx_data = "stop"
    keys = [82,84,81,82,'s','q','h','p']
    cmd = ["go","back","left","right","stop","honk","park"]
    labels = [90,0,45,135,0]
    go_where = [go_forward,go_backward,go_left,go_right,go_stop]
    speed = 25
    while(cap.isOpened()):
        key = cv2.waitKey(10)
        for i in range(0,len(keys)):
            if key==keys[i]:
                print("[COMMAND] %s",cmd[i])
                if i<=4:
                    if i==4:
                        speed = 0
                    if (i==0) or (i==2) or (i==3):
                        label=labels[i]
                        isSave=1
                    go_where[i](speed)
                else:
                    honk1_park2 = i-4
                    buzzer_in_action(honk1_park2)
                if(i<4 and GPIO.input(SWs[i])==1):
                    print("Emergency Stop!!")
                    go_where[-1](0)
            
            ret,src = cap.read(cv2.GRAYSCALE)
            src = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
            #src = cv2.flip(src,-1)
            cv2.imshow("org",src)
            #height = src.shape[0]
            out = src[int(height/2):,:]
            out = cv2.GaussianBlur(out,(3,3),0)
            out = cv2.resize(out,dsize=(66,200),interpolation = cv2.INTER_LINEAR)
            cv2.imshow("out",out)
            if isSave==1:
                fname  = "%s/out%05d%_%03d.png" %(folder,count,label)
                count+=1
                isSave = 0
        cv2.destroyAllWindows()


"""
********************************************************
       Jobs 
********************************************************
"""
if __name__=="__main__":
    #task1 = threading.Thread(target = bt_serial_thread)
    #task1.start()
    main()

    #bt_serial.close()
    for pin in leds_buzzer_motors:
        GPIO.out(pin,0)
    GPIO.cleanup()







