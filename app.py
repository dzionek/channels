from os import environ

from flask import Flask, render_template, session, request
from flask_session import Session

from models import *


app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Session()

db.init_app(app)

def create_db():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return log_in(request.form)
    else:
        if is_logged():
            return set_up_app()
        else:
            return render_template('login.html')

def log_in(request_form):
    username = request_form.get('username')
    session['username'] = username
    return set_up_app()

def is_logged():
    if not session.get('username'):
        return False
    elif not isinstance(session['username'], str):
        raise TypeError('Username is not a string')
    else:
        return True

def set_up_app():
    username = session['username']
    if not User.query.filter_by(username=username).first():
        db.session.add(User(username=username))
        db.session.commit()

    channels = Channel.query.all()
    messages = Message.query.all()

    return render_template(
        'app.html', username=username, channels=channels, messages=messages
    )


if __name__ == '__main__':
    with app.app_context():
        create_db()
        app.debug = True
        app.run()
