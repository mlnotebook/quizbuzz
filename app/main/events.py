from flask import session
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from .. import socketio


@socketio.on('joined', namespace='/quiz')
def joined(message):
    if current_user.is_authenticated:
        room = session.get("QUIZID")
        join_room(room)
        msg = session.get("USERNAME") + ' has joined!'
        emit('joined', {'msg': msg}, room=room)


@socketio.on('buzz', namespace='/quiz')
def buzz(message):
    if current_user.is_authenticated:
        room = session.get("QUIZID")
        emit('buzz', {'username': f'{session.get("USERNAME")}'}, room=room)


@socketio.on('reset', namespace='/quiz')
def reset(message):
    if current_user.is_authenticated:
        room = session.get("QUIZID")
        emit('reset', {}, room=room)


@socketio.on('start', namespace='/quiz')
def start(message):
    if current_user.is_authenticated:
        room = session.get("QUIZID")
        emit('start', {}, room=room)


@socketio.on('left', namespace='/quiz')
def left(message):
    if current_user.is_authenticated:
        room = session.get("QUIZID")
        leave_room(room)
        msg = session.get("USERNAME") + ' left the room!!'
        emit('status', {'msg': msg}, room=room)
