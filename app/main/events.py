from flask import session, render_template, request, redirect, url_for
from app.models import User, Quiz
from app.main.forms import EmptyForm
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from .. import socketio, db


@socketio.on('joined', namespace='/quiz')
def joined(message):
    """When a user joins (or reconnects) to the session.

    Gets the session id of the new user from the request.
    Adds the session id to the user's db entry.
    Emits notification to everyone in the room except the new user.
    """
    if current_user.is_authenticated:
        room = session.get("QUIZID")
        new_user_sessionid = request.sid
        user = User.query.filter_by(username=current_user.username).first_or_404()
        user.session_id = new_user_sessionid
        db.session.commit()
        join_room(room)
        emit('joined', {'new_user': session.get("USERNAME"), 'new_user_sessionid': new_user_sessionid}, room=room,
             broadcast=True, include_self=False)


@socketio.on('add_quizzer', namespace='/quiz')
def add_quizzer(message):
    """When a quizzer is added every other user requests this.

    Render the new user tile (which adds 'remove' button if quizmaster).
    Sends the user tile back to each individual user (except new user).
    """
    if current_user.is_authenticated:
        remove_quizzer_form = EmptyForm()
        quiz = Quiz.query.filter_by(id=current_user.quizid).first_or_404()
        user = User.query.filter_by(username=message['new_user']).first_or_404()
        quizzers = render_template('_user_tile.html',
                                   logged_in_user=user,
                                   remove_quizzer_form=remove_quizzer_form,
                                   quiz=quiz)
        new_user_sessionid = message['new_user_sessionid']
        this_session_id = request.sid
        emit('add_quizzer', {'quizzers': quizzers, 'new_user': message['new_user']}, room=this_session_id,
             skip_sid=new_user_sessionid)


@socketio.on('buzz', namespace='/quiz')
def buzz(message):
    """When a user presses the buzzer."""
    if current_user.is_authenticated:
        room = session.get("QUIZID")
        emit('buzz', {'username': f'{session.get("USERNAME")}', 'timedelta': message['timedelta']}, room=room)


@socketio.on('type_buzz', namespace='/quiz')
def type_buzz(message):
    """When a user sends their answer."""
    if current_user.is_authenticated:
        room = session.get("QUIZID")
        quiz = Quiz.query.filter_by(id=room).first_or_404()
        quizmaster_user = User.query.filter_by(username=quiz.quizmaster).first_or_404()
        quizmaster_session = quizmaster_user.session_id
        emit('buzz', {'username': f'{session.get("USERNAME")}', 'timedelta': message['timedelta']}, room=room, skip_sid=quizmaster_session)
        emit('buzzed_quizmaster', {'username': f'{session.get("USERNAME")}', 'timedelta': message['timedelta'], 'answer': message['answer']}, room=quizmaster_session)


@socketio.on('reset', namespace='/quiz')
def reset(message):
    """When the quizmaster resets the quiz."""
    if current_user.is_authenticated:
        room = session.get("QUIZID")
        emit('reset', {}, room=room)


@socketio.on('start_fastest_finger', namespace='/quiz')
def start_fastest_finger(message):
    """When the quizmaster starts fastest finger round."""
    if current_user.is_authenticated:
        room = session.get("QUIZID")
        emit('start_fastest_finger', {}, room=room)


@socketio.on('start_type_answer', namespace='/quiz')
def start_type_answer(message):
    """When the quizmaster starts type answer round."""
    if current_user.is_authenticated:
        room = session.get("QUIZID")
        emit('start_type_answer', {}, room=room)


@socketio.on('user_left', namespace='/quiz')
def user_left(message):
    """When a quizzer leaves the quiz."""
    if current_user.is_authenticated:
        room = session.get("QUIZID")
        leave_room(room)
        user = User.query.filter_by(username=message['username']).first()
        db.session.delete(user)
        db.session.commit()
        emit('remove_quizzer', {'username': message['username']}, room=room)


@socketio.on('remove_user', namespace='/quiz')
def remove_user(message):
    """When the quizmaster removes a quizzer.

    Find that user and delete them from the db.
    Emit request to send that user back to the homepage.
    Emit request to remove user from the quizzers list.
    """
    if current_user.is_authenticated:
        room = session.get('QUIZID')
        user = User.query.filter_by(username=message['username']).first()
        db.session.delete(user)
        db.session.commit()
        emit('remove_user', {'username': message['username']}, room=user.session_id, include_self=False)
        emit('remove_quizzer', {'username': message['username']}, room=room)
