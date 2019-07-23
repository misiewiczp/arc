#!/usr/bin/python
import argparse
import time
import lcm
from arc import control_t, imu_t, distance_t
import sys
import math
import PID

parser = argparse.ArgumentParser()
args = parser.parse_args()

lc = lcm.LCM()

def lcm_imu(channel, data):
    m = imu_t.decode(data)
    omega = 180.0*m.gyro[1]/math.pi
    a0 = (round(m.accel[0]*9.81*10))
    heading = math.atan2(m.compass[0]-31, m.compass[2] - 14.5)/math.pi*180
    print 'IMU', m.timestamp, omega, a0, heading

def lcm_dstn(channel, data):
   m = distance_t.decode(data)
   print 'DSTN', m.timestamp, m.measure

#lc.subscribe('IMU', lcm_imu)
lc.subscribe('DSTN', lcm_dstn)

while True:
    lc.handle()
    time.sleep(0.01)

