from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app, async_mode='gevent')

@app.route('/record/<id>')
def record(id):
    return render_template('record.html', id=id)

@app.route('/watch/<id>')
def watch(id):
    return render_template('watch.html', id=id)

@socketio.on('join', namespace='/ws')
def join(data):
    room = data['room']
    join_room(room)
    emit('status', {'msg': f'Joined room: {room}'}, room=room)

@socketio.on('leave', namespace='/ws')
def leave(data):
    room = data['room']
    leave_room(room)
    emit('status', {'msg': f'Left room: {room}'}, room=room)

@socketio.on('stream', namespace='/ws')
def stream(data):
    room = data['room']
    emit('stream', {'data': data['data']}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)