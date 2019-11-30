#!/usr/bin/python
import argparse
import time
import lcm
from arc import control_t
import sys
import math
import numpy as np
import acado


parser = argparse.ArgumentParser()
parser.add_argument('--x', type=float,  default=0)
parser.add_argument('--y', type=float,  default=0)
#parser.add_argument('--time', type=int, default=5)
args = parser.parse_args()
#print(args)

SPEED=1.
NX=5 #x, y, v, yaw,st
NU=2 #acceleration, angle
NY=2
NYN=NY
T=20

PX = np.array([0., args.x])
PY = np.array([0., args.y])


RAD_90 = math.pi / 2
def find_cont(x, y, ax, ay):
    tx = [x]
    ty = [y]       
    START = 0
    
    while ((x - ax[START])**2 + (y-ay[START])**2 < .01 and START+1 < len(ax)):
        START = START+1
    
    if (START+1 == len(ax)): # ostatni element - nie ma co szukac dalej
        tx.append(ax[START])
        ty.append(ay[START])
        return tx,ty
    
    min = (x - ax[START])**2 + (y-ay[START])**2    
    # czy to jest stabilne do dodawania ???
    tga = math.atan2(ay[START+1]-ay[START], ax[START+1] - ax[START]) + math.atan2(-y+ay[START], -x + ax[START])
    for i in range(1, len(ax) ):      
#        print (tga/math.pi*180., min)
        dst = (x - ax[i])**2 + (y-ay[i])**2
        if dst > min:
            if abs(tga) >= RAD_90 and min > .25: #jeszcze trzeba dojechaz do najblizszego punktu
                tx.extend(ax[(i-1):]) 
                ty.extend(ay[(i-1):])
            else:
                tx.extend(ax[i:]) 
                ty.extend(ay[i:])
            break
        else:
            min = (x - ax[i])**2 + (y-ay[i])**2
            if i < len(ax)-1:
                tga = math.atan2(ay[i+1]-ay[i], ax[i+1] - ax[i]) + math.atan2(-y+ay[i], -x + ax[i])
            else: # zostal ostatni
                tx.extend(ax[i:]) 
                ty.extend(ay[i:])
                break
    
    return tx, ty


def next_steps(x, y, ax, ay, v, dt, T):
    tx = [x]
    ty = [y]
    t = 1
    for nx, ny in zip(ax, ay):
        steps = ((nx-x)**2+(ny-y)**2)**.5/v/dt
        dx = (nx-x) / steps
        dy = (ny-y) / steps
        for i in range( int(steps)+1 ):
            if t >= T:
                return tx, ty
            x = x+dx
            y = y+dy
            tx.append(x)
            ty.append(y)
            t = t+1
            if abs(x - nx) + abs(y - ny) < 0.1:
                break

    ltx = len(tx)
    while (ltx < T): 
        tx.append(tx[ltx-1])
        ty.append(ty[ltx-1])
        ltx = ltx+1
    return tx, ty


### replace by acado.sim
# CONSTANTS
mass = 2.120;
Lr = .15;
Lf = .15;
L = Lr+Lf;	# vehicle wheel base
dt = .02;   # sampling time for discrete-time system
    
# PARAMS
th_b = 5.;
th_K = 15.;
st_b = 10.;
st_K = math.pi/6.;

def predict_motion(X, U, dt, T):
    x, y, v, yaw, st = X[0,0], X[0,1], X[0,2], X[0,3], X[0,4]
    ax, ay, av, ayaw, ast = [x],[y],[v],[yaw],[st]
    for i in range(T):
        u_th, u_st = U[i,0], U[i,1]        
        beta = math.atan2( Lr * math.tan(st), L );
        x = x+v*dt*math.cos(yaw+beta);
        y = y+v*dt*math.sin(yaw+beta);
        v = v+(-v*th_b+th_b*th_K*u_th)/mass*dt;
        st = st+(-st*st_b+st_b*st_K*u_st)*dt;
        yaw = yaw+v*dt*math.sin(beta)/Lr;
        while yaw >= math.pi*2:
            yaw = yaw - math.pi*2
        while yaw <= -math.pi*2:
            yaw = yaw + math.pi*2            
        ax.append(x)
        ay.append(y)
        av.append(v)
        ayaw.append(yaw)
        ast.append(st)

    return ax, ay, av, ayaw, ast



