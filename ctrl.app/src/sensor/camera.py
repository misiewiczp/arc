import time
import picamera
import picamera.array
import sys
from signal import *
import socket
from threading import Thread

dump_dir = sys.argv[1]

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
    camera.start_recording( DuplexOutput( dump_dir + '/video/video_{}.h264'.format( time.time() ) ), splitter_port=1, resize=(640,480), format='h264', profile='baseline' );

    handler = lambda signum,frame: fn_handler(signum, frame, camera)

    signal(SIGINT, handler )
    signal(SIGTERM, handler )


    while bRun:
        t = time.time()
        camera.capture(dump_dir + '/image/image_{}.jpeg'.format(t), format='jpeg', use_video_port=True)
        time.sleep(1)

#    camera.stop_recording()



