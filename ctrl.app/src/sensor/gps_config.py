import sys
import time
import serial
import pynmea2
from ublox import ubx

# configure CFG-RATE, system (GPS), messages (NMEA)
# https://www.u-blox.com/sites/default/files/products/documents/u-blox6_ReceiverDescrProtSpec_%28GPS.G6-SW-10018%29_Public.pdf

port = "/dev/ttyAMA0"

serialPort = serial.Serial(port, baudrate = 9600, 
    parity=serial.PARITY_NONE, 
    stopbits=serial.STOPBITS_ONE, 
    bytesize=serial.EIGHTBITS, 
    xonxoff=False,
    rtscts=False,
    dsrdtr=False,
    exclusive=True,
    timeout = 10)

x = ubx.UbxStream(dev=serialPort)
print "Connected ..."

print "Configuring baudrate and enabling only UBX msgs sent to GPS"
x.baudrate = 9600 # it also sets only UBX in

print "Disabling not needed NMEA messages"
#GGA, GLL, GSA, GSV, VTG
for i in [0x00, 0x01, 0x02, 0x03, 0x05]:
    x.disable_message(0xF0, i)

print "Enabling only GPRMC"
x.enable_message(0xF0, 0x04) #RMC

print "Setting update frequency to 5Hz"
x.rate = 200

serialPort.close()
