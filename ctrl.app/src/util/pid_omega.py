#!/usr/bin/python
import argparse
import time
import lcm
from arc import control_t, imu_t
import sys
import math
import PID

parser = argparse.ArgumentParser()
parser.add_argument('--prc_servo', type=int,  default=-100)
parser.add_argument('--tgt_omega', type=int,  default=0)
parser.add_argument('--time', type=int, default=5)
args = parser.parse_args()
#print(args)
#print(args.prc)
#sys.exit()

ADJUST_EVERY = 0.2

lc = lcm.LCM()
pid = PID.PID(P=0.1,I=0.01,D=0.01)
pid.SetPoint = float(args.tgt_omega)
pid.setSampleTime(ADJUST_EVERY)

time_start = time.time()

last_motor = 0
last_adjust = time.time()

def adjust_motor(diff_motor):
    global lc
    global last_motor
    if (last_motor + diff_motor > 100):
        last_motor = 100
    elif (last_motor + diff_motor < -100):
        last_motor = -100
    else:
        last_motor = last_motor + diff_motor

    msg = control_t()
    msg.timestamp = time.time()
    msg.motor = last_motor
    msg.servo = args.prc_servo
    lc.publish('CTRL', msg.encode())


def lcm_imu(channel, data):
    global pid
    global last_adjust
    global last_motor
    m = imu_t.decode(data)
    omega = 180.0*m.gyro[1]/math.pi
    pid.update( omega )
    if (time.time() - ADJUST_EVERY > last_adjust):
        last_adjust = time.time()
        adjust_motor(pid.output)
        print omega, last_motor, pid.output, pid.PTerm, pid.ITerm, pid.DTerm


lc.subscribe('IMU', lcm_imu)

while time.time() < time_start + args.time:
    lc.handle()
    time.sleep(0.01)

adjust_motor(-last_motor)
