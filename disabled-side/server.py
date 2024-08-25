import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify, Response
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading
import os
import signal
import cv2
import subprocess

cred = credentials.Certificate('isl-sih-firebase-adminsdk-34c6u-4b9c452afa.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

processes = {}

@app.route('/start_server', methods=['POST'])
def start_server():
    data = request.get_json()
    user = data.get('user')
    thread = threading.Thread(target=run_server, args=(user,))
    thread.start()
    return jsonify({'message': 'Server started for user: ' + user})

@app.route('/stop_all_servers', methods=['POST'])
def stop_all_servers():
    for user, process in processes.items():
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    processes.clear()
    return jsonify({'message': 'All servers stopped'})

@app.route('/connect_all', methods=['POST'])
def connect_all():
    users_ref = db.collection('users')
    users = users_ref.stream()
    for user in users:
        user_id = user.id
        thread = threading.Thread(target=run_server, args=(user_id,))
        thread.start()
    return jsonify({'message': 'All users connected'})

@app.route('/video_feed/<user>')
def video_feed(user):
    return Response(generate_video_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_video_feed():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video device.")
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

def run_server(user):
    process = subprocess.Popen(['python3', 'intercom.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
    processes[user] = process
    for line in iter(process.stdout.readline, b''):
        output = line.decode('utf-8').strip()
        print(output)
        send_to_firestore(user, output)
        socketio.emit('server_output', output)

def send_to_firestore(user, output):
    doc_ref = db.collection('users').document(user)
    doc_ref.set({'output': output})

    all_ref = db.collection('users').document('all')
    all_ref.set({'output': output}, merge=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)