import time
import picamera
import picamera.array
import sys
from signal import *

dump_dir = sys.argv[1]

bRun = True

def fn_handler(signum, frame, camera):
    camera.stop_recording()
    bRun = False
    sys.exit(0)

with picamera.PiCamera() as camera:
    camera.rotation = 180
    camera.framerate = 30
    camera.resolution = (1920, 1080)
    camera.start_recording(dump_dir + '/video/video_{}.h264'.format( time.time() ), splitter_port=1, resize=(640,480) );

    handler = lambda signum,frame: fn_handler(signum, frame, camera)

    signal(SIGINT, handler )
    signal(SIGTERM, handler )


    while bRun:
        t = time.time()
        camera.capture(dump_dir + '/image/image_{}.jpeg'.format(t), format='jpeg', use_video_port=True)
        time.sleep(1)

    camera.stop_recording()


