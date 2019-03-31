import time
import picamera
import picamera.array
import sys
from signal import *
import socket
from threading import Thread
from arc import camera_t
import lcm

dump_dir = sys.argv[1]

lc = lcm.LCM()

bRun = True

def fn_handler(signum, frame, camera):
    global bRun
    print "Handle SIGNAL", signum
    camera.stop_recording()
    bRun = False
    print "Stopped recording ..  waiting to exit"
#    sys.exit(0)

connection = 0

def wait_connection():
    global bRun
    global connection
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(0)
    server_socket.settimeout(5)
    while bRun:
        try:
            connection = server_socket.accept()[0].makefile('wb')
            print "Have new connection"
        except socket.timeout:
            pass


thread = Thread(target = wait_connection)
thread.start();

class DuplexOutput(object):

    def __init__(self, filename):
        self.file_stream = open(filename, 'wb')

    def write(self, s):
        self.file_stream.write(s)
        global connection
        if (connection):
            connection.write(s)

    def flush(self):
        self.file_stream.flush()
        global connection
        if (connection):
            connection.flush()

    def close(self):
        self.file_stream.close()
        global connection
        if (connection):
            connection.close()


with picamera.PiCamera() as camera:
    camera.rotation = 180
    camera.framerate = 30
    camera.resolution = (1920, 1080)
    camera.start_recording( DuplexOutput( dump_dir + '/video/video_{}.h264'.format( time.time()*1000 ) ), splitter_port=1, resize=(640,480), format='h264', profile='baseline' );

    handler = lambda signum,frame: fn_handler(signum, frame, camera)

    signal(SIGINT, handler )
    signal(SIGTERM, handler )

    c_t = camera_t()
    while bRun:
        t = time.time()
        c_t.timestamp = t*1000*1000
        c_t.filename = dump_dir + '/image/image_{}.jpeg'.format(t*1000)
        camera.capture(c_t.filename, format='jpeg', use_video_port=True)
        lc.publish('CAMERA', c_t.encode())
        print c_t.filename
        time.sleep(1)

#    camera.stop_recording()



