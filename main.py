from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit

import random
import simple_websocket

# Initialize the Flask app.
app = Flask(__name__)
CORS(app)

# socket routes
socketio = SocketIO(app, cors_allowed_origins='*')


@socketio.on('connect')
def handle_connect():
    print('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


@socketio.on('cell update')
def handle_cell_update(data):
    emit('cell update', data, broadcast=True)


@socketio.on('status update')
def handle_status_update(data):
    emit('status update', data, broadcast=True)
    
@app.route('/hello_world')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    socketio.run(app, debug=True)