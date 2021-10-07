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
x = 0.1
o = 0.2
q = 0.4
d = 0.8
notes = [262,294,330,349,392,415,440,494,523,587,584,659,698,784,880,987]
melody_Honking = [4,0,4]
duration_Honking = [o,x,o]
melody_Parking = [11,10,11,10,11,7,9,8,6,0]#,2,6,7,2,5,7,8,2,11,10,11,10,11,7,9,8,6,0,2,6,7,2,8,7,6]
duration_Parking = [o,o,o,o,o,o,o,o,d,o]
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
motor A[IN1 IN2] B[IN1 IN2] led [FL FR BL BR]
"""

STATE_FORWARD  = [[0,1,0,1],[1,1,0,0]]
STATE_BACKWARD = [[1,0,1,0],[0,0,1,1]]
STATE_RIGHT    = [[0,1,1,0],[0,1,0,1]]
STATE_LEFT     = [[1,0,0,1],[1,0,1,0]]
STATE_STOP     = [[0,1,0,1],[0,0,0,0]]
