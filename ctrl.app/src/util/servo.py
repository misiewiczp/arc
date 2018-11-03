#!/usr/bin/python
import argparse
import time
import lcm
from arc import control_servo_t
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--prc', type=int,  default=0)
parser.add_argument('--time', type=int, default=5)
args = parser.parse_args()
#print(args)
#print(args.prc)
#sys.exit()

lc = lcm.LCM()

msg = control_servo_t()
msg.timestamp = time.time()
msg.servo = args.prc
lc.publish('CTRL_SERVO', msg.encode())
time.sleep( args.time )
msg.timestamp = time.time()
msg.servo = 0
lc.publish('CTRL_SERVO', msg.encode())
