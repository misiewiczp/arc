import lcm
from arc import req_plan_path_t
from arc import res_plan_path_t
import time
import sys
import math

lc = lcm.LCM()

def calc_dist(lat_x, lng_x, lat_y, lng_y):
    r_lat_x = lat_x * math.pi / 180.0
    r_lat_y = lat_y * math.pi / 180.0
    d_r_lat = (lat_y-lat_x) * math.pi / 180.0
    d_r_lng = (lng_y-lng_x) * math.pi / 180.0
    a = math.sin(d_r_lat/2)**2 + math.cos(r_lat_x)*math.cos(r_lat_y)*(math.sin(d_r_lng/2)**2)
    c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a) )
    dist = c * 6371000.0 # earths diagonal
    
    return (dist)

def calc_dist_brng(lat_x, lng_x, lat_y, lng_y):
    r_lat_x = lat_x * math.pi / 180.0
    r_lat_y = lat_y * math.pi / 180.0
    d_r_lat = (lat_y-lat_x) * math.pi / 180.0
    d_r_lng = (lng_y-lng_x) * math.pi / 180.0
    a = math.sin(d_r_lat/2)**2 + math.cos(r_lat_x)*math.cos(r_lat_y)*(math.sin(d_r_lng/2)**2)
    c = 2 * math.atan2( math.sqrt(a), math.sqrt(1-a) )
    dist = c * 6371000.0 # earths diagonal
    
    y = math.sin( d_r_lng )*math.cos(r_lat_y)
    x = math.cos(r_lat_x)*math.sin(r_lat_y)-math.sin(r_lat_x)*math.cos(r_lat_y)*math.cos( d_r_lng )
    brng = math.atan2( y, x )*180.0/math.pi
    return (dist, brng)



def response_handler_gps(channel, data):
    msg = res_plan_path_t.decode(data);
    print(msg.points_x, msg.points_y)
    for i in range(1, msg.npoints-1):
        dist,brng = calc_dist_brng(msg.points_x[i], msg.points_y[i], msg.points_x[i+1], msg.points_y[i+1] )
        rel_x = calc_dist(msg.points_x[i], msg.points_y[i], msg.points_x[i+1], msg.points_y[i] )
        rel_y = calc_dist(msg.points_x[i], msg.points_y[i], msg.points_x[i], msg.points_y[i+1] )
        print (rel_x, rel_y, brng, dist)

    


    sys.exit();

lc.subscribe('GPS_RES', response_handler_gps)

msg = req_plan_path_t()
msg.timestamp = int(time.time()*1000)
msg.src[0] = float(sys.argv[1])
msg.src[1] = float(sys.argv[2])
msg.dst[0] = float(sys.argv[3])
msg.dst[1] = float(sys.argv[4])

lc.publish('GPS_REQ', msg.encode())

try:
#    while True:
    lc.handle_timeout(5000)
#    time.sleep(0.1)
except KeyboardInterrupt:
    pass