def mpc(T, x0, y0, v0, yaw0, st0, tx, ty, X, U):
    x0 = np.array( [x0, y0, v0, yaw0, st0] ).reshape( (1,NX) )

    Y=np.zeros((T,NY))
    yN=np.zeros((1,NY))
    Q = np.diag([1.,1.])  # state cost matrix ([0.5, 0.5, 1.0, 1.0])  
    #Qf = np.diag([1.0, 1.0, 0.1, 1.0])  # state cost matrix
    Qf = Q
## ? czemu nie przesuwamy o -1 ?
    Y[:,0]=np.array(tx)
    Y[:,1]=np.array(ty) 
   
    yN[0,0]=tx[T-1]
    yN[0,1]=ty[T-1]

    for i in range(1):
        ax, ay, av, ayaw, ast = predict_motion(X, U, dt, T)        #X, x0 ?
        for j in range(T):
            X[j,:] = ax[j], ay[j], av[j], ayaw[j], ast[j]
        result, objective, X, U = acado.mpc(0, 1, x0,X,U,Y,yN, np.transpose(np.tile(Q,T)), Qf, 0)
        print (result, objective)
    
    return (objective, X, U)

lc = lcm.LCM()

def set_ctrl(throttle, servo):
    msg = control_t()
    msg.timestamp = time.time()
    if (throttle < 0):
        throttle = 0.
    if (throttle > 0):
        throttle = 15+throttle*85
    msg.motor = -int(throttle) # do przodu
    msg.servo = int(servo*100.)
    lc.publish('CTRL', msg.encode())

x,y,v,yaw,st = [0.,0.,0.,0.,0.]
px, py = [PX.flatten()[1:], PY.flatten()[1:]]
dst_x = px[len(px)-1]
dst_y = py[len(py)-1]
nx, ny = next_steps(x,y,px, py, SPEED,.02, 20)
mx = []
my = []
myaw = []
mv = []
mst = []
mu_th = []
mu_st = []
mobj = []

U=np.zeros((T,NU))
U[:,0] = np.ones(T)
X=np.zeros((T+1,NX))

start = time.time()
for i in range(1000):
    mx.append(x)
    my.append(y)
    myaw.append(yaw)
    mv.append(v)
    mst.append(st)
    if (x - dst_x)**2 + (y - dst_y)**2 < .25 and len(px) <= 2:
        print ("REACHED GOAL !!!")
        break
    objective, X, U = mpc(20, x,y,v,yaw,st,nx,ny, X, U) ### czy przekazywac X, U wczesniej wyliczone ???
    mobj.append(objective)
#    print(U[:,1])
    # localization after 1 steps of mpc
    x,y,v,yaw,st = X[1,:]
    u_th, u_st = U[1,:]
    mu_th.append(u_th)
    mu_st.append(u_st)
    set_ctrl(u_th, u_st)
    nx_old, ny_old = nx, ny
    nx, ny = find_cont(x, y, nx, ny) #nx[1:], ny[1:])
#    print(nx, ny)
    #plt.figure()
    if len(nx) != 20:
        px, py = find_cont(x, y, px, py)
#        plt.plot(px[0:2],py[0:2])
        nx, ny = next_steps(x,y, px[1:], py[1:], SPEED,.02, 20)        
        if len(nx) != 20:
            print ("NO MORE STEPS !!!")
            break

set_ctrl(0., 0.)
end = time.time()

print('MX', mx)
print('MY', my)
print('Throttle', mu_th)
print('Steer', mu_st)
print('Velocity', mv)
print('Liczba krokow:', len(mx), 'Czas: ', end-start)




