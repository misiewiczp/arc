#!/usr/bin/python
import argparse
import time
import lcm
from arc import control_t
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--prc_servo', type=int,  default=0)
parser.add_argument('--prc_motor', type=int,  default=0)
parser.add_argument('--time', type=int, default=5)
args = parser.parse_args()
#print(args)
#print(args.prc)
#sys.exit()

lc = lcm.LCM()

msg = control_t()
msg.timestamp = time.time()
msg.motor = args.prc_motor
msg.servo = args.prc_servo
lc.publish('CTRL', msg.encode())
time.sleep( args.time )
msg.timestamp = time.time()
msg.motor = 0
msg.servo = args.prc_servo
lc.publish('CTRL', msg.encode())
