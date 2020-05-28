from os import environ
import re

from flask import Flask, render_template, session, request, jsonify
from flask_session import Session

from models import *


app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Session()

db.init_app(app)

valid_pattern = re.compile(r'[A-Za-z0-9 \-_]+')

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


def channel_has_invalid_name(channel_name: str) -> bool:

    if not channel_name:
        return True
    else:
        return not(bool(re.fullmatch(valid_pattern, channel_name)))\
               or channel_name.startswith(' ')\
               or channel_name.endswith(' ')


def channel_already_exists(channel_name):
    channel = Channel.query.filter_by(name=channel_name).first()
    return bool(channel)

def add_channel(channel_name):
    db.session.add(Channel(name=channel_name))
    db.session.commit()

@app.route('/add-channel', methods=['POST'])
def add_channel_ajax():
    channel_name = request.form.get('channelName')
    if channel_has_invalid_name(channel_name):
        return jsonify({'success': False, 'errorMessage': f'You cannot create a channel of the given name: {channel_name}'})
    elif channel_already_exists(channel_name):
        return jsonify({'success': False, 'errorMessage': 'The channel already exists'})
    else:
        add_channel(channel_name)
        return jsonify({'success': True, 'errorMessage': 'None'})


if __name__ == '__main__':
    with app.app_context():
        create_db()
        app.debug = True
        app.run()
