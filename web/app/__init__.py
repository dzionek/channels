"""
This is the main package of the application.
This particular module contains the app factory.
"""
from datetime import datetime

from flask import Flask, url_for, request
from flask_login import current_user
from flask_socketio import SocketIO, join_room, leave_room, emit

from .config import configure_app
from . import models, main, login, bcrypt, login_manager, cli
import app.cli.commands
from .main.utils import pretty_time
from .models import Channel, Message, db


def create_app() -> Flask:
    """Flask app factory initialising all its components.

    Returns:
        The created Flask application.

    """
    app = Flask(__name__)
    configure_app(app)

    models.init_app(app)
    main.init_app(app)
    login.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    cli.init_app(app)

    return app


app = create_app()
socket_io = SocketIO(app)


@socket_io.on('join room')
def on_join(data):
    """TODO"""
    room = data['room']
    join_room(room)
    print(f'You have joined room {room}')

@socket_io.on('leave room')
def on_leave(data):
    """TODO"""
    room = data['room']
    leave_room(room)
    print(f'You have left room {room}')

@socket_io.on('add message')
def add_message(data: dict):
    channel = data['channel']
    message_content = data['message_content']

    username = current_user.username
    user_id = current_user.id
    user_picture = f"{url_for('static', filename='img/profile_pictures')}/{ current_user.profile_picture }"

    full_time = datetime.utcnow()

    channel_id = Channel.query.filter_by(name=channel).first().id

    db.session.add(Message(
        content=message_content, user_id=user_id, time=full_time, channel_id=channel_id
    ))

    db.session.commit()
    return announce_message(username, user_picture, pretty_time(full_time), channel, message_content)

def announce_message(user_name: str, user_picture: str, time: str, channel: str, message_content: str) -> None:
    """Emit all information about the message that was added to DB.

    Args:
        user_name: Name of the user who sent the message.
        user_picture: Picture of the user who sent the message.
        time: Time when she/he sent it.
        channel: Channel the message was sent to.
        message_content: Content of the message.

    """
    response = {
        'userName': user_name,
        'userPicture': user_picture,
        'time': time,
        'channel': channel,
        'messageContent': message_content
    }
    room = Channel.query.filter_by(name=channel).first().id
    print(f'Announce message: {response} to room {room}. Session id: {request.sid}')
    emit('announce message', response, room=room)