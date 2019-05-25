CC=gcc
CFLAGS=-Isrc -Isrc/lcm/include
LDFLAGS=-L. -llcm
DUMP_DIR=/var/dump/



lcm: 
	lcm-gen -c --c-cpath=src/lcm/c --c-hpath=src/lcm/c/include arc.lcm
	lcm-gen --cpp --cpp-hpath=src/lcm/cpp --cpp-include=src/lcm/cpp/include arc.lcm
	lcm-gen -p arc.lcm

init:
	mkdir -p ${DUMP_DIR}

start_distance: init
	python src/sensor/distance.py --print >> ${DUMP_DIR}/distance.csv &

start_imu: init
	python src/sensor/imu.py --print >> ${DUMP_DIR}/imu.csv &

start_gps: init
#	python src/sensor/gps.py --print >> ${DUMP_DIR}/gps.csv &
	cat /dev/ttyAMA0 | grep GPRMC >> ${DUMP_DIR}/gps.csv &

start_camera: init
	python src/sensor/camera.py --stdout >> ${DUMP_DIR}/camera.csv &

start_sensors: start_distance start_imu start_gps start_camera
	echo "DONE"


start_pigpio:
	killall pigpiod || true
	nohup pigpiod &


start_ctrl: start_pigpio
	export LD_LIBRARY_PATH=/usr/local/lib
	python src/actuator/controller.py


stop_all:
	killall python || killall pigpiod || true


clean:
