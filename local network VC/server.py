from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global variables to store connection status
connections = {
    'sanskar': False,
    'anubhav': False
}


@socketio.on('connect_user')
def handle_connect_user(data):
    user = data['user']
    if user in connections:
        connections[user] = True
        emit('user_connected', {'user': user, 'status': 'connected'}, broadcast=True)
    else:
        emit('error', {'error': 'User not found'})

@socketio.on('disconnect_user')
def handle_disconnect_user(data):
    user = data['user']
    if user in connections:
        connections[user] = False
        emit('user_disconnected', {'user': user, 'status': 'disconnected'}, broadcast=True)
    else:
        emit('error', {'error': 'User not found'})

@socketio.on('connect_all')
def handle_connect_all():
    for user in connections:
        connections[user] = True
    emit('all_connected', {'status': 'all connected'}, broadcast=True)

@socketio.on('disconnect_all')
def handle_disconnect_all():
    for user in connections:
        connections[user] = False
    emit('all_disconnected', {'status': 'all disconnected'}, broadcast=True)

@socketio.on('request_video_feed')
def handle_video_feed():
    # Logic to start sending video feed
    emit('video_feed', {'feed': 'video stream data goes here'})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
