import sys
import time
import serial
import pynmea2
import lcm
from arc import gps_t

# configure CFG-RATE, system (GPS), messages (NMEA)
# https://www.u-blox.com/sites/default/files/products/documents/u-blox6_ReceiverDescrProtSpec_%28GPS.G6-SW-10018%29_Public.pdf

bPrint = 0
if (len(sys.argv) > 1 and sys.argv[1] == '--print'):
    bPrint = 1


port = "/dev/ttyAMA0"


g_t = gps_t()
lc = lcm.LCM()

def publishGPS(str):
    try:
        msg = pynmea2.parse(str)
        if msg.is_valid:
            g_t.timestamp = long(time.time()*1000*1000)
            g_t.lat = msg.latitude
            g_t.lon = msg.longitude
            g_t.vel = float(spd_over_grnd)
            lc.publish("GPS", g_t.encode())
    except pynmea2.nmea.ParseError as pe:
        if bPrint:
            print pe

    if bPrint:
        print(time.time(), str)



while True:
    serialPort = serial.Serial(port, baudrate = 9600, 
        parity=serial.PARITY_NONE, 
        stopbits=serial.STOPBITS_ONE, 
        bytesize=serial.EIGHTBITS, 
        xonxoff=True,
        rtscts=False,
        dsrdtr=False,
        exclusive=True,
        timeout = 10)
    try:
        while True:
            str = serialPort.readline()
            if str.find('RMC') > 0:
                publishGPS(str)
    except serial.SerialException as e:
        if bPrint:
            print e
        serialPort.close()
        time.sleep(0.1)

