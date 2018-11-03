#!/usr/bin/python
import sys, getopt
sys.path.append('.')
import RTIMU
import os.path
import time
import math
import lcm

bPrint = 0
if (sys.argv[1] == '--print'):
    bPrint = 1

   
SETTINGS_FILE = "RTIMULib"
s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)  
   
if (not imu.IMUInit()):  
    sys.exit(1)  
   
imu.setSlerpPower(0.02)  
imu.setGyroEnable(True)  
imu.setAccelEnable(True)  
imu.setCompassEnable(True)  
   
poll_interval = imu.IMUGetPollInterval()  

while True:
    hack = time.time()  

    if imu.IMURead():
        data = imu.getIMUData()
        accel = data['accel']
        gyro = data['gyro']
        comp = data['compass']
#        temp = data['temperature']
#        press = data['pressure']
        timestamp = data['timestamp']

# gyro - OK
        omega = round(180*gyro[2]/math.pi)

# accel - might be
        a0 = -(round(accel[0]*9.81*10)) # in 0.1m/s

# compass - needs calibration
#        fusion = data['fusionPose']
#        heading = round(fusion[2]*180/math.pi)
#        heading = math.atan2(comp[2], comp[1])/math.pi*180
#        q = data['fusionQPose']
#        yaw = math.atan2(2.0 * (q[1] * q[2] + q[0] * q[3]), q[0] * q[0] + q[1] * q[1] - q[2] * q[2] - q[3] * q[3])
#        yaw = yaw*180.0/math.pi
#        print(yaw)

        if bPrint:
            print ("{},{},{},{},{},{}".format( timestamp, round(omega), round(a0), round(comp[0]), round(comp[1]), round(comp[2]) ) )

    time.sleep(0.1) 
    #poll_interval*1.0/1000.0)
