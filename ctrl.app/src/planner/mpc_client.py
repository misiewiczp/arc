import lcm
from arc import req_plan_mpc_t
from arc import res_plan_mpc_t
import time
import sys
import math

lc = lcm.LCM()

start = 0

def response_handler_mpc(channel, data):
    global start
    msg = res_plan_mpc_t.decode(data);
    print((time.time()-start), msg.delta_dir, msg.delta_acc, msg.points_x, msg.points_y)
    sys.exit();

lc.subscribe('MPC_RES', response_handler_mpc)

msg = req_plan_mpc_t()
msg.timestamp = int(time.time()*1000)
msg.x = float(sys.argv[1])
msg.y = float(sys.argv[2])
msg.yaw = float(sys.argv[3])
msg.vel = float(sys.argv[4])
msg.acc = float(sys.argv[5])
msg.dir = float(sys.argv[6])
msg.ref_vel = 5 #m/s
msg.latency = 0.1 #s
msg.npoints = int((len(sys.argv) - 6) / 2)
msg.points_x = [float(sys.argv[i]) for i in range(7, len(sys.argv), 2)]
msg.points_y = [float(sys.argv[i+1]) for i in range(7, len(sys.argv), 2)] # for clarity

start = time.time()
lc.publish('MPC_REQ', msg.encode())

try:
#    while True:
    lc.handle_timeout(5000)
#    time.sleep(0.1)
except KeyboardInterrupt:
    pass
