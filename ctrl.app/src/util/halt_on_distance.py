#!/usr/bin/python
import argparse
import time
import lcm
from arc import distance_t
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--halt_cm', type=int,  default=20)
parser.add_argument('--unhalt_cm', type=int,  default=100)
parser.add_argument('--unhalt_req_ticks', type=int,  default=10)
args = parser.parse_args()

lc = lcm.LCM()
sent_halt = 0
seen_unhalt = 0

def lcm_distance(channel, data):
    global sent_halt
    global seen_unhalt
    m = distance_t.decode(data)
    if (sent_halt == 0) and (m.measure < args.halt_cm):
        lc.publish('CTRL_HALT', 'HALT')
        sent_halt = 1
        seen_unhalt = 0
        print("{},HALT".format( time.time() ) )
    if (sent_halt == 1) and (seen_unhalt > args.unhalt_req_ticks) and (m.measure > args.unhalt_cm):
        lc.publish('CTRL_UNHALT', 'UNHALT')
        sent_halt = 0
        print("{},UNHALT".format( time.time() ) )
    if (sent_halt):
        if m.measure > args.unhalt_cm:
            seen_unhalt += 1
        else:
            seen_unhalt = 0

lc.subscribe('DSTN', lcm_distance)

while True:
    lc.handle()
    time.sleep(0.01)
