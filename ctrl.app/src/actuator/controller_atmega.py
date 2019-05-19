import time
import lcm
from arc import control_t, control_servo_t, control_motor_t, distance_t
import spidev
import struct
import sys

bPrint = 0
if (len(sys.argv) > 1 and sys.argv[1] == '--print'):
    bPrint = 1

MOTOR_0 = 1490
SERVO_0 = 1500

SERVO_CAP = 100
MOTOR_CAP = 100

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 50000

is_on_halt = 0

last_motor=0
last_servo=0

lc = lcm.LCM()
c_t = control_t()

last_timer_idx = -1
d_t = distance_t()

#unimplemented at Atmega
def spi_send_motor_req(val):
    pwm_val = int(val) * 5 + MOTOR_0 # / 100.0 * 500.0
    resp = spi.xfer2([0x11, byte(pwm_val), byte(pwm_val>>8), 0xFF])
    if (resp[3] != 0x11):
        print ("Motor REQ error")
        return 0
    return 1

#unimplemented at Atmega
def spi_send_servo_req(val):
    pwm_val = int(val) * 5 + SERVO_0 # / 100.0 * 500.0
    resp = spi.xfer2([0x12, byte(pwm_val), byte(pwm_val>>8), 0xFF])
    if (resp[3] != 0x12):
        print ("Servo REQ error")
        return 0
    return 1

def spi_send_motor_servo_req(val_motor, val_servo):
    pwm_val_motor = int(val_motor) * 5 + MOTOR_0 # / 100.0 * 500.0
    pwm_val_servo = int(val_servo) * 5 + SERVO_0 # / 100.0 * 500.0
    resp = spi.xfer2([0x13, pwm_val_motor & 0xFF, (pwm_val_motor>>8)& 0xFF, (pwm_val_servo)& 0xFF,(pwm_val_servo>>8)& 0xFF, 0xFF, 0]) # on 0 we get result send for 0xFF
    if (resp[6] != 0x13):
        print ("Motor & Servo REQ error")
        print(resp)
        return 0
    return 1


def spi_read_stats():
    t = long(time.time()*1000*1000)
    resp = spi.xfer2([0x01, 0,0, 0,0, 0,0, 0,0, 0,0, 0, 0])
#   print resp
    dist = (int(resp[3])<<8)+resp[2]
    pwm1 = (int(resp[5])<<8)+resp[4]
    pwm2 = (int(resp[7])<<8)+resp[6]
    idx = resp[12]
#    print("{},{},{},{},{}".format(time.time(), idx, dist, pwm1, pwm2))
    if last_timer_idx <> idx:
        d_t.measure = dist
        d_t.timestamp = t
        lc.publish("DSTN", d_t.encode())
        c_t.timestamp = t
        c_t.motor = pwm1
        c_t.servo = pwm2
        lc.publish('CTRL_LOG', c_t.encode())
        if bPrint:
            print("{},{},{},{},{}".format(int(t/1000), idx, dist, pwm1, pwm2))
    lastidx = idx



'''

lc = lcm.LCM()

while True:
   t = long(time.time()*1000*1000)
   resp = spi.xfer2([0x01, 0,0, 0,0, 0,0, 0,0, 0,0, 0, 0])
#   print resp
   dist = (int(resp[3])<<8)+resp[2]
   pwm1 = (int(resp[5])<<8)+resp[4]
   pwm2 = (int(resp[7])<<8)+resp[6]
   idx = resp[12]
   if lastidx <> idx:
       d_t.measure = dist
       d_t.timestamp = t
       lc.publish("DSTN", d_t.encode())
       c_t.timestamp = t
       c_t.motor = pwm1
       c_t.servo = pwm2
       lc.publish('CTRL_LOG', c_t.encode())
       if bPrint:
           print("{},{},{},{},{}".format(int(t/1000), idx, dist, pwm1, pwm2))
   lastidx = idx
   time.sleep(0.01)
'''


def request_handler_ctrl(channel, data):
    msg = control_t.decode(data)
    spi_send_motor_servo_req( msg.motor, msg.servo )
    last_servo=msg.servo
    last_motor=msg.motor
    c_t.timestamp=time.time()
    c_t.servo = last_servo
    c_t.motor = last_motor
    lc.publish('CTRL_LOG', c_t.encode())
    print ( "{},{},{},{},{}".format(c_t.timestamp,last_servo, last_motor,SERVO_CAP,MOTOR_CAP) )

def request_handler_ctrl_servo(channel, data):
    msg = control_servo_t.decode(data)
    spi_send_motor_servo_req( last_motor, msg.servo )
    last_servo=msg.servo
    c_t.timestamp=time.time()
    c_t.servo = last_servo
    c_t.motor = last_motor
    lc.publish('CTRL_LOG', c_t.encode())
    print ( "{},{},{},{},{}".format(c_t.timestamp,last_servo, last_motor,SERVO_CAP,MOTOR_CAP) )

def request_handler_ctrl_motor(channel, data):
    msg = control_motor_t.decode(data)
    spi_send_motor_servo_req( msg.motor, last_servo )
    last_motor=msg.motor
    c_t.timestamp=time.time()
    c_t.servo = last_servo
    c_t.motor = last_motor
    lc.publish('CTRL_LOG', c_t.encode())
    print ( "{},{},{},{},{}".format(c_t.timestamp,last_servo, last_motor,SERVO_CAP,MOTOR_CAP) )

def request_handler_halt(channel, data):
    global is_on_halt
    is_on_halt = 1
    spi_send_motor_req( 0 )
    print ( "{},0,0,0,0".format(time.time()) )

def request_handler_unhalt(channel, data):
    global is_on_halt
    is_on_halt = 0
    print ( "{},0,0,{},{}".format(time.time(), SERVO_CAP, MOTOR_CAP) )


spi_read_stats()
spi_send_motor_servo_req( 0, 0 )

c_t.timestamp=time.time()
c_t.servo = 0
c_t.motor = 0
lc.publish('CTRL_LOG', c_t.encode())
if (bPrint):
    print ( "{},{},{},{},{}".format(c_t.timestamp,last_servo, last_motor,SERVO_CAP,MOTOR_CAP) )


lc.subscribe('CTRL_SERVO', request_handler_ctrl_servo)
lc.subscribe('CTRL_MOTOR', request_handler_ctrl_motor)
lc.subscribe('CTRL', request_handler_ctrl)
lc.subscribe('CTRL_HALT', request_handler_halt)
lc.subscribe('CTRL_UNHALT', request_handler_unhalt)


try:
    while True:
        lc.handle_timeout(10) # at least 100Hz
        spi_read_stats()
#        time.sleep(0.01)
except KeyboardInterrupt:
    spi_send_motor_servo_req( 0, 0 )
    pass



