from pyroutelib3 import Router
import lcm
from arc import req_plan_path_t, res_plan_path_t
import time
import sys

lc = lcm.LCM()

router = Router("cycle", "map.osm")


def request_handler_gps(channel, data):
    msg = req_plan_path_t.decode(data);
    start = router.findNode(msg.src[0], msg.src[1]) # Find start and end nodes
    end = router.findNode(msg.dst[0], msg.dst[1])
    print(start, end)
    status, route = router.doRoute(start, end) 
    # Find the route - a list of OSM nodes
    if status == 'success':
        rll = list(map(router.nodeLatLon, route))
        res = res_plan_path_t()
        res.timestamp = int(time.time()*1000)
        res.req_timestamp = msg.timestamp
        res.npoints = len(rll)
        res.points_x = [pt[0] for pt in rll]
        res.points_y = [pt[1] for pt in rll]
        lc.publish('GPS_RES', res.encode())
        print(rll)
    else:
        print (status)

lc.subscribe('GPS_REQ', request_handler_gps)

print("Initialized")

try:
    while True:
        lc.handle()
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
