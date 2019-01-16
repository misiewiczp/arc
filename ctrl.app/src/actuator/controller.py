import pigpio
import time
import lcm
from arc import control_t, control_servo_t, control_motor_t

MOTOR_PIN=13
SERVO_PIN=18

MOTOR_CAP=50
SERVO_CAP=100

last_motor=0
last_servo=0

pi = pigpio.pi()
lc = lcm.LCM()
c_t = control_t()

def arc_set_pwm(pin, val, cap):
    if (val > cap):
        val = cap
    elif (val < -cap):
        val = -cap
    prc = round(1000000*(305+val*90.0/100.0)/3200)
    print prc
    pi.hardware_PWM(pin, 63, prc)


def request_handler_ctrl(channel, data):
    msg = control_t.decode(data)
    arc_set_pwm(MOTOR_PIN, -msg.motor, MOTOR_CAP ) # capped
    arc_set_pwm(SERVO_PIN, msg.servo, SERVO_CAP)
    last_servo=msg.servo
    last_motor=msg.motor
    c_t.timestamp=time.time()
    c_t.servo = last_servo
    c_t.motor = last_motor
    lc.publish('CTRL_LOG', c_t.encode())
    print ( "{},{},{},{},{}".format(c_t.timestamp,last_servo, last_motor,SERVO_CAP,MOTOR_CAP) )

def request_handler_ctrl_servo(channel, data):
    msg = control_servo_t.decode(data)
    arc_set_pwm(SERVO_PIN, msg.servo, SERVO_CAP)
    last_servo=msg.servo
    c_t.timestamp=time.time()
    c_t.servo = last_servo
    c_t.motor = last_motor
    lc.publish('CTRL_LOG', c_t.encode())
    print ( "{},{},{},{},{}".format(c_t.timestamp,last_servo, last_motor,SERVO_CAP,MOTOR_CAP) )

def request_handler_ctrl_motor(channel, data):
    msg = control_motor_t.decode(data)
    arc_set_pwm(MOTOR_PIN, -msg.motor, MOTOR_CAP) # capped
    last_motor=msg.motor
    c_t.timestamp=time.time()
    c_t.servo = last_servo
    c_t.motor = last_motor
    lc.publish('CTRL_LOG', c_t.encode())
    print ( "{},{},{},{},{}".format(c_t.timestamp,last_servo, last_motor,SERVO_CAP,MOTOR_CAP) )


arc_set_pwm(MOTOR_PIN, 0, MOTOR_CAP)
arc_set_pwm(SERVO_PIN, 0, SERVO_CAP)

c_t.timestamp=time.time()
c_t.servo = 0
c_t.motor = 0
lc.publish('CTRL_LOG', c_t.encode())
print ( "{},{},{},{},{}".format(c_t.timestamp,last_servo, last_motor,SERVO_CAP,MOTOR_CAP) )


lc.subscribe('CTRL_SERVO', request_handler_ctrl_servo)
lc.subscribe('CTRL_MOTOR', request_handler_ctrl_motor)
lc.subscribe('CTRL', request_handler_ctrl)

try:
    while True:
        lc.handle()
        time.sleep(0.01)
except KeyboardInterrupt:
    arc_set_pwm(MOTOR_PIN, 0, MOTOR_CAP)
    arc_set_pwm(SERVO_PIN, 0, SERVO_CAP)
    pass

