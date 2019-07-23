#!/usr/bin/python
import argparse
import time
import lcm
from arc import control_t, imu_fusion_t
import sys
import math
import PID

parser = argparse.ArgumentParser()
parser.add_argument('--prc_motor', type=int,  default=0)
parser.add_argument('--tgt_yaw', type=int,  default=-44)
parser.add_argument('--time', type=int, default=1)
args = parser.parse_args()
#print(args)
#print(args.prc)
#sys.exit()

ADJUST_EVERY = 0.05

lc = lcm.LCM()
pid = PID.PID(P=10,I=5.0,D=5.0)
pid.SetPoint = float(args.tgt_yaw)/180.0*math.pi
pid.setSampleTime(ADJUST_EVERY)

time_start = time.time()

last = 0
last_adjust = time.time()
last_yaw = 0

def stop():
    msg = control_t()
    msg.timestamp = time.time()
    msg.motor = 0
    msg.servo = 0
    lc.publish('CTRL', msg.encode())
   

def adjust_servo(diff):
    global lc
    global last
    if (last + diff > 100):
        last = 100
    elif (last + diff < -100):
        last = -100
    else:
        last = last + diff

    msg = control_t()
    msg.timestamp = time.time()
    msg.motor = args.prc_motor
    msg.servo = last
    lc.publish('CTRL', msg.encode())


def lcm_imu(channel, data):
    global pid
    global last_adjust
    global last
    global last_yaw
    m = imu_fusion_t.decode(data)
    if (last_yaw > 90.0 and m.yaw < -90):
        m.yaw = 360.0 + m.yaw
    if (last_yaw < -90.0 and m.yaw > 90):
        m.yaw = m.yaw - 360.0
    last_yaw = m.yaw
    pid.update( m.yaw )
    if (time.time() - ADJUST_EVERY > last_adjust):
        last_adjust = time.time()
        adjust_servo(pid.output)
#        print m.yaw, last, pid.output, pid.PTerm, pid.ITerm, pid.DTerm

lc.subscribe('IMU_FUSION', lcm_imu)

while time.time() < time_start + args.time:
    lc.handle()
    time.sleep(0.01)

stop()
