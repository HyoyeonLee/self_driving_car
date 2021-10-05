import RPi.GPIO as GPIO
import time

SWs = [ 5, 6,13,19]
      # L, U, D, R
GPIO.setwarnings(False)
GPIO.setmode(BCM)
for sw in SWs:
    GPIO.setup(sw, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

sw_state_old = [0,0,0,0]
sw_state_new = [0,0,0,0]
sw_click_count = [0,0,0,0]

try:
    while True:
        for i in range(0,len(SWs)):
            sw_state_new[i] = GPIO.input(SWs[i])
            if sw_state_new[i] != sw_state_old[i]:
                sw_state_old[i] = sw_state_new[i]
                if sw_state_new[i] == 1:
                    sw_click_count[i]+=1
                    print("SW%d click : %d" %(i,sw_click_count[i])
                time.sleep(0.2) #for chattering
except KeyboardInterrupt:
    pass

GPIO.cleanup()
