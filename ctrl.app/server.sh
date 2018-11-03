#!/bin/sh

DUMP_DIR=/var/dump/

trap cleanup 1 2 3 6 15

cleanup()
{
    echo "Cleaning ..."
    killall python || true
    exit 0
}

lcm-gen -p arc.lcm
mkdir -p ${DUMP_DIR}

start_distance(){
	python src/sensor/distance.py --print >> ${DUMP_DIR}/distance.csv
}

start_imu(){
	python src/sensor/imu.py --print >> ${DUMP_DIR}/imu.csv
}

start_gps(){
#	python src/sensor/gps.py --print >> ${DUMP_DIR}/gps.csv &
	cat /dev/ttyAMA0 | grep GPRMC >> ${DUMP_DIR}/gps.csv
}

start_camera(){
	python src/sensor/camera.py
}


start_distance &
start_imu &
start_gps &
start_camera &

wait
