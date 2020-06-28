from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from app.models import User, Quiz


class JoinQuizForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    quizid = StringField('Quiz ID', validators=[DataRequired()])
    joinSubmit = SubmitField('Join Quiz')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_quizid(self, quizid):
        quiz = Quiz.query.filter_by(id=quizid.data).first()
        if quiz is None:
            raise ValidationError('Quiz ID does not exist.')


class CreateQuizForm(FlaskForm):
    username = StringField('Quizmaster', validators=[DataRequired()])
    quizname = StringField('Quiz Name', validators=[DataRequired()])
    createSubmit = SubmitField('Create Quiz')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class BuzzerForm(FlaskForm):
    buzzSubmit = SubmitField('Buzz')
    buzzed_in_area = TextAreaField('', id="chat")


class LeaveQuizForm(FlaskForm):
    leaveQuizSubmit = SubmitField('Leave Quiz')


class DeleteQuizForm(FlaskForm):
    deleteQuizSubmit = SubmitField('Delete Quiz')


class DeleteUsersForm(FlaskForm):
    deleteUsersSubmit = SubmitField('Delete All Users')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

