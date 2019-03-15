PROG_NAME=pwm16
ARDUINO_DIR=/usr/share/arduino
BOARD_TAG=uno
F_CPU=8000000L
ARDUINO_PORT = 
ARDUINO_LIBS = 
include /usr/share/arduino/Arduino.mk


install:
	gpio -g write 7 0
	avrdude -p m328p -P /dev/spidev0.0 -c linuxspi -b 10000 -e -U flash:w:build-uno/${PROG_NAME}.hex

run:
	gpio -g write 7 1
