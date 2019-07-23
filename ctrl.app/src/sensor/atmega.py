import spidev
import time
import struct
import lcm
from arc import distance_t
from arc import control_t
import sys

bPrint = 0
if (len(sys.argv) > 1 and sys.argv[1] == '--print'):
    bPrint = 1


spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 50000 
lastidx = -1

d_t = distance_t()
c_t = control_t()
lc = lcm.LCM()

while True:
   t = long(time.time()*1000*1000)
   resp = spi.xfer2([0x01, 0,0, 0,0, 0,0, 0,0, 0,0, 0, 0, 0])
#   print resp
   dist = (int(resp[3])<<8)+resp[2]
   motor_read = (int(resp[5])<<8)+resp[4]
   servo_read = (int(resp[7])<<8)+resp[6]

   motor_applied = (int(resp[9])<<8)+resp[8]
   servo_applied = (int(resp[11])<<8)+resp[10]

   idx = resp[12]
   is_autonomous = resp[13]
   if lastidx <> idx:
       d_t.measure = dist
       d_t.timestamp = t
       lc.publish("DSTN", d_t.encode())
       c_t.timestamp = t
       c_t.motor = motor_applied
       c_t.servo = servo_applied
       lc.publish('CTRL_LOG', c_t.encode())
       if bPrint:
           print("{},{},{},{},{},{}".format(int(t/1000), idx, dist, motor_applied, servo_applied, is_autonomous))
   lastidx = idx
   time.sleep(0.01)
