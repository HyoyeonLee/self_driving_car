import RPi.GPIO as GPIO

"""
*****************************************************************
              DEFINES : pins and states 
*****************************************************************
"""
LED_FL = 26
LED_FR = 16
LED_BL = 20
LED_BR = 21
LEDs = [LED_FL,LED_FR,LED_BL,LED_BR]
SW_UP    = 6
SW_DOWN  = 13
SW_LEFT  = 5
SW_RIGHT = 19
SWs = [6,13,5,19]
BUZZER = 12

MOTOR_A_L_PWM = 18
MOTOR_A_L_IN1 = 22
MOTOR_A_L_IN2 = 27


MOTOR_B_R_PWM = 23
MOTOR_B_R_IN1 = 25
MOTOR_B_R_IN2 = 24
MOTOR_INs = [MOTOR_A_L_IN1,MOTOR_A_L_IN2,MOTOR_B_L_IN1,MOTOR_B_R_IN2]

BT_RX = 14
BT_TX = 15

mDo = 261
mRe = 293
mMi = 329
mFa = 349
mSol = 392
mLa = 440
mSi = 493
mDO = 523

#mHonking = []
#mParking = []
"""
--------------------------------------
        |   MOTOR       |   LED
---------------------------------------
FORWARD |  F      F     |   O O
        |               |   X X
---------------------------------------
BACKWARD|  B      B     |   X X
        |               |   O O
---------------------------------------
LEFT    |  B      F     |   O X
        |               |   O X
---------------------------------------
RIGHT   |  F      B     |   X O
        |               |   X O
---------------------------------------
STOP    |  F=0    F=0   |   X X
        |               |   X X
---------------------------------------
motor [IN1 IN2 IN1 IN2] led [FL FR BL BR]
           A   |   B

"""

STATE_FORWARD  = [[0,1,0,1],[1,1,0,0]]
STATE_BACKWARD = [[1,0,1,0],[0,0,1,1]]
STATE_RIGHT    = [[0,1,1,0],[0,1,0,1]]
STATE_LEFT     = [[1,0,0,1],[1,0,1,0]]
STATE_STOP     = [[0,1,0,1],[0,0,0,0]]
