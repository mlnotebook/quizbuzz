from app import create_app, db, socketio
from app.models import User, Quiz

app = create_app(debug=True)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Quiz': Quiz}


if __name__ == '__main__':
    """Launches the WebApp.
    
    host='0.0.0.0' ensures that other devices on local network
    can access the app.
    flask-socketio replaces app.run in order to enable WebSockets.
    """
    socketio.run(app, host='0.0.0.0')
