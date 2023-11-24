from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

import simple_websocket

import random

# Initialize the Flask app.
app = Flask(__name__)
CORS(app)

# socket routes
socketio = SocketIO(app, cors_allowed_origins='*')

clients = 0
active_users = {}

colours = ['#FF1053', '#11B4FF', '#7CFF7A', '#FFD500']


@socketio.on('connect')
def handle_connect(data):
    print('Client connected')


@socketio.on('register')
def handle_register(data):
    global clients
    clients += 1
    user_id = data['userUid']
    user_first_name = data['userFirstName']
    user_last_name = data['userLastName']

    # pick a random colour from colours. if its already in use, pick another
    color = random.choice(colours)
    while color in [user['color'] for user in active_users.values()]:
        color = random.choice(colours)

    active_users[user_id] = {
        'socketId': request.sid,
        'firstName': user_first_name,
        'lastName': user_last_name,
        'userId': user_id,
        'color': color
    }
    print('User {} connected'.format(user_first_name))
    broadcast_active_users()


@socketio.on('lead-value-update')
def handle_lead_value_update(data):
    emit('lead-value-update', data, broadcast=True)


@socketio.on('disconnect')
def handle_disconnect():
    global clients
    clients -= 1
    user_id = next(key for key, value in active_users.items()
                   if value['socketId'] == request.sid)
    user_name = active_users[user_id]['firstName']
    del active_users[user_id]
    print('User {} disconnected'.format(user_name))
    broadcast_active_users()


def broadcast_active_users():
    emit('active-users', active_users, broadcast=True)


@socketio.on('cell update')
def handle_cell_update(data):
    emit('cell update', data, broadcast=True)


@socketio.on('status update')
def handle_status_update(data):
    emit('status update', data, broadcast=True)


@socketio.on('cell-hover')
def handle_cell_hover(data):
    emit('cell-hover', data, broadcast=True)


@app.route('/websocket/info')
def websocket_info():
    # Get number of connected clients
    # clients = len(socketio.server.eio.clients)
    return active_users


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)