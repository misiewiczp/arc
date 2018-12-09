from flask import Flask,render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kaksadhajkdwyeuiqqxmZB'
#app.config['host']='0.0.0.0'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('index.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('CTRL')
def handle_CTRL_event(json, methods=['GET', 'POST']):
    print('CTRL req: ' + str(json))
    socketio.emit('CTRL_LOG', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=False)
