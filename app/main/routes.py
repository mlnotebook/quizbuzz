from app import db
from app.main import bp
from app.models import User, Quiz
from flask_login import current_user, login_required, login_user
from flask import render_template, redirect, url_for, flash, request, session
from werkzeug.urls import url_parse
from app.main.forms import JoinQuizForm, LeaveQuizForm, DeleteUsersForm, CreateQuizForm, DeleteQuizForm, UserBuzzerInForm
from flask_socketio import emit


@bp.before_app_request
def before_request():
    pass


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    """Renders the homepage.

    Creates a quizzer or quizmaster. Adds them to the db.
    Sets the username and quizid of the user in the session.
    Button to delete all users and quizzes from the db.
    """
    join_form = JoinQuizForm()
    create_form = CreateQuizForm()

    if join_form.joinSubmit.data and join_form.validate():
        quiz = Quiz.query.filter_by(id=join_form.quizid.data).first_or_404()
        user = User(username=join_form.username.data,
                    quizid=quiz.id)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        user.set_logged_in_status(True)
        db.session.commit()
        session["USERNAME"] = user.username
        session["QUIZID"] = quiz.id
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.quiz')
        return redirect(next_page)

    if create_form.createSubmit.data and create_form.validate():
        quiz = Quiz(quizname=create_form.quizname.data,
                    quizmaster=create_form.username.data)
        db.session.add(quiz)
        db.session.commit()
        user = User(username=create_form.username.data,
                    quizid=quiz.id)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        user.set_logged_in_status(True)
        db.session.commit()
        session["USERNAME"] = user.username
        session["QUIZID"] = quiz.id
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.quizmaster')
        return redirect(next_page)

    return render_template('index.html',
                           title='Home',
                           join_form=join_form,
                           create_form=create_form)


@bp.route('/delete_all_users', methods=['GET', 'POST'])
def delete_all_users():
    """Renders the delete all users page."""
    delete_users_form = DeleteUsersForm()

    if delete_users_form.deleteUsersSubmit.data and delete_users_form.validate():
        try:
            num_users_deleted = db.session.query(User).delete()
            num_quizes_deleted = db.session.query(Quiz).delete()
            db.session.commit()
            flash(f'Users Removed: {num_users_deleted}')
            flash(f'Quizes Removed: {num_quizes_deleted}')
        except:
            db.session.rollback()
        return redirect(url_for('main.index'))
    return render_template('_delete_all_users.html', delete_users_form=delete_users_form)


@bp.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    """Renders page for the quizzers.

    Leave button removes lets quizzers remove self from db and quiz.
    """
    leave_quiz_form = LeaveQuizForm()
    user_buzzed_in_form = UserBuzzerInForm()

    if leave_quiz_form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first_or_404()
        db.session.delete(user)
        db.session.commit()
        flash('User Removed')
        return redirect(url_for('main.index'))

    room = session.get("QUIZID")
    quiz = Quiz.query.filter_by(id=current_user.quizid).first_or_404()
    logged_in_users = User.query.filter_by(logged_in_status=True, quizid=quiz.id).all()
    return render_template('quiz.html',
                           title='Quiz',
                           quiz=quiz,
                           leave_quiz_form=leave_quiz_form,
                           logged_in_users=logged_in_users,
                           room=room,
                           user_buzzed_in_form=user_buzzed_in_form)


@bp.route('/quizmaster', methods=['GET', 'POST'])
@login_required
def quizmaster():
    """Renders page for the quizmaster.

    Delete quiz button removes the quiz from db.
    """
    quiz = Quiz.query.filter_by(id=current_user.quizid).first_or_404()

    if current_user.username != quiz.quizmaster:
        flash('Only the Quizmaster can view that page!')
        return redirect(url_for('main.index'))

    delete_quiz_form = DeleteQuizForm()
    user_buzzed_in_form = UserBuzzerInForm()

    if delete_quiz_form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first_or_404()
        db.session.delete(user)
        db.session.delete(quiz)
        db.session.commit()
        flash('User Removed')
        flash('Quiz Removed')
        return redirect(url_for('main.index'))

    room = session.get("QUIZID")
    quiz = Quiz.query.filter_by(id=current_user.quizid).first_or_404()
    logged_in_users = User.query.filter_by(logged_in_status=True, quizid=quiz.id).all()
    return render_template('quizmaster.html',
                           title='Quizmaster',
                           delete_quiz_form=delete_quiz_form,
                           logged_in_users=logged_in_users,
                           quiz=quiz,
                           room=room,
                           user_buzzed_in_form=user_buzzed_in_form
                           )


@bp.route('/remove_user/<username>', methods=['GET', 'POST'])
@login_required
def remove_user(username):
    """Emits request to remove user from the quiz."""
    quizid = session.get('QUIZID')
    quiz = Quiz.query.filter_by(id=quizid).first_or_404()
    quizmaster = User.query.filter_by(username=quiz.quizmaster).first_or_404()

    emit('remove_quizzer', {'username': username}, room=quizmaster.session_id)


@bp.route('/_type_answer', methods=['GET', 'POST'])
@login_required
def _type_answer():
    """Renders the type answer question div."""
    return render_template('_type_answer.html')


@bp.route('/_buzzer', methods=['GET', 'POST'])
@login_required
def _buzzer():
    """Renders the buzzer question div."""
    return render_template('_buzzer.html')
