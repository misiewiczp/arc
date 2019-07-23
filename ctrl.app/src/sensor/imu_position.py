#!/usr/bin/python
import sys, getopt
sys.path.append('.')
import RTIMU
import os.path
import time
import math
import lcm
from arc import imu_t
from pykalman import KalmanFilter


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

dt = poll_interval*1.0/1000.0

# transition_matrix  
F = [[1, dt, 0.5*dt**2], 
     [0,  1,       dt],
     [0,  0,        1]]

# observation_matrix   
H = [0, 0, 1]

# transition_covariance 
Q = [[0.2,    0,      0], 
     [  0,  0.1,      0],
     [  0,    0,  10e-4]]

R = 0.0020

X0 = [0,0,0]

P0 = [[  0,    0,               0], 
      [  0,    0,               0],
      [  0,    0,   		R]]


kf = KalmanFilter(transition_matrices = F, 
                  observation_matrices = H, 
                  transition_covariance = Q, 
                  observation_covariance = R, 
                  initial_state_mean = X0, 
                  initial_state_covariance = P0)

fsm = X0
fsc = P0

i_t = imu_t()
lc = lcm.LCM()

log_step = 0

while True:
    hack = int(time.time()*1000)

    if imu.IMURead():
        data = imu.getIMUData()
        pitch, roll, yaw = imu.getFusionData()
        accel = data['accel']

        fsm, fsc = kf.filter_update( fsm, fsc, accel[0] )
        if (log_step % 50 == 0):
            print("%f %f %f" % (pitch/math.pi*180,roll/math.pi*180,yaw/math.pi*180))
            print("%f %f %f" % (accel[0], accel[1], accel[2]))
            print("%f %f %f" % (fsm[0], fsm[1], fsm[2]))
            print( fsc )

        log_step += 1

        timestamp = int(data['timestamp']/1000)

    time.sleep( dt ) #0.004 - 250Hz
