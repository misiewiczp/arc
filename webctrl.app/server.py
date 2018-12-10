import threading
import time
from flask import Flask,render_template
from flask_socketio import SocketIO
import eventlet
import lcm
from arc import control_t, distance_t, imu_t

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kaksadhajkdwyeuiqqxmZB'
#app.config['host']='0.0.0.0'
socketio = SocketIO(app)
lc = lcm.LCM()
runLoop = True

lastMsgTime = {"DSTN":0}
TIME_LIMIT=0.5 # update twice a second

@app.before_first_request
def activate_job():
    def run_job():
        while runLoop:
            lc.handle()
            eventlet.sleep(0) # otherwise emit's wait for long time
    thread = threading.Thread(target=run_job)
    thread.start()


@app.route('/')
def sessions():
    return render_template('index.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('CTRL')
def handle_CTRL_event(json, methods=['GET', 'POST']):
    print('CTRL req: ' + str(json))
    socketio.emit('CTRL_LOG', json, callback=messageReceived)

def skip_emit(queue, json):
    global lastMsgTime
    if time.time() - lastMsgTime[queue] > TIME_LIMIT:
        socketio.emit(queue, json)
        lastMsgTime[queue]=time.time()

def lcm_dstn(channel, data):
    m = distance_t.decode(data)
    skip_emit('DSTN', {'m':m.measure})

def lcm_ctrl_log(channel, data):
    m = control_t.decode(data)
    socketio.emit('CTRL_LOG', {'m':m.motor, 's':m.servo})

lc.subscribe("DSTN", lcm_dstn)
lc.subscribe("CTRL_LOG", lcm_ctrl_log)


if __name__ == '__main__':
    try:
        socketio.run(app, host='0.0.0.0', debug=False)
        runLoop = False
    except KeyboardInterrupt:
        runLoop = False
