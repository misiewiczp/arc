#!/bin/sh
START=`date +%Y%m%d%H%M%S`
DUMP_DIR=/var/dump/${START}/

trap cleanup 1 2 3 6 15

cleanup()
{
    echo "Cleaning ..."
    killall -SIGTERM python || true
    killall cat || true
    exit 0
}

lcm-gen -p arc.lcm
mkdir -p ${DUMP_DIR}
mkdir -p ${DUMP_DIR}/image
mkdir -p ${DUMP_DIR}/video

rm -f ${DUMP_DIR}/../latest
ln -s ${DUMP_DIR} ${DUMP_DIR}/../latest

start_distance(){
	python src/sensor/distance.py --print >> ${DUMP_DIR}/distance.csv
}

start_imu(){
	python src/sensor/imu.py --print >> ${DUMP_DIR}/imu.csv
}

start_gps(){
#	python src/sensor/gps.py --print >> ${DUMP_DIR}/gps.csv &
	cat /dev/ttyAMA0 | grep -v unknown >> ${DUMP_DIR}/gps.csv
}

start_camera(){
	python src/sensor/camera.py ${DUMP_DIR}
}


start_distance &
start_imu &
start_gps &
start_camera &

wait
