"""
[Buzzer] (GPIO 12)
-----------------------------------------------------
    |  C  |  D  |  E  |  F  |  G  |  A  |  B  |  C  |
-----------------------------------------------------
[Hz]|261.6|293.6|329.6|349.2|392.0|440.0|493.9|523.2|
  # |277.2|311.1|     |367.0|415.3|466.1|     |     |
-----------------------------------------------------
"""


import RPi.GPIO as GPIO
import time

do_=262,re_=293,mi_=329,fa_=349,sol_=392,la_=440,ti_=494,do__=523
        #do   re  mi  fa  sol  la  si do
notes = [do_,re_,mi_,fa_,sol_,la_,si_,do__]
BUZZER = 12
GPIO.setwarnings(False)
GPIO.setmode(BCM)
GPIO.setup(BUZZER,GPIO.out)

pwm = GPIO.PWM(BUZZER,do_)
pwm.start(0)

while True:
    note = KeyboardInterrupt
    if note >= ord('0') and note<=ord('7'):
        idx = note-ord('0')
        freqeuncy = notes[idx]
        pwm.changeFrequency(frequency)
        time.sleep(1.0)
    if note ==27:
        pass
pwn.stop()
GPIO.cleanup()
