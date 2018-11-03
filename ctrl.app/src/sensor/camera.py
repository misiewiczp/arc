import time
import picamera
import picamera.array
import socket
import sys

with picamera.PiCamera() as camera:
    camera.rotation = 180
    camera.framerate = 30
    camera.resolution = (1920, 1080)
    camera.start_recording('/var/dump/videos/video_{}.h264'.format( time.time() ), splitter_port=1, resize=(320,240) );

    while True:
        t = time.time()
        camera.capture('/var/dump/images/image_{}.jpeg'.format(t), format='jpeg', use_video_port=True)
        time.sleep(1)

    camera.stop_recording()

