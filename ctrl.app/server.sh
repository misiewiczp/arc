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

start_atmega(){
	python src/sensor/atmega.py --print >> ${DUMP_DIR}/atmega.csv
}


start_imu(){
	python src/sensor/imu.py --print >> ${DUMP_DIR}/imu.csv
}

start_gps(){
	python src/sensor/gps.py --print >> ${DUMP_DIR}/gps.csv
}

start_camera(){
	python src/sensor/camera.py ${DUMP_DIR}
}

start_ctrl(){
	python src/actuator/controller.py --print >> ${DUMP_DIR}/ctrl.csv
}

start_halt(){
	python src/util/halt_on_distance.py >> ${DUMP_DIR}/halt.csv
}


#start_halt &
#start_distance &
start_atmega &
start_imu &
#start_gps &
start_camera &
#start_ctrl &

wait
# copy
#rsync -avzr --include="*.csv" --include="*/" --exclude="*" /var/dump/ pi@aisoft.com.pl:/work/diska/pi/dump/
