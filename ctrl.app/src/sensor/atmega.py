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
