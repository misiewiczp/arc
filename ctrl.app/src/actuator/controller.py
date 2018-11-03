import pigpio
import time
import lcm
from arc import control_t, control_servo_t, control_motor_t

MOTOR_PIN=13
SERVO_PIN=18

MOTOR_CAP=25
SERVO_CAP=100

pi = pigpio.pi()
lc = lcm.LCM()

def arc_set_pwm(pin, val, cap):
    if (val > cap):
        val = cap
    elif (val < -cap):
        val = -cap
    prc = round(1000000*(305+val*90.0/100.0)/3200)
    pi.hardware_PWM(pin, 63, prc)


def request_handler_ctrl(channel, data):
    msg = control_t.decode(data)
#    print ( "{},{}".format(msg.servo, msg.motor) )
    arc_set_pwm(SERVO_PIN, msg.servo, SERVO_CAP)
    arc_set_pwm(MOTOR_PIN, -msg.motor, MOTOR_CAP ) # capped

def request_handler_ctrl_servo(channel, data):
    msg = control_servo_t.decode(data)
#    print ("SERVO:" + msg.servo)
    arc_set_pwm(SERVO_PIN, msg.servo, SERVO_CAP)

def request_handler_ctrl_motor(channel, data):
    msg = control_motor_t.decode(data)
#    print ("MOTOR: " + msg.motor)
    arc_set_pwm(MOTOR_PIN, -msg.motor, MOTOR_CAP) # capped


arc_set_pwm(MOTOR_PIN, 0, 100)
arc_set_pwm(SERVO_PIN, 0, 100)

lc.subscribe('CTRL_SERVO', request_handler_ctrl_servo)
lc.subscribe('CTRL_MOTOR', request_handler_ctrl_motor)
lc.subscribe('CTRL', request_handler_ctrl)

try:
    while True:
        lc.handle()
except KeyboardInterrupt:
    pass

