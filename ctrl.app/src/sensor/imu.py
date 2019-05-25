#!/usr/bin/python
import sys, getopt
sys.path.append('.')
import RTIMU
import os.path
import time
import math
import lcm
from arc import imu_t, imu_fusion_t

bPrint = 0
if (len(sys.argv) > 1 and sys.argv[1] == '--print'):
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

print (poll_interval)

i_t = imu_t()
if_t = imu_fusion_t()
lc = lcm.LCM()

log_step = 0

while True:
    hack = int(time.time()*1000)

    if imu.IMURead():
        data = imu.getIMUData()

        accel = data['accel']
        gyro = data['gyro']
        comp = data['compass']
        fusionPose = data["fusionPose"]
        pitch, roll, yaw = imu.getFusionData()
        if (log_step % 50 == 0):
            # pitch, roll, yaw
            print("%f %f %f" % (pitch/math.pi*180,roll/math.pi*180,yaw/math.pi*180))
#            print("%f %f %f" % (accel[0], accel[1], accel[2]))
        log_step += 1

#        temp = data['temperature']
#        press = data['pressure']
        timestamp = int(data['timestamp']/1000)

        i_t.timestamp = timestamp
        i_t.accel = accel
        i_t.gyro = gyro
        i_t.compass = comp
        if log_step % 10 == 0:
            lc.publish("IMU", i_t.encode())

        if_t.timestamp = timestamp
        if_t.yaw = yaw
        if_t.pitch = pitch
        if_t.roll = roll
        if log_step % 10 == 0:
            lc.publish("IMU_FUSION", if_t.encode())

# gyro - OK
#        omega = round(180*gyro[2]/math.pi) #BAD
        omega = round(180*gyro[1]/math.pi) #OK
# accel - might be
        a0 = -(round(accel[0]*9.81*10)) # in 0.1m/s

# compass - needs calibration
#        fusion = data['fusionPose']
#        heading = round(fusion[2]*180/math.pi)
        c = (comp[0]-31, comp[1]-(-30.5), comp[2]-14.5)
        
        heading = math.atan2(comp[0]-31, comp[2] - 14.5)/math.pi*180
#        q = data['fusionQPose']
#        yaw = math.atan2(2.0 * (q[1] * q[2] + q[0] * q[3]), q[0] * q[0] + q[1] * q[1] - q[2] * q[2] - q[3] * q[3])
#        yaw = yaw*180.0/math.pi
#        print(yaw)

        if bPrint:
#            print ("{},{},{},{},{},{}".format( timestamp, round(omega), round(a0), round(comp[0]), round(comp[1]), round(comp[2]) ) )
#            print ("fmt {},{},{},{},{},{}".format( timestamp, round(omega), round(a0), comp[0], comp[1], comp[2] ) )
            print ("{},{},{},{},{},{},{},{},{},{},{}".format(hack,timestamp,accel[0],accel[1],accel[2], gyro[0],gyro[1],gyro[2], comp[0],comp[1],comp[2]))
            

#            print ( "{},{},{},{}".format(timestamp, round(omega), round(a0), round(heading)) )
#            print (comp2)
#            print( "{},{},{},{},{},{}".format( math.atan2(c[1],c[0]), math.atan2(c[2],c[0]), math.atan2(c[2],c[1]), math.atan2(c[0],c[1]), math.atan2(c[0],c[2]), math.atan2(c[1],c[2]) ) )

#    else:

    time.sleep(poll_interval*1.0/1000.0) #0.004 - 250Hz
