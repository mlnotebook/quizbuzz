from app import db, login
from hashlib import md5
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    logged_in_status = db.Column(db.Boolean, index=False, unique=False)
    quizid = db.Column(db.Integer, index=False, unique=False)
    session_id = db.Column(db.Integer, index=False, unique=True)

    def __repr__(self):
        return '<User {}, quizid {}>'.format(self.username, self.quizid)

    def avatar(self, size):
        digest = md5(self.username.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def set_logged_in_status(self, status):
        self.logged_in_status = status


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quizname = db.Column(db.String(64), index=True, unique=False)
    quizmaster = db.Column(db.String(64), index=True, unique=False)

    def __repr__(self):
        return f'<Quiz id: {self.id}, quizname: {self.quizname}>'

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
