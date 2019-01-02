import threading
import time
from flask import Flask,render_template,send_from_directory
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

c_t = control_t()

lastMsgTime = {"DSTN":0}
TIME_LIMIT=0.5 # update twice a second

def lc_handle():
    while runLoop:
        lc.handle_timeout(10)
        eventlet.sleep(0.1) # otherwise emit's wait for long time

#thread = threading.Thread(target=run_job)
#thread.start()
eventlet.spawn( lc_handle )

@app.route('/')
def sessions():
    return render_template('index.html')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('CTRL')
def handle_CTRL_event(json, methods=['GET', 'POST']):
    print('CTRL req: ' + str(json))
    c_t.timestamp = time.time()
    c_t.servo = json['s']
    c_t.motor = json['m']
    lc.publish('CTRL', c_t.encode())

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
    print(m.motor, m.servo)
    socketio.emit('CTRL_LOG', {'m':m.motor, 's':m.servo})

lc.subscribe("DSTN", lcm_dstn)
lc.subscribe("CTRL_LOG", lcm_ctrl_log)


if __name__ == '__main__':
    try:
        print "Starting server ..."
        socketio.run(app, host='0.0.0.0', port=9080, debug=True)
        runLoop = False
    except KeyboardInterrupt:
        runLoop = False
