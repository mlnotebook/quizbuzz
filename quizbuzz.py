import eventlet
eventlet.monkey_patch()

from app import create_app, db, socketio
from app.models import User, Quiz

app = create_app(debug=True)


@app.shell_context_processor
def make_shell_context():
    return{'db': db, 'User': User, 'Quiz': Quiz}


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')