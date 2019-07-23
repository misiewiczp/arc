import lcm
from arc import req_plan_mpc_t
from arc import res_plan_mpc_t
import time
import sys
import math

lc = lcm.LCM()

last_servo = 0
last_motor = 0

MAX_ACC = 5.0 # 5m/ss - przyspieszenie dla zmiany 100


msg = req_plan_mpc_t()
msg.timestamp = int(time.time()*1000)
msg.x = 0
msg.y = 0
msg.yaw = 0
msg.vel = 0
msg.acc = 0
msg.dir = 0
msg.ref_vel = 5 #m/s
msg.latency = 0.1 #s
msg.npoints = 10
msg.points_x = [i for i in range(10)]
msg.points_y = [2*i*5 for i in range(10)]


def delta_dir_2_servo(delta_dir):
    global last_servo
    last_servo = last_servo + (delta_dir) / (25.0 / 180.0 * math.pi)*100.0 # +-25 is max
    print ("Servo ", last_servo)
    if last_servo > 100:
        last_servo = 100
    if last_servo < -100:
        last_servo = -100
    return last_servo

def delta_acc_2_motor(delta_acc):
    global last_motor
    delta_motor = (delta_acc / MAX_ACC)*100.0
    last_motor = (last_motor + delta_motor)  # +-25 is max
    print ("Motor ", last_motor)
    if last_motor > 100:
        last_motor = 100
    if last_motor < -100:
        last_motor = -100
    return last_motor

def servo_2_dir(servo):
    return servo / 100.0 * (25.0/180.0*math.pi)

def motor_2_velocity(motor):
    if (motor >= -15 and motor <= 15):
        return 0
    if motor > 15:
        return (motor - 15)/(100.0-15)*15.0 # max velocity m/s
    if motor < -15:
        return -(-motor - 15)/(100.0-15)*15.0 # max velocity m/s
   
    return 0


def response_handler_mpc(channel, data):
    msg = res_plan_mpc_t.decode(data);
    global last_servo
    global last_motor
    last_servo = delta_dir_2_servo(msg.delta_dir)
    last_motor = delta_acc_2_motor(msg.delta_acc)

#    print(msg.delta_dir, msg.delta_acc, msg.points_x, msg.points_y)

lc.subscribe('MPC_RES', response_handler_mpc)
dt = 0.1
try:
    while True:
        lc.handle_timeout(1000)
        time.sleep(10)
        msg.timestamp = int(time.time()*1000)
        msg.acc = 0
        msg.vel = motor_2_velocity( last_motor )
        msg.dir = servo_2_dir( last_servo )
        msg.x = msg.x + math.cos( msg.dir )*msg.vel*dt
        msg.y = msg.x + math.sin( msg.dir )*msg.vel*dt
        msg.yaw = msg.yaw + msg.dir*msg.vel/0.13*dt # 0.13 length to CoG
	msg.points_x = [msg.x+i for i in range(10)]
	msg.points_y = [msg.y+2*i for i in range(10)]

        print("Status: ", msg.dir, msg.vel, msg.x, msg.y)
        lc.publish('MPC_REQ', msg.encode())

except KeyboardInterrupt:
    pass
