import pigpio
import time
import sys

MOTOR_PIN=13
SERVO_PIN=18

MOTOR_CAP=100
SERVO_CAP=200

last_motor=0
last_servo=0

pi = pigpio.pi()

def arc_set_pwm(pin, val, cap):
    if (val > cap):
        val = cap
    elif (val < -cap):
        val = -cap
    prc = round(1000000*(305+val*90.0/100.0)/3200)
    pi.hardware_PWM(pin, 63, prc)


PIN = MOTOR_PIN
CAP = MOTOR_CAP
if sys.argv[1] == "-m":
    PIN = MOTOR_PIN
    CAP = MOTOR_CAP
elif sys.argv[1] == "-s":
    PIN = SERVO_PIN
    CAP = SERVO_CAP
else:
    sys.exit(-1)

val = int(sys.argv[2])

arc_set_pwm(PIN, val, CAP)
time.sleep(5)
arc_set_pwm(PIN, 0, CAP)

