import lcm
from arc import req_plan_path_t
from arc import res_plan_path_t
import time
import sys
import math

lc = lcm.LCM()

def response_handler_gtc(channel, data):
    msg = res_plan_path_t.decode(data);
    print(msg.points_x, msg.points_y)
    sys.exit();

lc.subscribe('GTC_RES', response_handler_gtc)

msg = req_plan_path_t()
msg.timestamp = int(time.time()*1000)
msg.src = [float(sys.argv[1]),float(sys.argv[2])]
msg.dst = [float(sys.argv[3]),float(sys.argv[4])]
msg.yaw = float(sys.argv[5])
msg.nroad_points = int((len(sys.argv) - 5) / 3)
msg.road_x = [float(sys.argv[i]) for i in range(6, len(sys.argv), 3)]
msg.road_y = [float(sys.argv[i]) for i in range(6+1, len(sys.argv), 3)] # for clarity
msg.road_w = [float(sys.argv[i]) for i in range(6+2, len(sys.argv), 3)] # for clarity

lc.publish('GTC_REQ', msg.encode())

try:
#    while True:
    lc.handle_timeout(10000)
#    time.sleep(0.1)
except KeyboardInterrupt:
    pass
