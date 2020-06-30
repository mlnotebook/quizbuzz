from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from app.models import User, Quiz


class JoinQuizForm(FlaskForm):
    """Join quiz form."""
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
    """Create quiz form. Creator becomes the quizmaster."""
    username = StringField('Quizmaster', validators=[DataRequired()])
    quizname = StringField('Quiz Name', validators=[DataRequired()])
    createSubmit = SubmitField('Create Quiz')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class UserBuzzerInForm(FlaskForm):
    """Area to show the users that buzzed."""
    buzzed_in_area = TextAreaField('', id="chat")


class LeaveQuizForm(FlaskForm):
    """The quizzers' leave quiz button."""
    leaveQuizSubmit = SubmitField('Leave Quiz')


class DeleteQuizForm(FlaskForm):
    """The quizmaster's delete quiz button."""
    deleteQuizSubmit = SubmitField('Delete Quiz')


class DeleteUsersForm(FlaskForm):
    """Delete all users and quizzes from the db."""
    deleteUsersSubmit = SubmitField('Delete All Users')


class FastestFingerForm(FlaskForm):
    """Start Fastest Finger First Round."""
    fastestFingerSubmit = SubmitField('FastestFinger')


class EmptyForm(FlaskForm):
    """Empty submit button."""
    submit = SubmitField('Submit')

