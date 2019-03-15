#!/bin/sh
gpio -g mode 7 out
gpio -g write 7 0
avrdude -p m328p -P /dev/spidev0.0 -c linuxspi -b 10000 -U lfuse:w:0xe2:m
