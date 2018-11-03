#Libraries
import sys
import time
import lcm
import RPi.GPIO as GPIO
from signal import *
from arc import distance_t
import sys

bPrint = 0
if (sys.argv[1] == '--print'):
    bPrint = 1


#GPIO.setwarnings(False)

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 16
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
def clean(*args):
    GPIO.cleanup()
    sys.exit(0)


for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
    signal(sig, clean)


d_t = distance_t()
lc = lcm.LCM()

while True:
    d_t.measure = distance()
    d_t.timestamp = long(time.time()*1000*1000)
    lc.publish("DSTN", d_t.encode())
    if bPrint:
        print( "{},{}".format(d_t.timestamp, round(d_t.measure)) )
    time.sleep(0.1)
