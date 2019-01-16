import cv2 as cv
import numpy as np
import lcm
import math
from arc import imu_t

WORLD_SIZE=100
CELL_METRIC=5 #cm
world = np.zeros( (WORLD_SIZE,WORLD_SIZE), dtype=np.uint8 )

pos_x = 0.0
pos_y = 0.0
pos_heading = 0.0
pos_velocity = 0.0

last_timestamp = long(0)

calibrate = 2

def update_position(accel, omega, dtime):
    global pos_x, pos_y, pos_heading, pos_velocity
    global calibrate
    if calibrate:
        return
    pos_x += pos_velocity*dtime*math.cos(pos_heading)
    pos_y += pos_velocity*dtime*math.sin(pos_heading)
    pos_heading += omega*dtime
    pos_velocity += accel*dtime
    print ("POS:", round(pos_x*100), round(pos_y*100))
    print ("VEL:", pos_velocity, accel, omega, dtime)

sum_val = [0,0]
cnt_val = [0,0]
avg_val = [0,0]

VAL_ACCEL=0
VAL_GYRO=1

def calibrate_val( val_idx , val):
    global sum_val, cnt_val, avg_val, calibrate
    sum_val[val_idx] += val
    cnt_val[val_idx] += 1
    if (cnt_val[val_idx] > 10):
        avg_val[val_idx] = sum_val[val_idx] / cnt_val[val_idx]
        print ("AVG VAL:", val_idx, avg_val[val_idx])
        calibrate -= 1

def calibrated_accel(val):
    global avg_val
    return float(round((val-avg_val[VAL_ACCEL])*9.81*10))/10.0

def calibrated_gyro(val):
    global avg_val
    return (val-avg_val[VAL_GYRO])



def handle_imu(channel, data):
    global last_timestamp
    global sum_accell
    msg = imu_t.decode(data)
#    print ("IMU:", round(msg.accel[0]*9.81*100), round(180*msg.gyro[1]/math.pi), msg.timestamp, float(msg.timestamp - last_timestamp)/1000000.0)
    if calibrate:
        calibrate_val( VAL_ACCEL, msg.accel[0] )
        calibrate_val( VAL_GYRO, msg.gyro[1] )
    else:
        if last_timestamp > 0:
            update_position( calibrated_accel( msg.accel[0] ), calibrated_gyro( msg.gyro[1] ), float(msg.timestamp - last_timestamp)/1000000.0)
    last_timestamp = msg.timestamp

lc = lcm.LCM()
lc.subscribe("IMU", handle_imu)

while True:
    lc.handle()

